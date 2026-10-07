# Dispatch table

For every step: who, which mode, what to pass, which model, and what comes next. "Default" = the agent's frontmatter model. Lens rows apply only when that lens is active in `state.yaml`. Rows marked (L) apply to class L only.

## Triage (every new request)

| Step | Agent · mode | Pass | Next |
|---|---|---|---|
| Existing code? | cartographer · `investigate` | request, likely area | research note the definition agents read |
| Classify | hub | `triage_signals`, `lens_triggers` | state.yaml (class, lenses) |

## Discover / Specify

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft brief (L) | product-lead · `discover` | request, cartographer's research note | default | `intent_questions` → ask the human (≤3), re-dispatch; else review |
| Research questions | researcher · `question` / `domain` | the Q-nn | default | asking agent incorporates |
| Decided stack entry without skills | researcher · `skills` | the stack.yaml entry | default | human chooses → architect records in stack.yaml |
| Unfamiliar technology without adequate guidance | researcher · `technology-reference` | the stack.yaml entry | default | architect links the note from the entry |
| Review brief (L) | challenger · `review` | brief.md@v, round | default | revise loop |
| Draft requirements | product-lead · `specify` (S: REQ + AC only; M: brief + requirements together, with the intent check; L: requirements against the reviewed brief) | spec folder | default | review panel (for M it reviews brief and requirements together) |
| UX flows (UI) | ux-designer · `flows` (parallel with requirements) | spec folder | default | review panel |
| Review panel | challenger · `review`; test-engineer · `testability-review`; reliability-engineer · `nfr-review` (reliability); consultant · `specify-review` (active lenses) | requirements.md@v, ux.md@v, round | test-engineer: **opus** | revise loop |
| Feasibility | architect · `consult` | Q-nn IDs | default | product-lead revises if needed |
| Revise | product-lead / ux-designer · `revise` | review files | default | re-review |
| Contested or class L UI flow | ux-designer · `prototype` | flow IDs, the contested finding | default | the human and reviewers judge the prototype |
| UX question from another agent | ux-designer · `consult` | the question | default | asking agent incorporates |
| G1 (M/L) | — | G1 entry in decisions.md (product-lead) | — | approved → Design |

