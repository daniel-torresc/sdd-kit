# Dispatch table

For every step: who, which mode, what to pass, which model, and what comes next. "Default" = the agent's frontmatter model. Lens rows apply only when that lens is active in `state.yaml`. Rows marked (L) apply to class L only.

## Triage (every new request)

| Step | Agent · mode | Pass | Next |
|---|---|---|---|
| Existing code? | cartographer · `context` | request, likely area | product-lead reads `context.md` |
| Classify | hub | `triage_signals`, `lens_triggers` | state.yaml (class, lenses) |

## Discover / Specify

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft brief (M/L) | product-lead · `discover` | request, context.md | default | `intent_questions` → ask the human (≤3), re-dispatch; else review |
| Research questions | researcher · `question` / `domain` | the Q-nn | default | asking agent incorporates |
| Review brief | challenger · `review` | brief.md@v, round | default | revise loop |
| Draft requirements | product-lead · `specify` (S: REQ + AC only) | spec folder | default | review panel |
| UX flows (UI) | ux-designer · `flows` (parallel with requirements) | spec folder | default | review panel |
| Review panel | challenger · `review`; test-engineer · `testability-review`; reliability-engineer · `nfr-review` (reliability); consultant · `specify-review` (active lenses) | requirements.md@v, ux.md@v, round | test-engineer: **opus** | revise loop |
| Feasibility | architect · `consult` | Q-nn IDs | default | product-lead revises if needed |
| Revise | product-lead / ux-designer · `revise` | review files | default | re-review |
| Contested or class L UI flow | ux-designer · `prototype` | flow IDs, the contested finding | default | the human and reviewers judge the prototype |
| UX question from another agent | ux-designer · `consult` | the question | default | asking agent incorporates |
| G1 (M/L) | — | gates/G1-intent.md | — | approved → Design |

## Design

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Technology options (one-way door) | researcher · `options` | the decision, REQ/NFR IDs | default | architect builds G2 |
| Draft design | architect · `design` | requirements@v, ux@v, context.md | default | G2 needed? → fairness review → human; else review panel |
| Threat model (security) | security-engineer · `threat-model` (parallel with design) | draft design, contracts | default | findings to architect / product-lead |
| SLOs and capacity (reliability) | reliability-engineer · `slo`, `capacity` | requirements, design | default | `.sdd/operations/*` |
| Lens analyses | consultant · `analysis` (active lenses) | lens, design | default | `lens-<lens>.md` / `evals.md` |
| G2 fairness | challenger · `review` (G2 fairness) | gate files + G2-brief.md | default | architect revises → human |
| Review panel | challenger · `review`; security-engineer · `design-review`; reliability-engineer · `design-review`; consultant · `design-review` | design.md@v, contracts, ADRs, threat model, round | default | revise loop |
| Revise | architect · `revise` | review files | default | re-review |
| New infrastructure or spend in the design | platform-engineer · `env-plan` | design, stack.yaml | default | **D3**: human approves resources and cost |

## Plan

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft plan | tech-lead · `plan` | design@v | default | review panel |
| Test plan | test-engineer · `test-plan` | spec folder | default | — |
| Perf plan (reliability) | reliability-engineer · `perf-plan` | requirements, design | default | test-engineer executes in Verify |
| Review panel | test-engineer · `plan-review`; architect · `plan-review`; challenger (L); consultant · `plan-review` | tasks.md@v, round | test-engineer: **opus** | tech-lead `revise` |
| Exit | hub: `sdd.py trace --phase plan` | — | — | Build |

## Build (per task)

