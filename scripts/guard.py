#!/usr/bin/env python3
"""PreToolUse guard for SDD (stdlib only).

The guard gives agents freedom and blocks only what is irreversible or the human's to decide.

- SDD agents: every call is approved automatically, except the denylist below, which is denied.
  Writes must stay inside the project (from an agent worktree, only specs/ and .sdd/ may be written
  back to the main checkout). MCP tools that look like writes are denied: external writes go through
  the hub after the human approves them (/sdd sync).
- The hub (main session): its bookkeeping is approved automatically (git, the trace script, and its
  own files). A denylisted command is not approved: the human gets the normal permission prompt.
  Everything else in the main session keeps normal prompts.
- Reads of the plugin's own files are approved for everyone, so agents can use the methodology.

Denylist: committing, merging or pushing to the main branch; force-pushes; deleting remote branches;
merging or publishing PRs and releases; production deploys and infrastructure applies; destructive
deletes and data operations; writes to outside systems. Projects can add prefixes in .sdd/config.yaml
(permissions.deny_commands). Set permissions.auto_approve: false to get normal prompts instead of
automatic approval; denials still apply.
"""

import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

AGENTS = {
    "product-lead", "ux-designer", "researcher", "architect", "tech-lead", "engineer", "test-engineer",
    "platform-engineer", "challenger", "code-reviewer", "security-engineer", "reliability-engineer",
    "consultant", "cartographer", "librarian", "incident-responder",
}
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_TOOLS = {"Read", "Glob", "Grep"}
HUB_FILES = re.compile(r"^(specs/[^/]+/(state\.yaml|decisions\.md)|\.sdd/(stack\.yaml|constitution\.md|config\.yaml))$")
SDD_SCRIPT = re.compile(r"^(rtk )?uv run (-q )?\"?/\S+?/skills/sdd-contracts/scripts/sdd\.py\"? (trace|stale|expected-failing)\b")
SEGMENTS = re.compile(r"&&|\|\||;|\||\n")
MAIN = r"(main|master)"
MCP_WRITE = re.compile(
    r"(^|[_\-])(create|update|delete|remove|add|set|send|post|write|edit|complete|uncomplete|"
    r"move|upload|publish|reschedule|reorder|manage|respond|import|insert|merge|close|assign|"
    r"comment|batch|execute|run)", re.I)

DENY = [
    (re.compile(rf"\bgit\s+push\b.*(\s|:|\+|refs/heads/){MAIN}(\s|$)"), "pushing to the main branch is the human's decision"),
    (re.compile(r"\bgit\s+push\b.*(\s-f\b|--force|\s\+\S)"), "force-pushing is the human's decision"),
    (re.compile(r"\bgit\s+push\b.*(\s--delete\b|\s-d\b|\s:\S)"), "deleting remote branches is the human's decision"),
    (re.compile(rf"\bgit\s+(switch|checkout)\s+{MAIN}\b.*\bgit\s+(merge|commit|rebase|cherry-pick|revert|pull|am)\b"),
     "committing or merging into the main branch is the human's decision"),
    (re.compile(r"\bgh\s+pr\s+(merge|ready)\b|\bgh\s+release\s+(create|delete|edit|upload)\b|\bgh\s+repo\s+(delete|archive|rename)\b"),
     "merging or publishing on the remote is the human's decision"),
    (re.compile(r"\bgh\s+(issue|pr)\s+(comment|review|close|reopen|edit|lock|delete)\b|\bgh\s+issue\s+(create|transfer)\b"),
     "writes to outside systems need the human's approval (/sdd sync)"),
    (re.compile(r"\b(terraform|tofu|pulumi)\s+(apply|destroy|up|import)\b|\bcdk\s+(deploy|destroy)\b|\b(sam|serverless|sls)\s+(deploy|remove)\b"
                r"|\bkubectl\s+(apply|create|delete|replace|patch|scale|rollout)\b|\bhelm\s+(install|upgrade|uninstall|rollback)\b"
                r"|\b(gcloud|aws|az)\b.*\b(deploy|delete|create-stack|update-stack|delete-stack)\b|\b(fly|flyctl|railway)\s+(deploy|up|destroy)\b"
                r"|\b(vercel|netlify)\b.*--prod\b|\bheroku\b.*\b(deploy|destroy|releases:rollback)\b"),
     "production deploys and infrastructure changes are the human's decision (G3 / env-plan)"),
    (re.compile(r"(^|\s)(sudo|su|mkfs\S*|shutdown|reboot|halt)(\s|$)|\bdd\s+if=", re.I), "system-level and destructive commands are never allowed"),
    (re.compile(r"\b(drop\s+(database|schema|table)|truncate\s+table)\b", re.I), "destructive data operations are the human's decision"),
    (re.compile(r"\b(curl|wget|http|httpie)\b.*(\s-X\s*(POST|PUT|PATCH|DELETE)\b|\s--data\b|\s-d\s|\s--upload-file\b|\s-F\s)", re.I),
     "writes to outside systems need the human's approval (/sdd sync)"),
]
LOCAL_HOST = re.compile(r"(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])")


