# Dispatch table

For every step: who, which mode, what the handoff must cover, and what comes next. Every dispatch is a natural-language handoff: the "Handoff covers" column lists what it must include, as file paths where the content lives in a file. Lens rows apply only when that lens is active in `state.yaml`. Which phases run per class: the "Phases per class" table in the workflow contract.

## Triage (every new request)

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Classify | hub | `triage_signals`, `lens_triggers` | class, lenses |
| Class T | hub opens `sdd/T-<slug>` → engineer · `implement` / `debug` (the request as the task) → code-reviewer · `task-review` (review in its envelope) → tech-lead · `integrate` (push, draft PR with the verdict) | the request in the human's words | stop: the human merges the PR |
| Open the feature (S/M/L) | hub opens `sdd/F<NNN>-<slug>`, `state.yaml` and `decisions.md` | — | — |
| Existing code? (S/M/L) | cartographer · `investigate` | the request, the likely area | research note the definition agents read |

## Discover (S/M/L)

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Question round | product-lead · `discover` | the request in the human's words, the cartographer's note, the Discover questions answered so far (`decisions.md`) | questions → the hub asks the human and records the answers word for word → next round; no open questions → brief |
| Research questions | researcher · `question` / `domain` | the Q-nn and who asked it | the asking agent incorporates |
| Brief | product-lead · `discover` (same mode; it drafts once no questions are open) | as above | brief approval entry → the human |
| Brief approval | — | the brief approval entry in `decisions.md` | approved → Specify; changes → product-lead revises |

## Specify

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Draft requirements | product-lead · `specify` (S: REQ + AC only) | the approved brief, what the human said at the brief approval | G1 entry |
| UX flows (UI) | ux-designer · `flows` (in parallel with requirements) | the approved brief, the cartographer's note on the existing UI | product-lead adopts or rejects its proposed ACs |
| Feasibility | architect · `consult` | the Q-nn IDs | product-lead revises if needed |
| UX question from another agent | ux-designer · `consult` | the question | the asking agent incorporates |
| Contested flow, or class L UI | ux-designer · `prototype` | the flow IDs, what is contested | the human judges the prototype at G1 |
| G1 | — | the G1 entry in `decisions.md` (product-lead) | approved → Design; changes → product-lead / ux-designer `revise` |

