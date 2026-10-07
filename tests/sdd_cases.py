"""sdd.py checks: python3 tests/sdd_cases.py (needs uv; builds its fixtures in a temp folder).
A complete clean feature, then one injected fault per traceability rule."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SDD = str(Path(__file__).resolve().parent.parent / "skills/sdd-contracts/scripts/sdd.py")
BASE = Path(tempfile.mkdtemp(prefix="sdd-trace-")).resolve()


def fm(artifact, version=1, upstream=None, owner="x"):
    up = f"upstream: [{', '.join(upstream)}]\n" if upstream else ""
    return f"---\nartifact: {artifact}\nfeature: F001\nowner: {owner}\nstatus: approved\nversion: {version}\n{up}---\n\n"


FILES = {
    "specs/001-reset/state.yaml": "feature: F001 Password reset\nclass: M\nlenses: [security]\n",
    "specs/001-reset/brief.md": fm("brief") + "# Brief\n\n## Outcome\n",
    "specs/001-reset/requirements.md": fm("requirements", 1, ["brief.md@1"]) + """# Requirements

### REQ-01: Request a reset link
When a user requests a reset, the system shall email a single-use link.
#### AC-01.1: Link is emailed
#### AC-01.2: Unknown email gets the same response

### REQ-02: Set a new password
#### AC-02.1: Valid token sets the password

### NFR-01: Reset email latency
verify: p95 under 5 s in the load test
""",
    "specs/001-reset/ux.md": fm("ux", 1, ["requirements.md@1"]) + "# UX\n\n### UX-01: Reset flow\nrefs: REQ-01, REQ-02\n",
    "specs/001-reset/design.md": fm("design", 1, ["requirements.md@1", "ux.md@1"]) + """# Design

### C-01: Reset service
refs: REQ-01, REQ-02, NFR-01

### IF-01: POST /password-resets
refs: REQ-01
""",
    "specs/001-reset/test-plan.md": fm("test-plan", 1, ["requirements.md@1", "design.md@1"]) + "# Test plan\n",
    "specs/001-reset/tasks.md": fm("tasks", 1, ["design.md@1"]) + """# Tasks

### T-01: Acceptance tests for reset
delivers: AC-01.1, AC-01.2, AC-02.1
owner: test-engineer
files: tests/acceptance/test_reset.py
stack: backend
done-when: tests fail for the right reason

### T-02: Reset request
delivers: REQ-01
depends: T-01
owner: engineer
files: src/app/reset.py
stack: backend
done-when: AC-01.* pass
reviews: security

### T-03: Set new password
delivers: REQ-02
depends: T-01, T-02
owner: engineer
files: src/app/password.py
stack: backend
done-when: AC-02.1 passes
""",
    "tests/acceptance/test_reset.py": """# F001:AC-01.1
def test_link_emailed(): pass

# F001:AC-01.2
def test_unknown_email_same_response(): pass

# F001:AC-02.1
def test_valid_token_sets_password(): pass
""",
    "junit-pass.xml": """<testsuite>
<testcase classname="tests.acceptance.test_reset" name="test_link_emailed"/>
<testcase classname="tests.acceptance.test_reset" name="test_unknown_email_same_response"/>
<testcase classname="tests.acceptance.test_reset" name="test_valid_token_sets_password"/>
</testsuite>""",
    "junit-fail.xml": """<testsuite>