def decide(kind: str, reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": kind,
        "permissionDecisionReason": f"SDD guard: {reason}",
    }}))
    sys.exit(0)


def main_root(cwd: Path) -> Path:
    """The main checkout when running inside an agent worktree (.claude/worktrees/<id>), else cwd."""
    parts = cwd.resolve().as_posix().split("/.claude/worktrees/")
    return Path(parts[0]) if len(parts) > 1 else cwd.resolve()


def config_text(cwd: Path) -> str:
    try:
        return (main_root(cwd) / ".sdd" / "config.yaml").read_text(encoding="utf-8")
    except OSError:
        return ""


def auto_approve(cwd: Path) -> bool:
    return not re.search(r"^\s*auto_approve\s*:\s*(false|no|off)\b", config_text(cwd), re.M | re.I)


def extra_denies(cwd: Path) -> list[str]:
    """Quoted prefixes listed under permissions.deny_commands in .sdd/config.yaml."""
    out, inside = [], False
    for line in config_text(cwd).splitlines():
        if re.match(r"^\s+deny_commands\s*:", line):
            inside = True
            continue
        if inside:
            m = re.match(r'^\s+-\s*["\']([^"\']+)["\']', line)
            if m:
                out.append(m.group(1).strip())
            elif line.strip() and not line.lstrip().startswith("#"):
                break
    return out