| Step | Agent · mode | Pass | Model | Isolation | Next |
|---|---|---|---|---|---|
| Ready tasks | tech-lead · `coordinate` | state.yaml tasks | default | — | dispatch up to the parallelism limit |
| Test task | test-engineer · `test-task` | task ID, feature branch | default | **worktree** | code-reviewer `test-review` |
| Engineer task | engineer · `implement` | task ID, feature branch | **opus** if `risk: high` | own | code-reviewer `task-review` (+ security-engineer `code-review` if security lens and task is security-relevant or `risk: high`); + consultant · `code-review` for tasks in an active lens's scope (migrations, personal data, model calls, public contracts, new spend) |
| Platform task | platform-engineer · `task` | task ID, feature branch | default | own | code-reviewer `task-review` |
| Dependency request | security-engineer · `dependency-review` | package, version, purpose | default | — | engineer resumes or re-plans |
| Secret request | security-engineer · `secret-review` | secret, consumer | default | — | platform-engineer wires |
| Review | code-reviewer · `test-review` / `task-review` (no handoff note) | task, branches, round, main-checkout review path | **opus** if `risk: high` | **worktree** (checks out the task branch detached) | approve → integrate; changes → fix |
| Fix | engineer · `fix` / test-engineer · `diagnose` / platform-engineer · `task` | review file | attempts 2–3: **opus** | own | code-reviewer · `re-review` |
| Integrate | tech-lead · `integrate` | approved branches | default | — | clean up agent worktree + `worktree-agent-*` branch |
| Unblock | tech-lead · `unblock` | failed task, output | default | — | as decided |
| Registry change (`.sdd/commands.yaml` changed on a task branch) | architect · `review-commands` | task branch diff | default | — | approve → integrate; changes → platform-engineer |
| Refactoring enabler task | engineer · `refactor` | task ID | default | own | code-reviewer `task-review` |
| Change request or fix touching existing code | cartographer · `impact` | the change, affected area | default | — | owner revises with the impact analysis |
| One-way door surfaces outside Design | architect · `g2` | the change request | default | — | fairness review → **G2** |
| Critical/major finding deferred | owner prepares `gates/risk-*` (security findings: security-engineer · `risk-package`) | the finding | default | — | **D3** risk acceptance |

## Verify

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Feature review (M/L) | code-reviewer · `feature-review` | feature branch, main | **opus** | fixes → engineer |
| Verify | test-engineer · `verify` | spec folder, feature branch, perf-plan | **opus** | evidence pack |
| Security verify (security) | security-engineer · `verify` | feature branch, threat model | default | evidence/security |
| UX review (UI) | ux-designer · `ux-review` | running app / evidence | default | findings → engineer |
| Lens verify | consultant · `verify` | evidence pack | default | findings → owners |
| Acceptance (M/L) | product-lead · `accept` | evidence pack, brief, requirements | default | findings → owners |
| Conformance (L) | architect · `conformance` | feature branch | default | findings → owners |
| Exit | hub: `sdd.py trace --phase verify --junit <evidence/junit.xml>` | — | — | Release |

## Release

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Release plan + rehearsal | platform-engineer · `release` | feature branch, evidence pack | **opus** | release.md, G3 package |
| Docs | librarian · `docs` (parallel) | spec folder, contracts | default | docs updated on the feature branch |
| Release review | reliability-engineer · `release-review` | release.md | default | revise loop |
| G3 | — | gates/G3-production.md | — | approved → merge (human) → deploy |
| Deploy | platform-engineer · `deploy` (staging soak, then production via the protected workflow) | version, environment | default | watch window |

## Evolve (after G3 or abandonment)

| Step | Agent · mode | Next |
|---|---|---|
| Knowledge | librarian · `knowledge` | `.sdd/knowledge/*` |
| Architecture upkeep | architect · `evolve` | overview, conventions, debt |
| Map refresh (existing code) | cartographer · `refresh` | `.sdd/map/*` |
| Retrospective | librarian · `retro` | retro.md, lessons, MIPs |
| Outcome vs success metric (after the watch window) | product-lead · `evolve` | release outcome, metrics | brief records the outcome; new REQs or features if needed |

## Operate (`/sdd incident`)

| Step | Agent · mode | Next |
|---|---|---|
| Triage | incident-responder · `triage` | **fast-path** mitigation package → human now |
| Diagnose (if needed) | reliability-engineer · `diagnose` / engineer · `debug` | evidence into the incident |
| Impact of the fix (existing code) | cartographer · `impact` | the proposed fix | blast radius for the fix feature |
| Investigate | incident-responder · `investigate` | — |
| Postmortem | incident-responder · `postmortem` (+ reliability-engineer · `post-incident`) | action items |
| Route actions | hub | `/sdd new` for fixes; change requests; debt; lessons |
| Follow-up | incident-responder · `follow-up` | postmortem closed |

## Adopt (`/sdd adopt`)

cartographer · `adopt` → proposals to architect (overview, conventions), product-lead (behavior baseline, product context), test-engineer (characterization tests), platform-engineer (CI gaps) → those owners do the work as normal features or init steps.

## Arbiters

| Dispute category | Arbiter | If the arbiter is a party / value or risk judgment |
|---|---|---|
| Scope, value, user impact | product-lead · `arbitrate` | human |
| Architecture, design, NFR trade-off | architect · `arbitrate` | human |
| Engineering practice, process, task split | tech-lead · `arbitrate` | human |
| Security severity | security-engineer verdict stands unless architect shows the exploit scenario is invalid; otherwise human | human |