## Design

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Technology options (one-way door) | researcher · `options` | the decision, REQ/NFR IDs | default | architect writes the G2 entry |
| Draft design | architect · `design` | requirements@v, ux@v, research notes | default | G2 needed? → fairness review → human; else review panel |
| Lens analyses | consultant · `analysis` (active lenses, early in Design) | lens, requirements, draft design | default | findings the architect folds into design (and test-engineer into the test plan's Evaluations) |
| G2 fairness | challenger · `review` (G2 fairness) | the G2 entries in decisions.md and their research notes | default | architect revises → human |
| Review panel | challenger · `review`; security-engineer · `design-review`; reliability-engineer · `design-review`; consultant · `design-review` | design.md@v, contracts, ADRs, round | default | revise loop (security, reliability and lens findings are folded into the design's sections) |
| Revise | architect · `revise` | review files | default | re-review |
| Runtime dependencies listed in the design | security-engineer · `dependency-review` | design.md Runtime dependencies | default | verdicts in the review file before Plan |
| New infrastructure or spend in the design | platform-engineer · `env-plan` | design, stack.yaml | default | **D3**: human approves resources and cost |

## Plan

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Draft plan | tech-lead · `plan` | design@v | default | review panel |
| Test plan | test-engineer · `test-plan` | spec folder | default | — |
| Performance review (reliability) | reliability-engineer · `perf-review` | requirements, design, test-plan.md@v | default | findings → test-engineer (performance section), tech-lead (missing tasks) |
| Review panel | test-engineer · `plan-review`; architect · `plan-review`; challenger (L); consultant · `plan-review` | tasks.md@v, round | test-engineer: **opus** | tech-lead `revise` |
| Exit | hub: `sdd.py trace --phase plan` | — | — | Build |

## Build (per task)

| Step | Agent · mode | Pass | Model | Isolation | Next |
|---|---|---|---|---|---|
| Ready tasks | tech-lead · `coordinate` | state.yaml tasks | default | — | dispatch up to the parallelism limit |
| Test task | test-engineer · `test-task` | task ID, feature branch | default | **worktree** | code-reviewer `test-review` |
| Engineer task | engineer · `implement` | task ID, feature branch | **opus** if `risk: high` | own | code-reviewer `task-review` + the task's `reviews:` (in parallel) |
| Platform task | platform-engineer · `task` | task ID, feature branch | default | own | code-reviewer `task-review` + the task's `reviews:` (in parallel) |
| Dependency request | security-engineer · `dependency-review` | package, version, purpose | default | — | engineer resumes or re-plans |
| Secret request | security-engineer · `secret-review` | secret, consumer | default | — | platform-engineer wires |
| Review | code-reviewer · `test-review` / `task-review` (no handoff note) | task, branches, round, main-checkout review path | **opus** if `risk: high` | **worktree** (checks out the task branch detached) | approve → integrate; changes → fix |
| Extra reviews (the task's `reviews:`) | `ux` → ux-designer · `ux-review`; `security` → security-engineer · `code-review`; a lens name → consultant · `code-review` with that lens | task branch, main-checkout review path | default | **worktree** (ux-review runs the app from the task branch) | all approve → integrate; changes → `fix` |
| Fix | engineer · `fix` / test-engineer · `diagnose` / platform-engineer · `task` | review file | attempts 2–3: **opus** | own | code-reviewer · `re-review` |
| Integrate | tech-lead · `integrate` | approved branches | default | — | clean up agent worktree + `worktree-agent-*` branch |
| Unblock | tech-lead · `unblock` | failed task, output | default | — | as decided |
| A needed command isn't registered | the task owner files a finding to the architect → architect · `revise` registers it in `stack.yaml` `commands:` | the finding | default | — | hub commits on the feature branch; the task resumes from the updated branch |
| Refactoring enabler task | engineer · `refactor` | task ID | default | own | code-reviewer `task-review` |
| Change request or fix touching existing code | cartographer · `impact` | the change, affected area | default | — | owner revises with the impact research note |
| One-way door surfaces outside Design | architect · `g2` | the change request | default | — | fairness review → **G2** |
| Critical/major finding deferred | the deferring owner writes a risk entry in decisions.md (security findings: security-engineer · `risk-package`) | the finding | default | — | **D3** risk acceptance |

## Verify

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Feature review (M/L) | code-reviewer · `feature-review` | feature branch, main | **opus** | fixes → engineer |
| Verify | test-engineer · `verify` | spec folder, feature branch | **opus** | evidence pack, `evidence/traceability.md` |
| Security verify (security) | security-engineer · `verify` | feature branch, design Security section | default | evidence/security |
| UX review (UI) | ux-designer · `ux-review` | running app / evidence | default | findings → engineer |
| Lens verify | consultant · `verify` | evidence pack | default | findings → owners |
| Acceptance (M/L) | product-lead · `accept` | evidence pack, brief, requirements | default | findings → owners |
| Conformance (L) | architect · `conformance` | feature branch | default | findings → owners |
| Exit | hub: `sdd.py trace --phase verify --junit <evidence/junit.xml>` | — | — | Release |

## Release

| Step | Agent · mode | Pass | Model | Next |
|---|---|---|---|---|
| Release plan + rehearsal | platform-engineer · `release` | feature branch, evidence pack | **opus** | release.md, G3 entry |
| Docs | librarian · `docs` (parallel) | spec folder, docs impact in decisions.md | default | docs updated on the feature branch |
| Release review | reliability-engineer · `release-review` | release.md | default | revise loop |
| G3 | — | G3 entry in decisions.md (platform-engineer) | — | approved → merge (human) → deploy |
| Deploy | platform-engineer · `deploy` (staging soak, then production via the protected workflow) | version, environment | default | watch window |

## Evolve (after G3 or abandonment)

| Step | Agent · mode | Pass | Next |
|---|---|---|---|
| Architecture upkeep | architect · `evolve` | the feature's design, ADRs, decisions.md | `architecture.md` (structure, conventions, debt), superseded ADRs, `stack.yaml` |
| Outcome vs success metric (after the watch window) | product-lead · `evolve` | release outcome, metrics | the brief's Outcome, `product.md`; new REQs or features if needed |
| Retrospective | librarian · `retro` | spec folder | findings → owners of canonical documents; methodology proposals in decisions.md |

## Operate (`/sdd incident`)

| Step | Agent · mode | Next |
|---|---|---|
| Triage | incident-responder · `triage` | **fast-path** mitigation entry → human now |
| Diagnose (if needed) | reliability-engineer · `diagnose` / engineer · `debug` | evidence into the incident file |
| Impact of the fix (existing code) | cartographer · `impact` | research note for the fix feature |
| Investigate | incident-responder · `investigate` | — |
| Postmortem | incident-responder · `postmortem` (+ reliability-engineer · `post-incident`) | Postmortem section of the incident file, action items |
| Route actions | hub | `/sdd new` for fixes; findings and change requests to the owners of the affected documents |
| Follow-up | incident-responder · `follow-up` | incident closed |

## Adopt (`/sdd adopt`)

cartographer · `adopt` → research notes → architect `init` (`architecture.md`, `stack.yaml` with `decided-by: existing`), product-lead `init` (`product.md`, behavior baseline), test-engineer (characterization-test tasks), platform-engineer (CI gaps), ux-designer `init` (UI) → those owners do the work in the foundation feature.

## Arbiters

| Dispute category | Arbiter | If the arbiter is a party / value or risk judgment |
|---|---|---|
| Scope, value, user impact | product-lead · `arbitrate` | human |
| Architecture, design, NFR trade-off | architect · `arbitrate` | human |
| Engineering practice, process, task split | tech-lead · `arbitrate` | human |
| Security severity | security-engineer verdict stands unless architect shows the exploit scenario is invalid; otherwise human | human |
