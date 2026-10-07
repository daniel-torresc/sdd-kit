"""Guard policy cases: python3 tests/guard_cases.py (builds its own fixture repo in a temp folder). Expected outcomes come from the contracts (artifacts.md ownership
table, agent definitions), not from ownership.json. A = allow, D = deny, P = passthrough (normal prompt)."""
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


CASES = {
    "product-lead": [
        ("A", W(".sdd/product.md")), ("A", W(f"{F}/brief.md")), ("A", W(f"{F}/requirements.md")),
        ("A", W(f"{F}/decisions.md")), ("A", W(f"{F}/reviews/specify-challenger-r1-answers.md")),
        ("D", W(f"{F}/reviews/specify-challenger-r1.md")), ("A", W(f"{F}/reviews/verify-product-lead-r1.md")),
        ("D", W(f"{F}/ux.md")), ("D", W(f"{F}/design.md")), ("D", W(".sdd/stack.yaml")),
        ("D", W(f"{F}/state.yaml")), ("D", W("src/app/main.py")),
        ("A", B(f"{SDD} trace {F} --phase specify")), ("D", B("uv run pytest")),
    ],
    "challenger": [
        ("A", W(f"{F}/reviews/specify-challenger-r1.md")), ("A", W(f"{F}/reviews/second-opinion-challenger-1.md")),
        ("A", W(f"{F}/decisions.md")),
        ("D", W(f"{F}/reviews/specify-test-engineer-r1.md")), ("D", W(f"{F}/requirements.md")),
        ("A", B(f"{SDD} trace {F} --phase design")),
    ],
    "architect": [
        ("A", W(".sdd/architecture.md")), ("A", W(".sdd/stack.yaml")), ("A", W("docs/adr/ADR-0001-datastore.md")),
        ("A", W(f"{F}/design.md")), ("A", W(f"{F}/contracts/api.yaml")), ("A", W(f"{F}/contracts/events/reset.yaml")),
        ("A", W(f"{F}/research/Q-01-spike.md")), ("A", W(f"{F}/decisions.md")),
        ("D", W(f"{F}/tasks.md")), ("D", W(".sdd/product.md")), ("D", W("src/app/main.py")), ("D", W("docs/guide/reset.md")),
        ("A", B("uv run python spikes/token_ttl.py")), ("D", B("uv run python spikes/../src/app/main.py")),
        ("D", B("uv run pytest")),
    ],
    "tech-lead": [
        ("A", W(f"{F}/tasks.md")), ("A", W(f"{F}/reviews/integration-tech-lead-1.md")), ("D", W(f"{F}/reviews/plan-architect-r1.md")),
        ("D", W(f"{F}/design.md")), ("D", W("src/app/clean.py")), ("A", W("src/app/conflicted.py")),
        ("A", B('git merge --no-ff sdd/F001-T-01 -m "Merge T-01"')), ("D", B("git merge main")),
        ("A", B("git push -u origin sdd/F001-reset")), ("D", B("git push origin main")),
        ("A", B("gh pr create --draft --title Reset")), ("D", B("gh pr merge 1")),
        ("A", B("uv run pytest -q")), ("D", B("uv add requests")),
        ("A", B(f"{SDD} expected-failing {F}")), ("D", B("uv run pytest && git push origin main")),
    ],
    "test-engineer": [
        ("A", W(f"{F}/test-plan.md")), ("A", W(f"{F}/evidence/README.md")), ("A", W("tests/acceptance/test_reset.py")),
        ("A", W("tests/support/fakes.py")), ("A", W("tests/e2e/test_flow.py")),
        ("D", W("tests/unit/test_token.py")), ("D", W("tests/security/test_authz.py")), ("D", W("src/app/main.py")),
        ("D", W(f"{F}/tasks.md")),
        ("A", B("uv run pytest tests/acceptance -q")), ("A", B("uv run locust -f tests/perf/load.py")),
        ("A", B("git switch -c sdd/F001-T-01")), ("A", B('git commit -m "test: reset ACs" -m "Refs: F001:T-01"')),
        ("D", B("uv add requests")), ("D", B("git push origin sdd/F001-T-01")),
    ],
    "engineer": [
        ("A", W("src/app/reset.py")), ("A", W("tests/unit/test_token.py")), ("A", W("migrations/0001_tokens.py")),
        ("A", W("pyproject.toml")), ("A", W(f"{F}/reviews/build-code-reviewer-T-02-r1-answers.md")), ("A", W(f"{F}/decisions.md")),
        ("D", W(f"{F}/reviews/build-code-reviewer-T-02-r1.md")), ("D", W(f"{F}/reviews/design-security-engineer-r1.md")),
        ("D", W("tests/acceptance/test_reset.py")), ("D", W("tests/security/test_authz.py")), ("D", W(f"{F}/design.md")),
        ("D", W(".sdd/stack.yaml")), ("D", W("README.md")), ("D", W("docs/guide/reset.md")),
        ("D", W(".github/workflows/ci.yml")), ("D", W("Dockerfile")), ("D", W("infra/main.tf")),
        ("A", B("uv run pytest -q")), ("A", B("uv add argon2-cffi")), ("A", B("uv run ruff check .")),
        ("A", B("uv run alembic upgrade head")), ("A", B("docker build -t app .")),
        ("A", B('git commit -m "feat: reset" -m "Refs: F001:T-02"')), ("A", B("git switch -c sdd/F001-T-02")),
        ("A", B("git switch -c sdd/T-fix-typo-impl")), ("A", B("curl -s http://localhost:8000/health")),
        ("D", B("curl -s https://example.com")), ("D", B("tofu plan")), ("D", B("git push origin sdd/F001-T-02")),
        ("D", B("uv run pytest --force")), ("D", B("uv run python -c print")), ("D", B("uv run pytest > out.txt")),
        ("D", B("uv run pytest; rm -rf /")),
    ],
    "code-reviewer": [
        ("A", W(f"{F}/reviews/build-code-reviewer-T-02-r1.md")), ("A", W(f"{F}/reviews/test-code-reviewer-T-01-r1.md")),
        ("A", W(f"{F}/reviews/verify-code-reviewer-r1.md")), ("A", W(f"{F}/decisions.md")),
        ("D", W(f"{F}/reviews/plan-test-engineer-r1.md")), ("D", W("src/app/reset.py")),
        ("A", B("git switch --detach sdd/F001-T-02")), ("A", B("uv run pytest -q")), ("A", B("trivy fs .")),
        ("A", B("uv run diff-cover coverage.xml --compare-branch sdd/F001-reset")),
        ("D", B('git commit -m "fix"')), ("D", B("uv add x")),
    ],
    "platform-engineer": [
        ("A", W(".github/workflows/ci.yml")), ("A", W("Dockerfile")), ("A", W("infra/main.tf")),
        ("A", W("docs/runbooks/reset.md")), ("A", W(f"{F}/release.md")), ("A", W("pyproject.toml")),
        ("D", W("src/app/services/reset.py")), ("D", W("src/app/main.py")), ("D", W("src/main.py")), ("D", W("README.md")), ("D", W("docs/guide/x.md")),
        ("D", W("tests/acceptance/test_x.py")), ("D", W(".sdd/stack.yaml")), ("D", W(f"{F}/design.md")),
        ("A", B("tofu plan -out plan.bin")), ("D", B("tofu apply")), ("A", B("actionlint")),
        ("A", B("./scripts/deploy/staging.sh v1")), ("D", B("./scripts/deploy/../prod.sh")),
        ("A", B("gh run watch 123")), ("A", B("docker build -t app .")), ("A", B("trivy image app")),
        ("A", B("gcloud run services describe api")), ("D", B("gcloud run deploy api")),
    ],
    "security-engineer": [
        ("A", W("tests/security/test_authz.py")), ("A", W(f"{F}/evidence/security/dast.md")),
        ("A", W(f"{F}/reviews/design-security-engineer-r1.md")),
        ("D", W("src/app/reset.py")), ("D", W(f"{F}/design.md")), ("D", W(f"{F}/evidence/README.md")),
        ("A", B("trivy fs .")), ("A", B("zap-baseline.py -t http://localhost:8000")),
        ("A", B("uv run pytest tests/security")), ("D", B("uv add x")),
    ],
    "reliability-engineer": [
        ("A", W(f"{F}/evidence/reliability/load.md")), ("A", W(f"{F}/reviews/plan-reliability-engineer-r1.md")),
        ("D", W(f"{F}/test-plan.md")), ("D", W("src/app/x.py")), ("D", W(f"{F}/reviews/plan-test-engineer-r1.md")),
        ("A", W(f"{F}/reviews/plan-test-engineer-r1-answers.md")),
        ("A", B("uv run locust -f tests/perf/load.py")), ("A", B("uv run py-spy record -o p.svg")),
        ("D", B("uv add x")),
    ],
    "ux-designer": [
        ("A", W(".sdd/design-system.md")), ("A", W(f"{F}/ux.md")), ("A", W(f"{F}/prototypes/index.html")),
        ("D", W(f"{F}/requirements.md")), ("D", W("src/app/x.py")),
        ("A", B("uv run uvicorn app.main:app")), ("A", B("git switch --detach sdd/F001-T-03")), ("D", B("uv run pytest")),
    ],
    "researcher": [
        ("A", W(f"{F}/research/Q-02-token-libs.md")), ("D", W(f"{F}/design.md")), ("D", W(".sdd/stack.yaml")),
        ("A", B("git log --oneline")), ("D", B("uv run pytest")),
    ],
    "cartographer": [
        ("A", W(f"{F}/research/Q-03-current-auth.md")), ("D", W("src/app/x.py")), ("D", W(".sdd/architecture.md")),
        ("A", B("git blame src/app/main.py")), ("A", B("scc")), ("D", B("uv run pytest")),
    ],
    "librarian": [
        ("A", W("README.md")), ("A", W("docs/guide/reset.md")), ("A", W(f"{F}/reviews/retro-librarian-r1.md")),
        ("D", W("docs/adr/ADR-0002.md")), ("D", W("docs/runbooks/x.md")), ("D", W(".sdd/product.md")),
        ("A", B("git shortlog -sn")), ("D", B("uv run pytest")),
    ],
    "incident-responder": [
        ("A", W(".sdd/incidents/INC-001-login-errors.md")), ("D", W("src/app/x.py")), ("D", W("docs/runbooks/x.md")),
        ("A", B("gcloud run services describe api")), ("A", B("gh run list")), ("D", B("gcloud run deploy api")),
    ],
    "consultant": [
        ("A", W(f"{F}/reviews/design-consultant-privacy-r1.md")), ("A", W(f"{F}/decisions.md")),
        ("D", W(f"{F}/reviews/design-challenger-r1.md")), ("D", W(f"{F}/design.md")),
        ("A", B("git diff")), ("D", B("uv run pytest")),
    ],
    None: [  # the hub (main session)
        ("A", W(f"{F}/state.yaml")), ("A", W(f"{F}/decisions.md")), ("A", W(".sdd/stack.yaml")),
        ("A", W(".sdd/constitution.md")), ("A", W(".sdd/config.yaml")),
        ("P", W(".sdd/product.md")), ("P", W("src/app/x.py")),
        ("A", B("git fetch")), ("A", B("git remote")), ("A", B("git switch -c sdd/F002-export origin/main")),
        ("A", B("git switch sdd/F001-reset")), ("A", B("git branch -r --merged origin/main")),
        ("A", B("git add specs .sdd")), ("P", B("git add src")),
        ("A", B('git commit -m "chore(sdd): product-lead specify requirements" -m "Refs: F001"')),
        ("P", B('git commit -m "feat: x"')), ("P", B("git push origin main")), ("P", B("git merge sdd/F001-reset")),
        ("A", B(f"{SDD} trace {F} --phase plan")), ("A", B("git show sdd/F001-reset:specs/001-reset/state.yaml")),
        ("A", B("git worktree remove --force .claude/worktrees/agent-abc123")),
        ("A", B("git branch -D worktree-agent-abc123")), ("P", B("git branch -D sdd/F001-reset")),
        ("P", B("git status && git push")),
    ],
}

