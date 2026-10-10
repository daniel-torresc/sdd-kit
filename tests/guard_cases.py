"""Guard cases: python3 tests/guard_cases.py (builds its own fixture repo in a temp folder). Expected outcomes come from the
denylist decided in docs/design-decisions.md §9: agents are approved except for irreversible actions and the human's decisions;
the hub's bookkeeping is approved and anything denylisted falls back to a prompt. A = allow, D = deny, P = passthrough (prompt)."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
FIX = Path(tempfile.mkdtemp(prefix="sdd-guard-")).resolve()
GUARD = PLUGIN / "scripts" / "guard.py"
SDD = f"uv run {PLUGIN}/skills/sdd-contracts/scripts/sdd.py"
F = "specs/001-reset"


def run(tool, tin, agent=None, cwd=FIX):
    data = {"tool_name": tool, "tool_input": tin, "cwd": str(cwd)}
    if agent:
        data["agent_type"] = f"sdd-methodology:{agent}"
    out = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(data), capture_output=True, text=True,
                         env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(PLUGIN)})
    if not out.stdout.strip():
        return "P", ""
    d = json.loads(out.stdout)["hookSpecificOutput"]
    return {"allow": "A", "deny": "D"}[d["permissionDecision"]], d["permissionDecisionReason"]


def W(path):
    return ("Write", {"file_path": str(FIX / path), "content": "x"})


def B(cmd):
    return ("Bash", {"command": cmd})


AGENT_CASES = [  # run for a few different agents: the denylist is the same for all
    ("A", W(f"{F}/design.md")), ("A", W("src/app/reset.py")), ("A", W(".sdd/stack.yaml")),
    ("A", B("uv run pytest -q")), ("A", B("uv run pytest > out.txt && uv run ruff check .")),
    ("A", B("git switch -c sdd/F001-T-02")), ("A", B("git push -u origin sdd/F001-reset")),
    ("A", B("gh pr create --draft --title Reset")),
    ("A", B("tofu plan -out plan.bin")), ("A", B("./scripts/deploy/staging.sh v1")), ("A", B("gcloud run deploy api-staging")),
    ("A", B("rm -rf build")), ("A", B("curl -s http://localhost:8000/health")), ("A", B("curl -X POST http://localhost:8000/reset")),
    ("A", B(f"{SDD} trace {F} --phase plan")),
    ("D", B("git push origin main")), ("D", B("git push origin HEAD:main")), ("D", B("git push --force origin sdd/F001-reset")),
    ("D", B("git push --force-with-lease")), ("D", B("git push origin --delete sdd/F001-T-01")), ("D", B("git push origin :sdd/F001-T-01")),
    ("D", B("git switch main && git merge sdd/F001-reset")), ("D", B('git commit -m "x"')),
    ("D", B("git merge --no-ff sdd/F001-T-01")),  # the main checkout is on main
    ("D", B("gh pr merge 1")), ("D", B("gh pr ready 1")), ("D", B("gh pr create --title Reset")), ("D", B("gh release create v1")),
    ("D", B("gh issue create --title x")), ("D", B("gh pr comment 1 --body x")),
    ("D", B("tofu apply")), ("D", B("terraform destroy")), ("D", B("gcloud run deploy api")), ("D", B("kubectl apply -f k8s/")),
    ("D", B("helm upgrade app ./chart")), ("D", B("vercel deploy --prod")),
    ("D", B("rm -rf /")), ("D", B("rm -rf ~")), ("D", B("rm -rf ..")), ("D", B("rm -rf .")), ("D", B("uv run pytest; rm -rf /")),
    ("D", B("sudo ls")), ("D", B('psql -c "DROP TABLE users"')), ("D", B("curl -X POST https://example.com/hook")),
    ("D", B("make release")),
]
HUB_CASES = [
    ("A", W(f"{F}/state.yaml")), ("A", W(f"{F}/decisions.md")), ("A", W(".sdd/stack.yaml")),
    ("A", W(".sdd/constitution.md")), ("A", W(".sdd/config.yaml")),
    ("P", W(".sdd/product.md")), ("P", W("src/app/x.py")), ("P", W(f"{F}/design.md")),
    ("A", B("git fetch")), ("A", B("git status && git log --oneline -5")), ("A", B("git -C . switch -c sdd/F002-export origin/main")),
    ("A", B("git add specs .sdd")), ("A", B(f"{SDD} trace {F} --phase plan")),
    ("A", B("git worktree remove --force .claude/worktrees/agent-abc123")),
    ("P", B("git push origin main")), ("P", B('git commit -m "chore(sdd): x"')),  # the main checkout is on main
    ("P", B("git push --force")), ("P", B("ls")), ("P", B("gh pr merge 1")),
]
AGENTS_SAMPLE = ["engineer", "architect", "tech-lead", "code-reviewer", "platform-engineer"]

EXTRA = []  # (label, expected, tool, tin, agent, cwd)
wt = FIX / ".claude" / "worktrees" / "agent-1"
OTHER = Path(tempfile.mkdtemp(prefix="not-sdd-")).resolve()
EXTRA += [
    ("engineer in worktree writes its own src", "A", "Write", {"file_path": str(wt / "src/app/reset.py")}, "engineer", wt),
    ("engineer in worktree writes back decisions.md", "A", "Write", {"file_path": str(FIX / F / "decisions.md")}, "engineer", wt),
    ("engineer in worktree writes main-checkout src", "D", "Write", {"file_path": str(FIX / "src/app/reset.py")}, "engineer", wt),
    ("engineer in worktree commits on its branch", "A", "Bash", {"command": 'git commit -m "feat: x" -m "Refs: F001:T-02"'}, "engineer", wt),
    ("tech-lead merges a task into a feature branch", "A", "Bash", {"command": "git merge --no-ff sdd/F001-T-01"}, "tech-lead", wt),
    ("hub commits on a feature branch", "A", "Bash", {"command": 'git commit -m "chore(sdd): x" -m "Refs: F001"'}, None, wt),
    ("engineer writes outside the project", "D", "Write", {"file_path": "/tmp/x.py"}, "engineer", FIX),
    ("architect MCP write", "D", "mcp__claude_ai_Linear__create_issue", {}, "architect", FIX),
    ("architect MCP read", "A", "mcp__context7__query-docs", {}, "architect", FIX),
    ("hub MCP write", "P", "mcp__claude_ai_Linear__create_issue", {}, None, FIX),
    ("hub git outside an SDD project", "P", "Bash", {"command": "git status"}, None, OTHER),
    ("anyone reads plugin files", "A", "Read", {"file_path": str(PLUGIN / "skills/sdd-contracts/templates/tasks.md")}, "engineer", FIX),
    ("unknown agent unrestricted", "P", "Write", {"file_path": str(FIX / "src/x.py")}, "some-other-agent", FIX),
]


def build_fixture():
    def sh(*cmd, cwd=FIX):
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True)
    git = ["git", "-c", "user.email=a@b", "-c", "user.name=t"]
    sh("git", "init", "-q", "-b", "main")
    (FIX / ".sdd").mkdir()
    (FIX / "src/app").mkdir(parents=True)
    config = (PLUGIN / "skills/sdd-contracts/templates/config.yaml").read_text()
    (FIX / ".sdd/config.yaml").write_text(config.replace('# - "./scripts/deploy/prod.sh"', '- "make release"'))
    template = (PLUGIN / "skills/sdd-contracts/templates/stack.yaml").read_text()
    cmds = {"test": ["uv run pytest"], "deploy-nonprod": ["./scripts/deploy/", "gcloud run deploy api-staging"]}
    body = "commands:\n" + "".join(f"  {k}:\n" + "".join(f'    - "{c}"\n' for c in v) for k, v in cmds.items())
    (FIX / ".sdd/stack.yaml").write_text(template[:template.index("commands:")] + body)
    sh(*git, "add", "-A")
    sh(*git, "commit", "-qm", "init")
    sh("git", "worktree", "add", "-q", "-b", "worktree-agent-1", ".claude/worktrees/agent-1")


def controls():
    """Checks that the harness can fail: the off switch drops approvals to prompts but keeps denials."""
    out = []
    cfg = FIX / ".sdd/config.yaml"
    text = cfg.read_text()
    cfg.write_text(text.replace("auto_approve: true", "auto_approve: false"))
    out.append(("off switch: agent write prompts", "P", run(*W("src/app/reset.py"), "engineer")[0]))
    out.append(("off switch: denial still applies", "D", run(*B("git push origin main"), "engineer")[0]))
    out.append(("off switch: hub write prompts", "P", run(*W("specs/001-reset/state.yaml"))[0]))
    cfg.write_text(text.replace('- "make release"', ""))
    out.append(("project deny list is read from config", "A", run(*B("make release"), "engineer")[0]))
    cfg.write_text(text)
    return [c for c in out if c[1] != c[2]]


def main():
    build_fixture()
    rows, fails = 0, []
    plan = [(a, AGENT_CASES) for a in AGENTS_SAMPLE] + [(None, HUB_CASES)]
    for agent, cases in plan:
        for exp, (tool, tin) in cases:
            got, why = run(tool, tin, agent)
            rows += 1
            label = tin.get("command") or Path(tin["file_path"]).relative_to(FIX).as_posix()
            if got != exp:
                fails.append((agent or "hub", tool, label, exp, got, why))
    for label, exp, tool, tin, agent, cwd in EXTRA:
        got, why = run(tool, tin, agent, cwd)
        rows += 1
        if got != exp:
            fails.append((agent or "hub", tool, label, exp, got, why))
    bad_controls = controls()
    print(f"{rows} cases, {len(fails)} mismatches; controls: {4 - len(bad_controls)}/4")
    for c in bad_controls:
        print(f"  control failed: {c[0]}: expected {c[1]}, got {c[2]}")
    for f in fails:
        print(f"  [{f[0]}] {f[1]} {f[2]!r}: expected {f[3]}, got {f[4]} — {f[5][:160]}")


if __name__ == "__main__":
    main()
