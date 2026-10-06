#!/usr/bin/env python3
"""PreToolUse ownership guard for SDD agents (stdlib only).

Reads the hook input on stdin. If the call comes from an SDD agent listed in
hooks/ownership.json, denies writes outside its owned paths, shell commands
outside its allowlist, and (optionally) MCP tools that look like writes.
Project commands come from the committed .sdd/commands.yaml (by purpose), so
agents' shell permissions follow each project's stack; a global denylist always
applies. In-policy calls (owned writes, allowlisted commands) are approved outright so
agents can work without permission prompts; set 'permissions: auto_approve:
false' in .sdd/config.yaml to fall back to normal prompts. Deny rules still win.
Reads of the plugin's own files are auto-allowed for everyone, so agents can
use the methodology references and templates. Everything else is left to the
normal permission flow.
"""

import fnmatch
import json
import os
import re
import subprocess
import sys
from pathlib import Path

WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
READ_TOOLS = {"Read", "Glob", "Grep"}
CHAINING = re.compile(r"[;&|`\n]|\$\(|>|<")
MCP_WRITE = re.compile(
    r"(^|[_\-])(create|update|delete|remove|add|set|send|post|write|edit|complete|uncomplete|"
    r"move|upload|publish|reschedule|reorder|manage|respond|import|insert|merge|close|assign|"
    r"comment|batch|execute|run)", re.I)


def deny(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"SDD ownership guard: {reason}",
    }}))
    sys.exit(0)


def allow(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": f"SDD: {reason}",
    }}))
    sys.exit(0)


def is_within(path: Path, root: Path) -> bool:
    try:
        path.expanduser().resolve().relative_to(root)
        return True
    except (ValueError, OSError):
        return False


# Never allowed through the project command registry, whatever prefix matched.
DANGEROUS = re.compile(
    r"(^|\s)(sudo|su|rm|rmdir|mkfs|dd|shutdown|reboot|halt|chmod|chown|ssh|scp|rsync|wget|curl|nc|eval|exec)(\s|$)"
    r"|git\s+(push|reset\s+--hard|clean|checkout\s+--|branch\s+-D|filter-branch|update-ref)"
    r"|\s-c\s|--force\b|--no-verify\b")


def worktree_project_root(cwd: Path) -> Path:
    """The main checkout when running inside an agent worktree (.claude/worktrees/<id>), else cwd."""
    parts = cwd.resolve().as_posix().split("/.claude/worktrees/")
    return Path(parts[0]) if len(parts) > 1 else cwd.resolve()