EXTRA = []  # (label, expected, tool, tin, agent, cwd)
wt = FIX / ".claude" / "worktrees" / "agent-1"
EXTRA += [
    ("engineer in worktree writes its own src", "A", "Write", {"file_path": str(wt / "src/app/reset.py")}, "engineer", wt),
    ("engineer in worktree writes back decisions.md", "A", "Write", {"file_path": str(FIX / F / "decisions.md")}, "engineer", wt),
    ("engineer in worktree writes main-checkout src", "D", "Write", {"file_path": str(FIX / "src/app/reset.py")}, "engineer", wt),
    ("code-reviewer in worktree writes main-checkout review", "A", "Write",
     {"file_path": str(FIX / F / "reviews/build-code-reviewer-T-02-r1.md")}, "code-reviewer", wt),
    ("engineer in worktree runs a command only its branch registered", "D", "Bash", {"command": "uv run evil"}, "engineer", wt),
    ("engineer runs an uncommitted registry addition", "D", "Bash", {"command": "uv run hack"}, "engineer", FIX),
    ("engineer writes outside the project", "D", "Write", {"file_path": "/tmp/x.py"}, "engineer", FIX),
    ("architect MCP write", "D", "mcp__claude_ai_Linear__create_issue", {}, "architect", FIX),
    ("architect MCP read", "P", "mcp__context7__query-docs", {}, "architect", FIX),
    ("hub MCP write", "P", "mcp__claude_ai_Linear__create_issue", {}, None, FIX),
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
    (FIX / ".sdd/config.yaml").write_text((PLUGIN / "skills/sdd-contracts/templates/config.yaml").read_text())
    template = (PLUGIN / "skills/sdd-contracts/templates/stack.yaml").read_text()
    cmds = {"install": ["uv sync"], "deps-add": ["uv add"], "deps-add-dev": ["uv add --dev"], "deps-remove": ["uv remove"],
            "format": ["uv run ruff format"], "lint": ["uv run ruff check"], "typecheck": ["uv run mypy"], "test": ["uv run pytest"],
            "coverage": ["uv run diff-cover"], "contract-test": ["uv run schemathesis"], "e2e": ["uv run pytest tests/e2e"],
            "mutation": ["uv run mutmut"], "perf": ["uv run locust"], "profile": ["uv run py-spy"], "migrate": ["uv run alembic"],
            "run": ["uv run uvicorn"], "build": ["docker build"], "scan": ["trivy", "gitleaks"], "pipeline-lint": ["actionlint"],
            "infra-plan": ["tofu plan"], "deploy-nonprod": ["./scripts/deploy/"], "cloud-read": ["gcloud run services describe"],
            "dast": ["zap-baseline.py"], "spike": ["uv run python spikes/"]}
    body = "commands:\n" + "".join(f"  {k}:\n" + "".join(f'    - "{c}"\n' for c in v) for k, v in cmds.items())
    (FIX / ".sdd/stack.yaml").write_text(template[:template.index("commands:")] + body)
    (FIX / "src/app/clean.py").write_text("x = 1\n")
    (FIX / "src/app/conflicted.py").write_text("<<<<<<< HEAD\nx = 1\n=======\nx = 2\n>>>>>>> sdd/F001-T-02\n")
    sh(*git, "add", "-A")
    sh(*git, "commit", "-qm", "init")
    # An agent worktree whose own branch registers an extra command (must not take effect).
    sh("git", "worktree", "add", "-q", "-b", "worktree-agent-1", ".claude/worktrees/agent-1")
    wt = FIX / ".claude/worktrees/agent-1"
    (wt / ".sdd/stack.yaml").write_text((wt / ".sdd/stack.yaml").read_text().replace("  test:\n", '  test:\n    - "uv run evil"\n'))
    sh(*git, "commit", "-qam", "self-grant", cwd=wt)
    # An uncommitted registry addition on the main checkout (must not take effect).
    (FIX / ".sdd/stack.yaml").write_text((FIX / ".sdd/stack.yaml").read_text().replace("  test:\n", '  test:\n    - "uv run hack"\n'))


def controls():
    """Checks that the harness can fail: a committed command is allowed; the off switch drops to prompts."""
    out = []
    subprocess.run(["git", "-c", "user.email=a@b", "-c", "user.name=t", "commit", "-qam", "register hack"], cwd=FIX, check=True)
    out.append(("committed command allowed", "A", run("Bash", {"command": "uv run hack"}, "engineer")[0]))
    cfg = FIX / ".sdd/config.yaml"
    text = cfg.read_text()
    cfg.write_text(text.replace("auto_approve: true", "auto_approve: false"))
    out.append(("off switch: owned write prompts", "P", run(*W("src/app/reset.py"), "engineer")[0]))
    out.append(("off switch: foreign write still denied", "D", run(*W(".sdd/stack.yaml"), "engineer")[0]))
    out.append(("off switch: hub write prompts", "P", run(*W("specs/001-reset/state.yaml"))[0]))
    cfg.write_text(text)
    return [c for c in out if c[1] != c[2]]


def main():
    build_fixture()
    rows, fails = 0, []
    for agent, cases in CASES.items():
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