def current_branch(cwd: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(cwd), "branch", "--show-current"], capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def nonprod_deploy(cmd: str, cwd: Path) -> bool:
    """True if the command matches a `deploy-nonprod` prefix in the committed .sdd/stack.yaml."""
    try:
        out = subprocess.run(["git", "-C", str(main_root(cwd)), "show", "HEAD:.sdd/stack.yaml"],
                             capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return False
    m = re.search(r"^\s{2}deploy-nonprod\s*:\s*\n((?:\s{4}-.*\n?)+)", out.stdout, re.M)
    prefixes = re.findall(r'-\s*"([^"]+)"', m.group(1)) if m else []
    return any(cmd == p or cmd.startswith(p + " ") or (p.endswith("/") and cmd.startswith(p) and ".." not in cmd)
               for p in prefixes if not p.startswith("<"))


def destructive_rm(cmd: str, cwd: Path) -> bool:
    """A recursive rm whose target is outside the project, the project root itself, or a home/root path."""
    root = main_root(cwd)
    for seg in SEGMENTS.split(cmd):
        try:
            words = shlex.split(seg)
        except ValueError:
            return True
        if not words or Path(words[0]).name != "rm":
            continue
        flags = [w for w in words[1:] if w.startswith("-")]
        if not any("r" in f.lower() or f == "--recursive" for f in flags):
            continue
        for target in (w for w in words[1:] if not w.startswith("-")):
            if target.startswith(("~", "$")) or target in ("/", "*", ".", ".."):
                return True
            path = (cwd / target).resolve() if not Path(target).is_absolute() else Path(target).resolve()
            if path == root or root not in path.parents:
                return True
    return False


def denied(cmd: str, cwd: Path) -> str | None:
    """Why the command is on the denylist, or None."""
    for pattern, reason in DENY:
        if pattern.search(cmd):
            if "deploy" in reason and nonprod_deploy(cmd, cwd):
                continue
            if "outside systems" in reason and "curl" in pattern.pattern and LOCAL_HOST.search(cmd):
                continue
            return reason
    if re.search(rf"(^|\s|&&|;)git\s+(merge|commit|rebase|cherry-pick|revert|pull|am)\b", cmd) and \
            re.fullmatch(MAIN, current_branch(cwd)):
        return "committing or merging into the main branch is the human's decision"
    if re.search(r"\bgh\s+pr\s+create\b", cmd) and "--draft" not in cmd:
        return "only draft PRs are autonomous; a ready PR is the human's decision"
    if destructive_rm(cmd, cwd):
        return "recursive deletes outside the project (or of the project itself) are never allowed"
    for prefix in extra_denies(cwd):
        if any(s.strip() == prefix or s.strip().startswith(prefix + " ") for s in SEGMENTS.split(cmd)):
            return f"'{prefix}' is denied by this project's config (permissions.deny_commands)"
    return None


def rel_to(path: Path, root: Path) -> str | None:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except (ValueError, OSError):
        return None


def target_path(tin: dict, cwd: Path) -> Path:
    raw = Path(tin.get("file_path") or tin.get("notebook_path") or "")
    return raw if raw.is_absolute() else cwd / raw


def hub(tool: str, tin: dict, cwd: Path) -> None:
    """Main session: approve the hub's bookkeeping; anything else keeps the normal prompt."""
    if not (main_root(cwd) / ".sdd").is_dir():
        return  # not an SDD project (or before /sdd init): normal prompts
    if tool in WRITE_TOOLS:
        rel = rel_to(target_path(tin, cwd), cwd)
        if rel and HUB_FILES.match(rel) and auto_approve(cwd):
            decide("allow", f"hub bookkeeping: '{rel}'")
    elif tool == "Bash":
        cmd = (tin.get("command") or "").strip()
        segments = [s.strip() for s in SEGMENTS.split(cmd) if s.strip()]
        ok = segments and all(s.startswith("git ") or s == "git" or SDD_SCRIPT.match(s) for s in segments)
        if ok and not denied(cmd, cwd) and auto_approve(cwd):
            decide("allow", "hub bookkeeping command")


def agent_call(name: str, tool: str, tin: dict, cwd: Path) -> None:
    """SDD agents: deny the denylist, approve everything else."""
    approve = auto_approve(cwd)
    if tool in WRITE_TOOLS:
        path = target_path(tin, cwd)
        root = main_root(cwd)
        if rel_to(path, cwd) is None:
            rel_main = rel_to(path, root)
            if rel_main is None:
                decide("deny", f"{name} may not write outside the project ({path}).")
            if cwd.resolve() != root and not rel_main.startswith(("specs/", ".sdd/")):
                decide("deny", f"{name} works in its own worktree; only specs/ and .sdd/ may be written to the main checkout.")
        if approve:
            decide("allow", f"{name} write")
        return
    if tool == "Bash":
        cmd = (tin.get("command") or "").strip()
        why = denied(cmd, cwd)
        if why:
            decide("deny", f"{why}. Escalate it to the hub instead.")
        if approve:
            decide("allow", f"{name} command")
        return
    if tool.startswith("mcp__"):
        method = tool.split("__")[-1]
        if MCP_WRITE.search(method):
            decide("deny", f"'{method}' looks like a write to an outside system. External writes are performed "
                           "by the hub after the human approves them; list it under escalations.")
        if approve:
            decide("allow", f"{name} read-only integration call")
        return
    if approve:
        decide("allow", f"{name} {tool}")


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parent.parent).resolve()
    tool = data.get("tool_name", "")
    tin = data.get("tool_input") or {}
    cwd = Path(data.get("cwd") or os.getcwd())

    if tool in READ_TOOLS:
        target = tin.get("file_path") or tin.get("path") or ""
        if target and rel_to(Path(target).expanduser(), plugin_root) is not None:
            decide("allow", "reading SDD methodology files shipped with the plugin")
        return

    agent = (data.get("agent_type") or "").split(":")[-1]
    if not agent:
        hub(tool, tin, cwd)
    elif agent in AGENTS:
        agent_call(agent, tool, tin, cwd)


if __name__ == "__main__":
    main()