def committed_file(cwd: Path, rel: str) -> str:
    """Content of a file as committed on the current branch (HEAD); '' if unavailable."""
    try:
        out = subprocess.run(["git", "-C", str(cwd), "show", f"HEAD:{rel}"],
                             capture_output=True, text=True, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return ""
    return out.stdout if out.returncode == 0 else ""


def project_commands(cwd: Path) -> dict[str, list[str]]:
    """Parse the committed .sdd/commands.yaml: {purpose: [prefix, …]} (restricted, stdlib-only format)."""
    registry: dict[str, list[str]] = {}
    purpose = None
    in_commands = False
    for line in committed_file(cwd, ".sdd/commands.yaml").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^commands\s*:", line):
            in_commands = True
            continue
        if in_commands and re.match(r"^\S", line):
            in_commands = False
        if not in_commands:
            continue
        m = re.match(r"^\s{2}([\w-]+)\s*:", line)
        if m:
            purpose = m.group(1)
            registry.setdefault(purpose, [])
            continue
        m = re.match(r'^\s+-\s*"([^"]+)"', line) or re.match(r"^\s+-\s*'([^']+)'", line)
        if m and purpose and not m.group(1).startswith("<"):
            registry[purpose].append(m.group(1).strip())
    return registry


def matched_purpose(cmd: str, purposes: list[str], registry: dict[str, list[str]]) -> tuple[str, str] | None:
    """(purpose, prefix) of the longest registry prefix the command starts with, among allowed purposes."""
    best = None
    for purpose in purposes:
        for prefix in registry.get(purpose, []):
            under_path = prefix.endswith("/") and cmd.startswith(prefix) and ".." not in cmd[len(prefix):].split(" ")[0]
            if cmd == prefix or cmd.startswith(prefix + " ") or under_path:
                if best is None or len(prefix) > len(best[1]):
                    best = (purpose, prefix)
    return best


def normalize_dep(token: str) -> str:
    name = token.strip("'\"")
    if name.startswith("@"):                      # scoped package: keep the scope, drop a version
        at = name.find("@", 1)
        name = name[:at] if at > 0 else name
    else:
        name = re.split(r"[\[<>=~!^;@ ]", name, maxsplit=1)[0]
    return name.replace("_", "-").lower()


def unapproved_runtime_deps(args: str, cwd: Path) -> list[str]:
    """Packages in a deps-add command's arguments not approved in .sdd/dependencies.yaml."""
    pkgs = [normalize_dep(t) for t in args.split() if not t.startswith("-")]
    if not pkgs:
        return []
    text = committed_file(cwd, ".sdd/dependencies.yaml")
    if not text:
        try:
            text = (worktree_project_root(cwd) / ".sdd" / "dependencies.yaml").read_text(encoding="utf-8")
        except OSError:
            text = ""
    approved = {normalize_dep(n) for n in re.findall(r"^\s*-?\s*name\s*:\s*['\"]?([@\w./-]+)", text, re.M)}
    return [p for p in pkgs if p not in approved]


def project_rel(raw: str, cwd: Path) -> str:
    path = Path(raw)
    if not path.is_absolute():
        path = cwd / path
    try:
        return Path(os.path.relpath(path.resolve(), cwd.resolve())).as_posix()
    except ValueError:
        return str(path)


def hub_grants(policy: dict, tool: str, tin: dict, cwd: Path) -> None:
    """Main session: approve only the hub's own bookkeeping; everything else keeps normal prompts."""
    if not policy:
        return
    if tool in WRITE_TOOLS:
        rel = project_rel(tin.get("file_path") or tin.get("notebook_path") or "", cwd)
        if not rel.startswith("../") and any(fnmatch.fnmatch(rel, g) for g in policy.get("write", [])):
            grant(cwd, f"SDD hub bookkeeping: '{rel}'")
    elif tool == "Bash":
        cmd = (tin.get("command") or "").strip()
        if CHAINING.search(re.sub(r'"[^"$`\\]*"', '""', cmd)):
            return
        if any(re.fullmatch(p, cmd) for p in policy.get("bash", [])):
            grant(cwd, "SDD hub bookkeeping command")


def auto_approve_enabled(cwd: Path) -> bool:
    """Off switch: 'auto_approve: false' under 'permissions:' in .sdd/config.yaml."""
    try:
        text = (cwd / ".sdd" / "config.yaml").read_text(encoding="utf-8")
    except OSError:
        return True
    return not re.search(r"^\s*auto_approve\s*:\s*(false|no|off)\b", text, re.M | re.I)


def grant(cwd: Path, reason: str) -> None:
    """Approve an in-policy call so autonomous agents are not stopped by permission prompts."""
    if auto_approve_enabled(cwd):
        allow(reason)


def has_conflict_markers(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return False
    return bool(re.search(r"^<{7}( |$)", text, re.M) and re.search(r"^>{7}( |$)", text, re.M))


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    plugin_root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parent.parent).resolve()
    tool = data.get("tool_name", "")
    tin = data.get("tool_input") or {}

    if tool in READ_TOOLS:
        target = tin.get("file_path") or tin.get("path") or ""
        if target and is_within(Path(target), plugin_root):
            allow("reading SDD methodology files shipped with the plugin")
        return

    agent = (data.get("agent_type") or "").split(":")[-1]
    policy_file = plugin_root / "hooks" / "ownership.json"
    try:
        policies = json.loads(policy_file.read_text())
    except (OSError, json.JSONDecodeError):
        return
    cwd = Path(data.get("cwd") or os.getcwd())

    if not agent:
        hub_grants(policies.get("__hub__") or {}, tool, tin, cwd)
        return
    policy = policies.get(agent)
    if not policy:
        return

    if tool in WRITE_TOOLS:
        raw = tin.get("file_path") or tin.get("notebook_path") or ""
        path = Path(raw)
        if not path.is_absolute():
            path = cwd / path
        try:
            rel = os.path.relpath(path.resolve(), cwd.resolve())
        except ValueError:
            rel = str(path)
        rel = Path(rel).as_posix()
        if rel.startswith("../"):
            # From an agent worktree, SDD artifacts (specs/, .sdd/) may be written back to the main checkout.
            root = worktree_project_root(cwd)
            try:
                rel_root = Path(os.path.relpath(path.resolve(), root)).as_posix()
            except ValueError:
                rel_root = "../"
            if rel_root.startswith(("specs/", ".sdd/")):
                rel = rel_root
            else:
                deny(f"{agent} may not write outside the project ({raw}).")
        allowed = policy.get("write", [])
        excluded = [g for g in policy.get("write_except", []) if not g.startswith("!")]
        reincluded = [g[1:] for g in policy.get("write_except", []) if g.startswith("!")]
        if any(fnmatch.fnmatch(rel, g) for g in excluded) and not any(fnmatch.fnmatch(rel, g) for g in reincluded):
            deny(f"{agent} may not modify '{rel}' (owned by another agent). "
                 "File a finding routed to the artifact's owner instead.")
        if policy.get("write_if_conflicted") and has_conflict_markers(path):
            grant(cwd, f"{agent} resolving merge conflict markers in '{rel}'")
            return
        if not any(fnmatch.fnmatch(rel, g) for g in allowed):
            deny(f"{agent} does not own '{rel}'. It may write only: {', '.join(allowed)}. "
                 "File a finding routed to the artifact's owner instead.")
        grant(cwd, f"{agent} owns '{rel}'")
        return

    if tool == "Bash":
        cmd = (tin.get("command") or "").strip()
        allowed = policy.get("bash", [])
        # Double-quoted text without expansions ($, backticks, backslashes) is inert,
        # so characters like <> inside a commit message are not treated as redirection.
        unquoted = re.sub(r'"[^"$`\\]*"', '""', cmd)
        if CHAINING.search(unquoted):
            deny(f"{agent} may not chain or redirect shell commands.")
        if any(re.fullmatch(p, cmd) for p in allowed):
            grant(cwd, f"command is on {agent}'s allowlist")
            return
        purposes = policy.get("project_commands", [])
        hit = matched_purpose(cmd, purposes, project_commands(cwd)) if purposes else None
        if hit is None:
            deny(f"{agent} is not allowed to run this command. It may run the SDD commands in its policy and the "
                 f"project commands registered in the committed .sdd/commands.yaml for: {', '.join(purposes) or 'none'}. "
                 "If the project needs a new command, ask platform-engineer to register it.")
        purpose, prefix = hit
        if DANGEROUS.search(cmd):
            deny(f"'{cmd}' contains an operation that is never allowed through the project command registry.")
        if purpose == "deps-add":
            unapproved = unapproved_runtime_deps(cmd[len(prefix):], cwd)
            if unapproved:
                deny(f"runtime dependencies not approved in .sdd/dependencies.yaml: {', '.join(unapproved)}. "
                     "Return status 'blocked' with a D2 escalation to security-engineer "
                     "(or use the deps-add-dev command if it is development-only).")
        grant(cwd, f"project command ({purpose}) for {agent}")
        return

    if tool.startswith("mcp__") and policy.get("mcp") == "read-only":
        method = tool.split("__")[-1]
        if MCP_WRITE.search(method):
            deny(f"{agent} has read-only access to integrations; '{method}' looks like a write. "
                 "External writes are performed by the hub.")


if __name__ == "__main__":
    main()
