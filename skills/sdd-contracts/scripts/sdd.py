#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""SDD traceability and staleness checker.

Usage:
  sdd.py trace <spec-dir> [--phase specify|design|plan|verify] [--junit FILE ...] [--root DIR] [--no-write]
  sdd.py stale <spec-dir>

Conventions are defined in skills/sdd-contracts/references/artifacts.md.
Exit codes: 0 clean, 1 violations, 2 usage/input error.
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

PHASES = ["specify", "design", "plan", "verify"]
ARTIFACT_FILES = [
    "brief.md", "requirements.md", "ux.md", "design.md",
    "threat-model.md", "tasks.md", "test-plan.md", "release.md",
]
LOCAL_ID = r"(?:REQ|NFR|UX|C|IF|THR|T|Q|ASM|RISK)-\d+|AC-\d+\.\d+"
HEADING_RE = re.compile(rf"^(#{{2,4}})\s+({LOCAL_ID})\b[:\s]*(.*)$")
FIELD_RE = re.compile(r"^\s*(refs|depends|verify|surface|stack|agent|touches|done-when|test-first)\s*:\s*(.*)$", re.I)
TASK_REQUIRED = ["agent", "surface", "stack", "touches", "done-when"]
ID_TOKEN_RE = re.compile(rf"\b(?:{LOCAL_ID})\b")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
TEST_FILE_RE = re.compile(
    r"(^test_.*\.py$|.*_test\.py$|.*\.(test|spec)\.[cm]?[jt]sx?$|.*_test\.go$|.*Test\.(java|kt)$|.*\.feature$)"
)
SKIP_DIRS = {".git", ".claude", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", ".tox", ".mypy_cache", ".pytest_cache"}


@dataclass
class Item:
    id: str
    title: str
    file: str
    withdrawn: bool = False
    refs: list[str] = field(default_factory=list)
    depends: list[str] = field(default_factory=list)
    verify: str = ""
    enabler: bool = False
    fields: dict[str, str] = field(default_factory=dict)


@dataclass
class Model:
    feature: str
    items: dict[str, Item] = field(default_factory=dict)
    duplicates: list[tuple[str, str, str]] = field(default_factory=list)
    frontmatter: dict[str, dict] = field(default_factory=dict)

    def active(self, prefix: str) -> list[Item]:
        return [i for i in self.items.values() if i.id.startswith(prefix + "-") and not i.withdrawn]


# ---------------------------------------------------------------- parsing

def feature_id(spec_dir: Path) -> str:
    m = re.match(r"(\d+)", spec_dir.name)
    if not m:
        sys.exit(f"error: spec folder '{spec_dir.name}' must start with a number (NNN-slug)")
    return f"F{int(m.group(1)):03d}"


def read_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def feature_class(spec_dir: Path) -> str | None:
    state = spec_dir / "state.yaml"
    if not state.exists():
        return None
    try:
        return str((yaml.safe_load(state.read_text(encoding="utf-8")) or {}).get("class", "")).upper() or None
    except yaml.YAMLError:
        return None


def split_ids(value: str) -> list[str]:
    return ID_TOKEN_RE.findall(value)


def parse_artifact(path: Path, model: Model) -> None:
    text = path.read_text(encoding="utf-8")
    model.frontmatter[path.name] = read_frontmatter(text)
    body = FRONTMATTER_RE.sub("", text, count=1)
    body = COMMENT_RE.sub("", body)
    current: Item | None = None
    level = 0
    in_fence = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        h = HEADING_RE.match(line)
        if h:
            hashes, item_id, title = h.groups()
            withdrawn = "[withdrawn]" in title.lower()
            item = Item(item_id, title.replace("[withdrawn]", "").strip(), path.name, withdrawn)
            if item_id in model.items:
                model.duplicates.append((item_id, model.items[item_id].file, path.name))
            else:
                model.items[item_id] = item
            current, level = item, len(hashes)
            continue
        if line.startswith("#"):
            depth = len(line) - len(line.lstrip("#"))
            if current and depth <= level:
                current = None
            continue
        if not current:
            continue
        f = FIELD_RE.match(line)
        if not f:
            continue
        key, value = f.group(1).lower(), f.group(2).strip()
        if key == "refs":
            if value.lower() == "enabler":
                current.enabler = True
            current.refs += split_ids(value)
        elif key == "depends":
            current.depends += split_ids(value)
        elif key == "verify":
            current.verify = value
        if value:
            current.fields[key] = value


def load_model(spec_dir: Path) -> Model:
    model = Model(feature_id(spec_dir))
    for name in ARTIFACT_FILES:
        p = spec_dir / name
        if p.exists():
            parse_artifact(p, model)
    return model


def scan_tests(root: Path, feature: str) -> dict[str, list[str]]:
    """Map local IDs (AC-/NFR-) to test locations referencing '<feature>:<ID>'."""
    ref_re = re.compile(rf"\b{feature}:((?:AC-\d+\.\d+)|(?:NFR-\d+))\b")
    py_def = re.compile(r"^\s*(?:async\s+)?def\s+(test\w*)")
    found: dict[str, list[str]] = {}
    for path in root.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if not TEST_FILE_RE.match(path.name):
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(root).as_posix()
        for n, line in enumerate(lines):
            for local in ref_re.findall(line):
                loc = f"{rel}:{n + 1}"
                if path.suffix == ".py":
                    # The marker belongs to the next def/class below it, however many
                    # decorator or parametrize lines sit in between.
                    for nxt in lines[n + 1:]:
                        if re.match(r"^\s*(async\s+def|def|class)\s", nxt):
                            m = py_def.match(nxt)
                            if m:
                                loc = f"{rel}::{m.group(1)}"
                            break
                found.setdefault(local, [])
                if loc not in found[local]:
                    found[local].append(loc)
    return found


Junit = dict[tuple[str, str], bool]


def junit_results(files: list[Path]) -> Junit:
    """Map (classname, test function name) -> passed (all parametrized cases must pass)."""
    results: Junit = {}
    for f in files:
        try:
            tree = ET.parse(f)
        except (ET.ParseError, OSError) as e:
            sys.exit(f"error: cannot read junit file {f}: {e}")
        for tc in tree.iter("testcase"):
            key = (tc.get("classname", ""), re.sub(r"\[.*\]$", "", tc.get("name", "")))
            failed = any(tc.find(tag) is not None for tag in ("failure", "error", "skipped"))
            results[key] = results.get(key, True) and not failed
    return results


def junit_status(junit: Junit, loc: str) -> bool | None:
    """Result for a 'path/to/test_x.py::test_fn' location: True/False, or None if not in the report."""
    if "::" not in loc:
        return None
    path, fn = loc.split("::", 1)
    module = path[:-3].replace("/", ".") if path.endswith(".py") else path.replace("/", ".")
    hits = [ok for (cls, name), ok in junit.items()
            if name == fn and (cls == module or cls.startswith(module + ".") or module.endswith("." + cls) or cls.endswith("." + module))]
    if not hits:
        return None
    return all(hits)


def commits_by_task(root: Path, feature: str) -> dict[str, int]:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "log", "--format=%B%x00"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    counts: dict[str, int] = {}
    trailer = re.compile(r"^Refs:\s*(.*)$", re.M)
    for msg in out.split("\x00"):
        for line in trailer.findall(msg):
            for t in re.findall(rf"\b{feature}:(T-\d+)\b", line):
                counts[t] = counts.get(t, 0) + 1
    return counts


# ---------------------------------------------------------------- staleness

def stale_artifacts(spec_dir: Path, model: Model) -> list[str]:
    versions = {name: fm.get("version") for name, fm in model.frontmatter.items()}
    problems = []
    for name, fm in model.frontmatter.items():
        for up in fm.get("upstream") or []:
            m = re.match(r"^\s*([\w.\-/]+)@(\d+)\s*$", str(up))
            if not m:
                problems.append(f"{name}: malformed upstream entry '{up}' (expected file.md@N)")
                continue
            up_name, up_ver = m.group(1), int(m.group(2))
            current = versions.get(up_name)
            if current is None:
                if not (spec_dir / up_name).exists():
                    problems.append(f"{name}: upstream '{up_name}' does not exist")
                continue
            if isinstance(current, int) and current > up_ver:
                problems.append(f"{name}: built against {up_name}@{up_ver}, current is @{current} → STALE")
    return problems


# ---------------------------------------------------------------- checks

def find_cycle(tasks: list[Item]) -> list[str] | None:
    graph = {t.id: [d for d in t.depends] for t in tasks}
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(n: str) -> list[str] | None:
        state[n] = 1
        stack.append(n)
        for d in graph.get(n, []):
            if state.get(d) == 1:
                return stack[stack.index(d):] + [d]
            if state.get(d) is None and d in graph:
                c = visit(d)
                if c:
                    return c
        stack.pop()
        state[n] = 2
        return None

    for n in graph:
        if state.get(n) is None:
            c = visit(n)
            if c:
                return c
    return None


def expand_acs(model: Model, refs: list[str]) -> set[str]:
    """AC IDs covered by a list of refs (a REQ covers all of its ACs)."""
    acs = {a.id for a in model.active("AC")}
    out: set[str] = set()
    for r in refs:
        if r.startswith("AC-") and r in acs:
            out.add(r)
        elif r.startswith("REQ-"):
            n = r.split("-")[1]
            out |= {a for a in acs if a.startswith(f"AC-{n}.")}
    return out


def ancestors(tasks: list[Item], task_id: str) -> set[str]:
    graph = {t.id: t.depends for t in tasks}
    seen: set[str] = set()
    stack = list(graph.get(task_id, []))
    while stack:
        n = stack.pop()
        if n not in seen:
            seen.add(n)
            stack += graph.get(n, [])
    return seen


def test_first_violations(model: Model, tasks: list[Item]) -> list[str]:
    """Engineer tasks must depend (transitively) on test-engineer tasks covering the same ACs."""
    out = []
    by_id = {t.id: t for t in tasks}
    for t in tasks:
        if t.fields.get("agent", "").strip().lower() != "engineer" or t.enabler:
            continue
        if t.fields.get("test-first", "").lower().startswith("waived"):
            continue
        needed = expand_acs(model, t.refs)
        covered: set[str] = set()
        for a in ancestors(tasks, t.id):
            dep = by_id.get(a)
            if dep and dep.fields.get("agent", "").strip().lower() == "test-engineer":
                covered |= expand_acs(model, dep.refs)
        gap = sorted(needed - covered)
        if gap:
            out.append(f"{t.id} implements {', '.join(gap)} without a preceding test-engineer task "
                       "(add one to 'depends', or 'test-first: waived — <reason>')")
    return out


def parse_touches(value: str) -> list[str]:
    return [x.strip().strip("`").rstrip("/") for x in value.split(",") if x.strip()]


def touches_overlap(a: list[str], b: list[str]) -> list[str]:
    hits = []
    for x in a:
        for y in b:
            if x == y or x.startswith(y + "/") or y.startswith(x + "/") \
                    or fnmatch.fnmatch(x, y) or fnmatch.fnmatch(y, x):
                hits.append(x if len(x) >= len(y) else y)
    return sorted(set(hits))


def conflict_warnings(tasks: list[Item]) -> list[str]:
    """Tasks that can run in parallel (no dependency path) but touch overlapping paths."""
    anc = {t.id: ancestors(tasks, t.id) for t in tasks}
    out = []
    for i, a in enumerate(tasks):
        for b in tasks[i + 1:]:
            if a.id in anc[b.id] or b.id in anc[a.id]:
                continue
            hits = touches_overlap(parse_touches(a.fields.get("touches", "")), parse_touches(b.fields.get("touches", "")))
            if hits:
                out.append(f"{a.id} and {b.id} can run in parallel but both touch {', '.join(hits)} "
                           "(add a dependency or accept merge-order risk)")
    return out


def check(model: Model, phase: str, tests: dict[str, list[str]], junit: Junit | None,
          stale: list[str], lightweight: bool = False) -> list[tuple[str, str]]:
    """Return (phase, message) violations applicable up to and including `phase`."""
    upto = PHASES[: PHASES.index(phase) + 1]
    v: list[tuple[str, str]] = []
    items = model.items
    reqs, nfrs = model.active("REQ"), model.active("NFR")
    acs = model.active("AC")
    comps = model.active("C") + model.active("IF")
    tasks = model.active("T")

    # always
    for i, a, b in model.duplicates:
        v.append(("specify", f"duplicate ID {i} (in {a} and {b})"))
    for item in items.values():
        for r in item.refs + item.depends:
            if r not in items:
                v.append(("specify", f"{item.id} ({item.file}) references undefined {r}"))
            elif items[r].withdrawn and not item.withdrawn:
                v.append(("specify", f"{item.id} references withdrawn {r}"))
    for s in stale:
        v.append(("specify", s))

    # specify
    if not reqs:
        v.append(("specify", "requirements.md defines no REQ"))
    for req in reqs:
        n = req.id.split("-")[1]
        if not any(ac.id.startswith(f"AC-{n}.") for ac in acs):
            v.append(("specify", f"{req.id} has no acceptance criteria"))
    for ac in acs:
        parent = f"REQ-{ac.id[3:].split('.')[0]}"
        if parent not in items:
            v.append(("specify", f"{ac.id} has no parent {parent}"))
    for nfr in nfrs:
        if not nfr.verify and nfr.id not in tests:
            v.append(("specify", f"{nfr.id} has no 'verify:' line and no test"))

    # design
    referenced = {r for c in comps for r in c.refs}
    if not comps:
        v.append(("design", "design.md defines no C-/IF- items"))
    for x in reqs + nfrs:
        if x.id not in referenced:
            v.append(("design", f"{x.id} is not referenced by any component or interface"))

    # plan
    covered: set[str] = set()
    for t in tasks:
        if not t.refs and not t.enabler:
            v.append(("plan", f"{t.id} has no refs (use 'refs: enabler' for enabling work)"))
        for r in t.refs:
            covered.add(r)
    if not tasks:
        v.append(("plan", "tasks.md defines no tasks"))
    for ac in acs:
        parent = f"REQ-{ac.id[3:].split('.')[0]}"
        if ac.id not in covered and parent not in covered:
            v.append(("plan", f"{ac.id} is not covered by any task"))
    for t in tasks:
        missing = [f for f in TASK_REQUIRED if not t.fields.get(f)]
        if missing:
            v.append(("plan", f"{t.id} is missing {', '.join(missing)}"))
    v += [("plan", m) for m in test_first_violations(model, tasks)]
    cycle = find_cycle(tasks)
    if cycle:
        v.append(("plan", "task dependency cycle: " + " → ".join(cycle)))

    # verify
    for ac in acs:
        locs = tests.get(ac.id, [])
        if not locs:
            v.append(("verify", f"{ac.id} has no test referencing {model.feature}:{ac.id}"))
        elif junit is not None:
            for loc in locs:
                if "::" not in loc:
                    v.append(("verify", f"{ac.id}: reference at {loc} could not be mapped to a test function"))
                    continue
                status = junit_status(junit, loc)
                if status is None:
                    v.append(("verify", f"{ac.id}: test {loc} not found in junit results"))
                elif not status:
                    v.append(("verify", f"{ac.id}: test {loc} did not pass"))

    if lightweight:  # class T/S: no design or plan artifacts by definition
        upto = [p for p in upto if p not in ("design", "plan")]
    if junit is not None:
        for nfr in nfrs:
            for loc in tests.get(nfr.id, []):
                status = junit_status(junit, loc) if "::" in loc else None
                if "::" not in loc:
                    v.append(("verify", f"{nfr.id}: reference at {loc} could not be mapped to a test function"))
                elif status is None:
                    v.append(("verify", f"{nfr.id}: test {loc} not found in junit results"))
                elif not status:
                    v.append(("verify", f"{nfr.id}: test {loc} did not pass"))

    return [(p, m) for p, m in v if p in upto]


# ---------------------------------------------------------------- report

def render(model: Model, tests: dict[str, list[str]], junit: Junit | None,
           commits: dict[str, int], violations: list[tuple[str, str]], phase: str) -> str:
    items = model.items
    comps = model.active("C") + model.active("IF")
    tasks = model.active("T")

    def refs_to(target: str, pool: list[Item]) -> str:
        return ", ".join(i.id for i in pool if target in i.refs) or "—"

    def test_status(ac_id: str) -> str:
        locs = tests.get(ac_id, [])
        if not locs:
            return "❌ none"
        if junit is None:
            return f"{len(locs)} (not run)"
        ok = all(junit_status(junit, l) is True for l in locs)
        return f"{len(locs)} {'✅' if ok else '❌'}"

    out = [
        "<!-- GENERATED by sdd.py trace — do not edit -->",
        f"# Traceability: {model.feature}",
        "",
        f"Generated {date.today().isoformat()} · checked through phase **{phase}** · "
        f"**{'CLEAN' if not violations else f'{len(violations)} violation(s)'}**",
        "",
        "## Requirements",
        "",
        "| Requirement | Acceptance criteria | Components / interfaces | Tasks |",
        "|---|---|---|---|",
    ]
    for req in model.active("REQ"):
        n = req.id.split("-")[1]
        acs = [a.id for a in model.active("AC") if a.id.startswith(f"AC-{n}.")]
        tk = {t.id for t in tasks if req.id in t.refs or any(a in t.refs for a in acs)}
        out.append(f"| {req.id} {req.title} | {', '.join(acs) or '—'} | {refs_to(req.id, comps)} | {', '.join(sorted(tk)) or '—'} |")

    out += ["", "## Acceptance criteria → tests", "", "| AC | Tests | Status |", "|---|---|---|"]
    for ac in model.active("AC"):
        locs = "<br>".join(f"`{l}`" for l in tests.get(ac.id, [])) or "—"
        out.append(f"| {ac.id} {ac.title} | {locs} | {test_status(ac.id)} |")

    nfrs = model.active("NFR")
    if nfrs:
        out += ["", "## Non-functional requirements", "", "| NFR | Verify | Components | Tests |", "|---|---|---|---|"]
        for n in nfrs:
            out.append(f"| {n.id} {n.title} | {n.verify or '—'} | {refs_to(n.id, comps)} | {len(tests.get(n.id, []))} |")

    if tasks:
        out += ["", "## Tasks", "", "| Task | Refs | Depends | Commits |", "|---|---|---|---|"]
        for t in tasks:
            refs = "enabler" if t.enabler and not t.refs else ", ".join(t.refs) or "—"
            out.append(f"| {t.id} {t.title} | {refs} | {', '.join(t.depends) or '—'} | {commits.get(t.id, 0)} |")

    withdrawn = [i.id for i in items.values() if i.withdrawn]
    if withdrawn:
        out += ["", f"Withdrawn: {', '.join(withdrawn)}"]

    warnings = conflict_warnings(tasks)
    if warnings:
        out += ["", "## Warnings (non-blocking)", ""] + [f"- {w}" for w in warnings]
    out += ["", "## Violations", ""]
    out += [f"- **[{p}]** {m}" for p, m in violations] or ["None."]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- cli

def find_root(start: Path) -> Path:
    for p in [start, *start.parents]:
        if (p / ".git").exists() or (p / ".sdd").exists():
            return p
    return start


def main() -> int:
    ap = argparse.ArgumentParser(prog="sdd.py", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("trace", help="validate traceability and write trace.md")
    t.add_argument("spec_dir", type=Path)
    t.add_argument("--phase", choices=PHASES, default="verify")
    t.add_argument("--junit", type=Path, nargs="*", help="junit XML report(s) to check test results")
    t.add_argument("--root", type=Path, help="project root to scan for tests (default: git root)")
    t.add_argument("--no-write", action="store_true", help="do not write trace.md")
    s = sub.add_parser("stale", help="report artifacts whose upstream versions moved")
    s.add_argument("spec_dir", type=Path)
    args = ap.parse_args()

    spec_dir: Path = args.spec_dir.resolve()
    if not spec_dir.is_dir():
        print(f"error: {spec_dir} is not a directory", file=sys.stderr)
        return 2
    model = load_model(spec_dir)
    stale = stale_artifacts(spec_dir, model)

    if args.cmd == "stale":
        print("\n".join(stale) if stale else "No stale artifacts.")
        return 1 if stale else 0

    root = (args.root or find_root(spec_dir)).resolve()
    tests = scan_tests(root, model.feature)
    junit = junit_results(args.junit) if args.junit else None
    commits = commits_by_task(root, model.feature)
    violations = check(model, args.phase, tests, junit, stale, lightweight=feature_class(spec_dir) in ("T", "S"))
    report = render(model, tests, junit, commits, violations, args.phase)
    if not args.no_write:
        (spec_dir / "trace.md").write_text(report, encoding="utf-8")
    if model.active("T") and PHASES.index(args.phase) >= PHASES.index("plan"):
        for w in conflict_warnings(model.active("T")):
            print(f"  warning: {w}")
    if violations:
        print(f"{model.feature}: {len(violations)} violation(s) through phase '{args.phase}':")
        for p, m in violations:
            print(f"  [{p}] {m}")
        return 1
    print(f"{model.feature}: clean through phase '{args.phase}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
