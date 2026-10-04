# Dispatch table

For every step: who, which mode, what to pass, which model, and what comes next. "Default" model = the agent's frontmatter model.

## Discover / Specify

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft brief (M/L) | product-lead · `discover` | request text, spec folder | default | `intent_questions`? → ask the human (AskUserQuestion, ≤3), re-dispatch with answers; else review |
| Review brief | challenger · `review` (phase discover) | target brief.md@v, round | default | revise loop |
| Draft requirements | product-lead · `specify` | spec folder (S: "REQ + AC only") | default | review panel |
| Review requirements | challenger · `review` + test-engineer · `testability-review` (parallel) | target requirements.md@v, round | test-engineer: **opus** | revise loop |
| Feasibility Qs routed to architect | architect · `consult` | the Q-nn IDs | default | product-lead revises if needed |
| Revise | product-lead · `revise` | review files to answer | default | re-review (round+1) |
| G1 (M/L) | — | present `gates/G1-intent.md` (ordered by challenger risk ranking) | — | approved → Design |

## Design

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft design | architect · `design` | spec folder, approved requirements@v | default | G2 needed? → challenger fairness review → human; else review panel |
| G2 fairness | challenger · `review` (G2 fairness) | gate files + `G2-brief.md` | default | architect revises → human |
| Review design | challenger · `review` (+ security-engineer, reliability-engineer when available — see fallbacks) | design.md@v, contracts, ADRs, round | default | revise loop |
| Revise | architect · `revise` | review files | default | re-review |

## Plan

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft plan | tech-lead · `plan` | spec folder, design@v | default | review panel |
| Test plan | test-engineer · `test-plan` (parallel with plan review) | spec folder | default | — |
| Review plan | test-engineer · `plan-review` + architect · `plan-review` (+ challenger for L) | tasks.md@v, round | test-engineer: **opus** | tech-lead `revise` loop |
| Exit | hub runs `sdd.py trace --phase plan` | — | — | Build |

## Build (per task)

| Step | Agent · mode | Pass | Model | Isolation | Next |
|---|---|---|---|---|---|
| Ready tasks | tech-lead · `coordinate` | state.yaml tasks | default | — | dispatch up to the parallelism limit |
| Test task | test-engineer · `test-task` | task ID, feature branch | default | **worktree** | code-reviewer `test-review` |
| Engineer task | engineer · `implement` | task ID, feature branch (for diff coverage) | **opus** if `risk: high`, else default | own (`isolation: worktree`) | code-reviewer `task-review` |
| Review | code-reviewer · `test-review` / `task-review` | task ID, task branch, feature branch, round — no handoff note | **opus** if `risk: high` | — | approve → integrate; changes → fix |
| Fix | engineer · `fix` (or test-engineer · `diagnose`) | review file | attempts 2–3: **opus** | own | `re-review` |
| Integrate | tech-lead · `integrate` | approved task branches | default | — | remove the task worktree; next ready tasks |
| Unblock | tech-lead · `unblock` | failed task, its output | default | — | as decided |

## Verify

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Feature review (M/L) | code-reviewer · `feature-review` | feature branch, main branch | **opus** | fixes → engineer |
| Verify | test-engineer · `verify` | spec folder, feature branch | **opus** | evidence pack |
| Acceptance (M/L) | product-lead · `accept` | evidence pack, brief, requirements | default | findings → owners |
| Conformance (L) | architect · `conformance` | feature branch | default | findings → owners |
| Exit | hub: `sdd.py trace --phase verify --junit <evidence/junit.xml>` | — | — | G3 |

## Release

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Release plan + rehearsal | platform-engineer · `release` | spec folder, feature branch, evidence pack | **opus** | `release.md`, `gates/G3-production.md` |
| Review release plan | reliability-engineer (if available) else architect · `review` | release.md | default | revise loop |
| G3 | — | present `gates/G3-production.md` | — | approved → merge (human, or approved merge) |
| Deploy | platform-engineer · `deploy` (staging soak first; production via the protected workflow — the human approves in GitHub) | version, environment | default | watch window → done |

Platform tasks in `tasks.md` (`agent: platform-engineer`) are dispatched like engineer tasks (own worktree, code review, integration).

## Arbiters

| Dispute category | Arbiter | If the arbiter is a party / value or risk judgment |
|---|---|---|
| Scope, value, user impact | product-lead · `arbitrate` | human |
| Architecture, design, NFR trade-off | architect · `arbitrate` | human |
| Engineering practice, process, task split | tech-lead · `arbitrate` | human |