<testcase classname="tests.acceptance.test_reset" name="test_link_emailed"/>
<testcase classname="tests.acceptance.test_reset" name="test_unknown_email_same_response"><failure/></testcase>
<testcase classname="tests.acceptance.test_reset" name="test_valid_token_sets_password"/>
</testsuite>""",
}


def build(dest: Path, edits=()):
    if dest.exists():
        shutil.rmtree(dest)
    for rel, text in FILES.items():
        p = dest / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    for rel, old, new in edits:
        p = dest / rel
        t = p.read_text()
        assert old in t, (rel, old)
        p.write_text(t.replace(old, new, 1))
    git = ["git", "-C", str(dest), "-c", "user.email=a@b", "-c", "user.name=t"]
    subprocess.run(git[:3] + ["init", "-q", "-b", "main"], check=True)
    subprocess.run(git + ["add", "-A"], check=True)
    subprocess.run(git + ["commit", "-qm", "base"], check=True)
    return dest


def sdd(dest, *args):
    r = subprocess.run(["uv", "run", "-q", SDD, *args], cwd=dest, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


SPEC = "specs/001-reset"
R, T = f"{SPEC}/requirements.md", f"{SPEC}/tasks.md"

# (label, edits, sdd args, expected exit, substring expected in output)
FAULTS = [
    ("REQ without AC", [(R, "#### AC-02.1: Valid token sets the password\n", "")],
     ["trace", SPEC, "--phase", "specify"], 1, "REQ-02 has no acceptance criteria"),
    ("duplicate ID", [(R, "#### AC-01.2:", "#### AC-01.1:")], ["trace", SPEC, "--phase", "specify"], 1, "duplicate ID AC-01.1"),
    ("undefined reference", [(f"{SPEC}/design.md", "refs: REQ-01\n", "refs: REQ-09\n")],
     ["trace", SPEC, "--phase", "specify"], 1, "references undefined REQ-09"),
    ("NFR without verify", [(R, "verify: p95 under 5 s in the load test\n", "")],
     ["trace", SPEC, "--phase", "specify"], 1, "NFR-01 has no 'verify:'"),
    ("withdrawn REQ still referenced", [(R, "### REQ-02: Set a new password", "### REQ-02: Set a new password [withdrawn]")],
     ["trace", SPEC, "--phase", "specify"], 1, "references withdrawn REQ-02"),
    ("REQ not in design", [(f"{SPEC}/design.md", "refs: REQ-01, REQ-02, NFR-01", "refs: REQ-01, NFR-01")],
     ["trace", SPEC, "--phase", "design"], 1, "REQ-02 is not referenced by any component"),
    ("AC not delivered", [(T, "delivers: AC-01.1, AC-01.2, AC-02.1", "delivers: AC-01.1, AC-02.1"),
                          (T, "delivers: REQ-01\n", "delivers: AC-01.1\n")],
     ["trace", SPEC, "--phase", "plan"], 1, "AC-01.2 is not covered by any task"),
    ("task missing files", [(T, "files: src/app/password.py\n", "")], ["trace", SPEC, "--phase", "plan"], 1, "T-03 is missing files"),
    ("test-first: engineer task without test task", [(T, "depends: T-01, T-02\n", "depends: T-02\n"),
                                                     (T, "delivers: AC-01.1, AC-01.2, AC-02.1", "delivers: AC-01.1, AC-01.2")],
     ["trace", SPEC, "--phase", "plan"], 1, "T-03"),
    ("dependency cycle", [(T, "depends: T-01\nowner: engineer\nfiles: src/app/reset.py", "depends: T-01, T-03\nowner: engineer\nfiles: src/app/reset.py")],
     ["trace", SPEC, "--phase", "plan"], 1, "cycle"),
    ("unknown reviewer", [(T, "reviews: security", "reviews: security, legal")], ["trace", SPEC, "--phase", "plan"], 1, "unknown reviewer 'legal'"),
    ("inactive lens warning (clean exit)", [(T, "reviews: security", "reviews: privacy")],
     ["trace", SPEC, "--phase", "plan"], 0, "requests 'privacy' review but that lens is not active"),
    ("file overlap warning (clean exit)", [(T, "files: src/app/password.py", "files: src/app/reset.py"),
                                          (T, "depends: T-01, T-02\n", "depends: T-01\n")],
     ["trace", SPEC, "--phase", "plan"], 0, "warning"),
    ("stale downstream", [(R, "version: 1", "version: 2")], ["stale", SPEC], 1, "design.md: built against requirements.md@1, current is @2"),
    ("stale blocks trace", [(R, "version: 1", "version: 2")], ["trace", SPEC, "--phase", "specify"], 1, "STALE"),
    ("AC without test", [("tests/acceptance/test_reset.py", "# F001:AC-02.1\n", "")],
     ["trace", SPEC, "--phase", "verify"], 1, "AC-02.1 has no test"),
    ("failing test in junit", [], ["trace", SPEC, "--phase", "verify", "--junit", "junit-fail.xml"], 1, "test_unknown_email_same_response did not pass"),
    ("class S skips design, checks plan", [(f"{SPEC}/state.yaml", "class: M", "class: S"),
                                           (f"{SPEC}/design.md", "refs: REQ-01, REQ-02, NFR-01", "refs: REQ-01, NFR-01"),
                                           (T, "files: src/app/password.py\n", "")],
     ["trace", SPEC, "--phase", "plan"], 1, "T-03 is missing files"),
]


def main():
    fails = []
    clean = build(BASE / "clean")
    for args, exp_code, exp_text in [
        (["trace", SPEC, "--phase", "specify"], 0, "clean through phase 'specify'"),
        (["trace", SPEC, "--phase", "design"], 0, "clean through phase 'design'"),
        (["trace", SPEC, "--phase", "plan"], 0, "clean through phase 'plan'"),
        (["trace", SPEC, "--phase", "verify", "--junit", "junit-pass.xml"], 0, "clean through phase 'verify'"),
        (["stale", SPEC], 0, "No stale artifacts"),
        (["expected-failing", SPEC], 0, "AC-01.1"),
    ]:
        code, out = sdd(clean, *args)
        if code != exp_code or exp_text not in out:
            fails.append(("clean: " + " ".join(args[:1] + args[2:]), exp_code, code, out))
    # report only on request
    if (clean / SPEC / "evidence").exists():
        fails.append(("no file written by default", 0, 1, "evidence/ exists"))
    code, out = sdd(clean, "trace", SPEC, "--phase", "verify", "--junit", "junit-pass.xml", "--report", "evidence/traceability.md")
    rep = clean / SPEC / "evidence" / "traceability.md"
    if not rep.exists() or "AC-01.1" not in rep.read_text():
        fails.append(("--report writes the matrix", 0, code, out))
    # expected-failing shrinks as implementation commits land
    git = ["git", "-C", str(clean), "-c", "user.email=a@b", "-c", "user.name=t", "commit", "-q", "--allow-empty"]
    subprocess.run(git + ["-m", "feat: reset request", "-m", "Refs: F001:T-02"], check=True)
    code, out = sdd(clean, "expected-failing", SPEC)
    if "AC-01.1" in out or "AC-02.1" not in out:
        fails.append(("expected-failing after T-02", 0, code, out))
    subprocess.run(git + ["-m", "feat: set password", "-m", "Refs: F001:T-03"], check=True)
    code, out = sdd(clean, "expected-failing", SPEC)
    if "every test must pass" not in out:
        fails.append(("expected-failing after T-03", 0, code, out))

    for label, edits, args, exp_code, exp_text in FAULTS:
        d = build(BASE / "fault", edits)
        code, out = sdd(d, *args)
        if code != exp_code or exp_text not in out:
            fails.append((label, exp_code, code, out))
    total = 6 + 2 + 2 + len(FAULTS)
    print(f"{total} checks, {len(fails)} failed")
    for label, exp, got, out in fails:
        print(f"--- {label}: expected exit {exp}, got {got}\n{out.strip()}")


if __name__ == "__main__":
    main()
