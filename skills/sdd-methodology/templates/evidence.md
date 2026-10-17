---
artifact: evidence
feature: [feature ID]
run: [n]
commit: [the feature branch commit checked]
date: [YYYY-MM-DD]
result: [pass | fail]
upstream: [requirements.md@version, design.md@version, plan.md@version]
---

# Evidence: <feature name>

> Records what the full check of a feature showed: the checks that ran and their results, which test proves each acceptance criterion, how each quality was verified, and what failed.
> It is the evidence the feature review and the human judge the feature on. It states what was observed, never what was expected.
> Each Verify run replaces this file with the next run number; earlier runs remain in the repository's history.

---

## 1. Checks

Record every check the project has, run against the feature branch at the commit in the frontmatter, using the commands the stack lists.

| Check | Command | Result | Notes |
|---|---|---|---|
| [Test suite, linter, type checker, build, …] | [Command] | [Pass / Fail] | [Failures, or None] |

### 1.1 Known Failures

List the failures that already existed when Build started, from the state record, and whether each one still fails. A known failure is not a failure of this feature, but it is reported.

- [Test or check]: [Still failing / Now passing]

---

## 2. Traceability

Show, for each requirement, the acceptance criteria that define it, what in the design and the plan covers them, and the tests that prove them.

Every acceptance criterion MUST have at least one test that names its full ID and passes. A criterion without one is a failure, recorded in section 4.

| Requirement | Acceptance criterion | Components and interfaces | Tasks | Tests | Result |
|---|---|---|---|---|---|
| [REQ-01] | [AC-01.1] | [C-01, IF-02] | [T-03] | [path::test name] | [Pass / Fail / No test] |

---

## 3. Qualities

Record how each non-functional requirement was verified, as its Verify field says.

| NFR | How it was verified | Target | Measured | Result |
|---|---|---|---|---|
| [NFR-01] | [Test, measurement, inspection, or monitoring] | [Target from the requirements] | [What was observed] | [Pass / Fail / Unverified] |

### 3.1 Unverified Qualities

For each quality that could not be verified here, state why, and the decision entry that puts it to the human.

- [NFR-nn]: [Why it could not be verified]. Decision: [H-nn]

---

## 4. What Failed

Record every failing check, acceptance criterion, and quality, with what is needed to write a fix task for it. Leave this section empty when everything passes.

### Failure 1: [What failed, in one line]

- **Concerns:** [AC-nn.m, NFR-nn, or the check]
- **Observed:** [The failure output, or what was seen]
- **Expected:** [What the requirement or the check says]
- **Likely cause:** [Where the problem seems to be, marked as an inference]
- **Lies in:** [The code / The design or the plan / The requirements]

Repeat for each failure.

---

## 5. Limits

State what this check could not cover, and why: an environment that was not available, a check that could not run, part of the feature that could not be exercised.

- [Limit, or None]

---

## 6. Maintenance Guidelines

This document records one Verify run. It is never edited after the run; the next run replaces it, with the next run number and the commit it checked.

- `result` is `pass` only when every check passes with no failure beyond the known ones, every acceptance criterion has a passing test, and every quality passes or is put to the human as unverified.
- Record what was observed. Never mark something as passing that was not run.

### Source of Truth

- This document is the canonical record of what the full check observed.
- The feature review judges the feature against the requirements, the design, and this evidence; its verdict is in its own review file.
- The requirements define the acceptance criteria and the qualities; this document never changes them.