## Design

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Technology options (one-way door) | researcher · `options` | the decision, the REQ/NFR IDs, `stack.yaml` constraints | architect writes the G2 entry |
| Lens analyses | consultant · `analysis` (active lenses, early in Design) | the lens, the requirements, the draft design | findings the architect folds into the design; findings for the test plan (e.g. evaluations) are held and passed to test-engineer · `test-plan` in Plan |
| Draft design | architect · `design` | requirements@v, ux@v, research notes, `stack.yaml`, the human's G1 decisions | G2 needed? → fairness review → the human; else design review |
| G2 fairness | challenger · `review` (G2 fairness) | the G2 entries in `decisions.md` and their research notes | architect revises → the human |
| Design review | challenger · `review`; security-engineer · `design-review` (security); reliability-engineer · `design-review` (reliability); consultant · `design-review` (active lenses) | design.md@v, contracts, ADRs, the requirements it answers, round | architect `revise` (up to 3 rounds; security, reliability and lens findings are folded into the design's sections) |
| Runtime dependencies listed in the design | security-engineer · `dependency-review` | the design's Runtime dependencies section | verdicts in its review file, before Plan |
| New infrastructure or spend in the design | platform-engineer · `env-plan` | the design, `stack.yaml` | **D3**: the human approves resources and cost |

## Plan

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Test plan (first; M/L) | test-engineer · `test-plan` | the spec folder, held lens findings for the test plan | untestable ACs → change requests to product-lead; then tasks |
| Performance profiles (reliability) | reliability-engineer · `perf-review` | requirements, design, test-plan.md@v | findings → test-engineer (performance section), tech-lead (missing tasks) |
| Draft plan | tech-lead · `plan` (S: short plan) | design@v, test-plan@v, the security-engineer's dependency verdicts | exit check |
| Exit | hub: `sdd.py trace --phase plan` (advisory: violations go to tech-lead as findings) | — | Build |

## Build (per task)

| Step | Agent · mode | Handoff covers | Isolation | Next |
|---|---|---|---|---|
| Ready tasks | tech-lead · `coordinate` | the tasks in `state.yaml` | — | dispatch up to the parallel limit |
| Test task | test-engineer · `test-task` | the task ID, the feature branch | **worktree** | code-reviewer `test-review` |
| Engineer task | engineer · `implement` | the task ID, the feature branch, what earlier tasks changed | own | code-reviewer `task-review` + the task's `reviews:` (in parallel) |
| Platform task | platform-engineer · `task` | the task ID, the feature branch | own | code-reviewer `task-review` + the task's `reviews:` (in parallel) |
| Refactoring enabler task | engineer · `refactor` | the task ID | own | code-reviewer `task-review` |
| Review | code-reviewer · `test-review` / `task-review` (never the author's handoff note) | the task, the branches, the main-checkout review path | **worktree** (checks out the task branch detached) | approve → integrate; changes → fix |
| Extra reviews (the task's `reviews:`, active lenses only) | `ux` → ux-designer · `ux-review`; `security` → security-engineer · `code-review`; a lens name → consultant · `code-review` with that lens | the task branch, the main-checkout review path | **worktree** (ux-review runs the app from the task branch) | all approve → integrate; changes → fix |
| Fix | engineer · `fix` / test-engineer · `diagnose` / platform-engineer · `task` | the review file | own | integrate; a code-reviewer · `re-review` only for a critical finding |
| Integrate | tech-lead · `integrate` (green = all tests pass except `sdd.py expected-failing`) | the approved branches | — | clean up the agent worktree and its `worktree-agent-*` branch |
| Unblock | tech-lead · `unblock` | the failed task, the output, the attempts made | — | as decided |
| Dependency request | security-engineer · `dependency-review` | the package, version, purpose | — | the engineer resumes or re-plans |
| Secret request | security-engineer · `secret-review` | the secret, its consumer | — | platform-engineer wires it |
| A new standard command | the task owner files a finding to the architect → architect · `revise` records it in `stack.yaml` `commands:` | the finding | — | the hub commits on the feature branch |
| Change request or fix touching existing code | cartographer · `impact` | the change, the affected area | — | the owner revises with the impact note |
| One-way door surfaces outside Design | architect · `g2` | the change request | — | fairness review → **G2** |
| Critical/major finding deferred | the deferring owner writes a risk entry in `decisions.md` (security findings: security-engineer · `risk-package`) | the finding | — | **D3** risk acceptance |

## Verify

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Verify | test-engineer · `verify` | the spec folder, the feature branch | evidence pack, `evidence/traceability.md` |
| Feature review | code-reviewer · `feature-review` | the feature branch, main | fixes → engineer |
| Security verify (security) | security-engineer · `verify` | the feature branch, the design's Security section | `evidence/security/` |
| UX review (ux) | ux-designer · `ux-review` | the running app, the accessibility evidence | findings → engineer |
| Lens verify (active lenses) | consultant · `verify` | the evidence pack | findings → owners |
| Blocking findings | tech-lead · `revise` → fix tasks in `tasks.md` → Build loop (per task) | the review files | test-engineer re-runs `verify`; the other reviewers re-check only their own blocking findings |
| Exit | hub: `sdd.py trace --phase verify --junit <evidence/junit.xml>` (advisory) | — | Release |

## Release

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Release plan + rehearsal | platform-engineer · `release` (S: G3 entry only, with a rollback note) | the feature branch, the evidence pack | `release.md`, G3 entry |
| Docs | librarian · `docs` (in parallel) | the spec folder, the docs impact list in `decisions.md` | docs updated on the feature branch |
| Architecture upkeep | architect · `evolve` (in parallel) | the design's Architecture updates, ADRs, `decisions.md` | `architecture.md`, superseded ADRs, `stack.yaml` on the feature branch |
| Release review (reliability) | reliability-engineer · `release-review` | `release.md` | platform-engineer revises |
| G3 | — | the G3 entry in `decisions.md` (platform-engineer) | approved → the human merges → the hub confirms the merge → follow-up branch from the latest main |
| Deploy | platform-engineer · `deploy` (staging soak, then production via the protected workflow) | the version, the environment, the follow-up branch | deploy and watch window recorded in `release.md` |

## Evolve (on `sdd/F<NNN>-followup`, after the deploy)

| Step | Agent · mode | Handoff covers | Next |
|---|---|---|---|
| Outcome vs success metric (after the watch window) | product-lead · `evolve` | the release outcome, the metrics | the brief's Outcome, `product.md`; new REQs or features if needed |
| Retrospective | librarian · `retro` | the spec folder | findings → owners of canonical documents; methodology proposals in `decisions.md` |
| Close | hub: `state.yaml` done; tech-lead · `integrate` (follow-up: push and draft PR) | — | the human merges the docs-only PR |

## Operate (`/sdd incident`, on `sdd/INC-nnn-<slug>`)

| Step | Agent · mode | Next |
|---|---|---|
| Triage | incident-responder · `triage` | **fast-path** mitigation entry → the human, now |
| Diagnose (if needed) | reliability-engineer · `diagnose` / engineer · `debug` | evidence into the incident file |
| Impact of the fix (existing code) | cartographer · `impact` | research note for the fix feature |
| Investigate | incident-responder · `investigate` | — |
| Postmortem | incident-responder · `postmortem` (+ reliability-engineer · `post-incident`) | Postmortem section of the incident file, action items |
| Route actions | hub | `/sdd new` for fixes; findings and change requests to the owners of the affected documents |
| Follow-up | incident-responder · `follow-up` | incident closed; tech-lead pushes the branch and opens a docs-only draft PR the human merges |

## Foundation (`/sdd init`, `/sdd adopt`)

The foundation feature runs through the normal phases as class L; what each phase does for a new project and for an existing codebase is in the workflow contract ("Foundation and existing codebases"). The rows above apply, with these modes: product-lead · `discover` (question loop about the product) then `init`, cartographer · `adopt` (existing code), researcher · `options`, architect · `init`, ux-designer · `init`, platform-engineer · `env-plan` and `scaffold`, platform-engineer · `release` (G3 entry).

## Arbiters

Disputes are rare now that most reviews are one round. When a blocking finding is still disputed at the cap:

| Dispute category | Arbiter | If the arbiter is a party / value or risk judgment |
|---|---|---|
| Scope, value, user impact | product-lead · `arbitrate` | the human |
| Architecture, design, NFR trade-off | architect · `arbitrate` | the human |
| Engineering practice, process, task split | tech-lead · `arbitrate` | the human |
| Security severity | security-engineer's verdict stands unless the architect shows the exploit scenario is invalid | the human |
