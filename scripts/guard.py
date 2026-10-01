#!/usr/bin/env python3
"""PreToolUse ownership guard for SDD agents (stdlib only).

Reads the hook input on stdin. If the call comes from an SDD agent listed in
hooks/ownership.json, denies writes outside its owned paths, shell commands
outside its allowlist, and (optionally) MCP tools that look like writes.
In-policy calls (owned writes, allowlisted commands) are approved outright so
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


RUNTIME_ADD = re.compile(r"^(?:rtk )?(uv add|npm (?:install|i|add)|pnpm add|yarn add)\s+(.*)$")
DEV_FLAGS = {"--dev", "-D", "--save-dev", "--optional", "--group", "--dev-dependency"}


def normalize_dep(token: str, npm: bool) -> str:
    name = token.strip("'\"")
    if npm:
        at = name.find("@", 1)  # keep a leading @scope
        name = name[:at] if at > 0 else name
    else:
        name = re.split(r"[\[<>=~!;@ ]", name, maxsplit=1)[0]
        name = name.replace("_", "-")
    return name.lower()


def unapproved_runtime_deps(cmd: str, cwd: Path) -> list[str]:
    """Runtime packages in an add/install command that are not approved in .sdd/dependencies.yaml."""
    m = RUNTIME_ADD.match(cmd.strip())
    if not m:
        return []
    tokens = m.group(2).split()
    if any(t in DEV_FLAGS or t.startswith("--group=") or t.startswith("--optional=") for t in tokens):
        return []
    npm = not m.group(1).startswith("uv")
    skip_next = False
    pkgs = []
    for t in tokens:
        if skip_next:
            skip_next = False
            continue
        if t.startswith("-"):
            skip_next = t in {"--directory", "--project", "--package", "--prefix", "-C"}
            continue
        pkgs.append(normalize_dep(t, npm))
    if not pkgs:
        return []
    try:
        text = (cwd / ".sdd" / "dependencies.yaml").read_text(encoding="utf-8")
    except OSError:
        text = ""
    approved = {normalize_dep(n, npm) for n in re.findall(r"^\s*-?\s*name\s*:\s*['\"]?([@\w./-]+)", text, re.M)}
    return [p for p in pkgs if p not in approved]


def config_flag(cwd: Path, name: str) -> bool:
    """True when '<name>: true' appears in .sdd/config.yaml."""
    try:
        text = (cwd / ".sdd" / "config.yaml").read_text(encoding="utf-8")
    except OSError:
        return False
    return bool(re.search(rf"^\s*{re.escape(name)}\s*:\s*(true|yes|on)\b", text, re.M | re.I))


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
            deny(f"{agent} may not write outside the project ({raw}).")
        allowed = policy.get("write", [])
        excluded = [g for g in policy.get("write_except", []) if not g.startswith("!")]
        if not config_flag(cwd, "engineer_does_platform"):
            excluded += policy.get("write_except_platform", [])
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
        if not any(re.fullmatch(p, cmd) for p in allowed):
            deny(f"{agent} is not allowed to run this command. Allowed patterns: {allowed or 'none'}.")
        if policy.get("deps_check"):
            unapproved = unapproved_runtime_deps(cmd, cwd)
            if unapproved:
                deny(f"runtime dependencies not approved in .sdd/dependencies.yaml: {', '.join(unapproved)}. "
                     "Return status 'blocked' with a D2 escalation to security-engineer "
                     "(or add it as a dev-only dependency if it is dev-only).")
        grant(cwd, f"command is on {agent}'s allowlist")
        return

    if tool.startswith("mcp__") and policy.get("mcp") == "read-only":
        method = tool.split("__")[-1]
        if MCP_WRITE.search(method):
            deny(f"{agent} has read-only access to integrations; '{method}' looks like a write. "
                 "External writes are performed by the hub.")


if __name__ == "__main__":
    main()
