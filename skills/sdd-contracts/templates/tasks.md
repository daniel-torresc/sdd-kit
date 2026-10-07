---
artifact: tasks
feature: F000
owner: tech-lead
status: draft
version: 1
upstream: [requirements.md@1, design.md@1]
---

# Tasks: <feature>

<!--
Each task is the engineer's (or test-engineer's / platform-engineer's) entry point: it says what to do,
and points to the requirements, design and contracts that say how. Fields are checked by sdd.py:

  delivers:  AC/REQ IDs that become true when the task is done, or "enabler"
  depends:   tasks that must be integrated first (optional)
  owner:     engineer | test-engineer | platform-engineer
  files:     paths or modules the task will change (detects conflicts between parallel tasks)
  stack:     stack.yaml concerns involved (the hub loads their skills)
  done-when: observable completion: named ACs passing, checks green
  reviews:   optional — extra reviewers beyond code-reviewer: ux, security, privacy, data-migration, ai-evals, finops, api-compat
  risk:      optional — "high" for security-sensitive, concurrency, data-migration or riskiest-slice work
  test-first: optional — "waived: <reason>" only with test-engineer's agreement
Every engineer task depends on a test-engineer task covering the same ACs.
-->

## Slices
<!-- One line per vertical slice: tasks, the ACs it makes observable, and why it sits in this position. -->

### T-01: Acceptance tests for <slice>
delivers: AC-01.1
owner: test-engineer
files: <acceptance test location>
stack: <stack concerns>
done-when: tests exist, reference their ACs, and fail for the right reason

Goal: <one or two sentences>.

### T-02: <what changes>
delivers: REQ-01
depends: T-01
owner: engineer
files: <module path>
stack: <stack concerns>
done-when: AC-01.x tests pass; project checks green

Goal: <one or two sentences on what this task changes and why>.
Notes: <pointers into design.md / contracts that matter for this task>.
