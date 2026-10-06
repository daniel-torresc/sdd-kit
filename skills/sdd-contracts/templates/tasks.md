---
artifact: tasks
feature: F000
owner: tech-lead
status: draft
version: 1
upstream: [requirements.md@1, design.md@1]
---

# Tasks: <feature name>

<!--
One heading per task. Fields (machine-checked by sdd.py trace --phase plan):
  refs:       REQ/AC IDs this task delivers, or "enabler"
  depends:    task IDs that must be merged first
  agent:      engineer | test-engineer | platform-engineer
  surface:    backend | frontend | data | infra | ml | docs
  stack:      concerns from .sdd/stack.yaml this task involves (the hub loads their skills), e.g. backend-language, http-framework
  touches:    comma-separated paths or modules this task changes (conflict detection)
  done-when:  observable completion criterion (ACs passing, checks green)
  test-first: optional; "waived — <reason>" only with test-engineer agreement
  risk:       optional; "high" for security-sensitive, concurrency, data-migration or riskiest-slice work (runs on opus)
Engineer tasks must depend (directly or transitively) on test-engineer tasks covering the same ACs.
-->

## Slices
<!-- One line per vertical slice: which tasks, which ACs, why this order. -->

### T-01: Walking skeleton — <thinnest end-to-end path>
refs: enabler
depends:
agent: platform-engineer
surface: infra
stack: <technologies>
touches: <project manifest>, <app entry point>, <pipeline definition>
done-when: app starts, health check passes in CI, deploys to the dev environment

### T-02: Acceptance tests for <slice 1>
refs: AC-01.1
depends: T-01
agent: test-engineer
surface: backend
stack: <technologies>
touches: <acceptance test location for the slice>
done-when: tests exist, reference their ACs, and fail for the right reason

### T-03: Implement <slice 1>
refs: REQ-01
depends: T-02
agent: engineer
surface: backend
stack: <technologies>
touches: <module path>
done-when: AC-01.1 tests pass; lint, types and unit tests green
