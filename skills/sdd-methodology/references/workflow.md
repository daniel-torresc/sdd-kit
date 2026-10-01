# Contract 4 — Workflow (hub state machine)

The hub is the main Claude Code session running the `/sdd` workflow. Agents are dispatched by the hub, write artifacts, and return an envelope. By policy, agents do not dispatch other agents, except read-only helper delegation explicitly listed in their own definition (e.g. an owner asking the researcher a question). Every cross-role handoff goes through the hub so state, gates and loop caps stay in one place.

## Triage classes

Assigned at intake from the signals in `.sdd/config.yaml`. **Any single signal of a higher class raises the class.** The class may be raised mid-flight (e.g. an engineer discovers a data migration); it is never silently lowered.

| Class | Typical signals | Flow | Human gates |
|---|---|---|---|
| **T** Trivial | typo, config value, patch dependency bump, docs | build → code-review → done | none |
| **S** Small | localized; no new interface, data model or dependency | mini-spec (REQ+AC) → test-first build → code-review → verify | none (G1 only if ambiguous) |
| **M** Standard | new capability, new interface or data model | full flow; lenses only when triggered | G1, G3 |
| **L** Critical | auth, money, PII, destructive migration, public API, greenfield, hard to reverse | full flow; all assurance lenses; threat model | G1, G2, G3 |

## Phases

| # | Phase | Owner | Contributors | Reviewers | Human gate |
|---|---|---|---|---|---|
| 0 | Triage | hub | cartographer | — | — |
| 1 | Discover | product-lead | researcher, cartographer, ux-designer | challenger | — |
| 2 | Specify | product-lead | ux-designer, architect (consult on feasibility Qs) | challenger, test-engineer | **G1 intent** (M, L) |
| 3 | Design | architect | security-engineer, reliability-engineer, researcher, consultants | challenger, security-engineer, reliability-engineer | **G2 foundations** (when triggered) |
| 4 | Plan | tech-lead | architect | test-engineer, architect (plan-review), challenger (L only) | — |
| 5 | Build | engineer ×N, platform-engineer | test-engineer (tests first) | code-reviewer (per task) | — |
| 6 | Verify | test-engineer | engineer (fixes) | code-reviewer, active lenses, product-lead (acceptance: M, L), architect (conformance: L) | — |
| 7 | Release | platform-engineer | librarian | reliability-engineer | **G3 production** |
| 8 | Operate | incident-responder | reliability-engineer, platform-engineer | — | — |
| 9 | Evolve | librarian | all | — | constitution changes |

## Reviewer independence

When dispatching a reviewer, the hub passes **only** the target artifact@version, its upstream artifacts, the phase, the round number and (round ≥2) the previous review file with the author's resolutions. It never passes the author's return envelope, summary or reasoning. When several reviewers run in parallel, the hub merges their findings, removes duplicates (keeping the most severe, crediting both) and routes each to its `route_to`.

## G1 and G2 preparation

- **G1:** the challenger's "assumptions ranked by risk" (from its specify review) sets the order of the assumptions table in `gates/G1-intent.md`; the riskiest come first and are marked for the human's attention.
- **G2:** the architect's options package is reviewed by the challenger for **fairness and completeness** (all viable options, symmetric pros/cons, accurate fit matrix, recommendation separated) before the hub presents it to the human.

## Second opinion

The hub may dispatch the challenger in `second-opinion` mode (a) on any disputed blocking finding before sending it to an arbiter, and (b) on any D1 decision in `log.md` of a class L feature at the phase exit. The second opinion informs the arbiter or the human; it does not decide.

## Intent questions (Discover, hybrid)

Before drafting, product-lead may return `needs-input` with **at most 3** intent questions, and only when the request has materially different interpretations (different users, problem, or success criteria). The hub asks the human, then re-dispatches product-lead with the answers. Every other gap becomes an `ASM-nn` and is confirmed at G1.

## Phase micro-cycle

```
drafting ──► in-review ──► revising ──(≤ cap)──► exit-check ──► [gate] ──► done
 (owner)    (panel, in       (owner)              (mechanical    (human,
            parallel)          ▲   │               + verdicts)    if D3)
                               └───┘ loops +1
                   cap reached ──► arbiter ──► human
```

## Loop caps (defaults in config.yaml)

- Review revision rounds: **2** for S/M, **3** for L.
- Build fix attempts per task: **3**, then tech-lead intervenes; if still failing, escalate.

## Artifacts live on the feature branch

Worktrees branch from the **committed** feature branch, so uncommitted artifacts are invisible to them. After every agent step that changes artifacts (specs, reviews, gates, log, `.sdd/*`), the hub commits them to the feature branch: `chore(sdd): <agent> <mode> <artifact>` with a `Refs:` trailer. Before a feature branch exists (Discover/Specify), the hub commits on `sdd/<F>-<slug>` created at intake.

## Build execution

1. The hub asks tech-lead (`coordinate`) which tasks are ready: dependencies merged, `touches` not overlapping a running task, at most `parallelism.max_parallel_tasks` running.
2. Each task runs in its own worktree on `sdd/<F>-<T>` branched from the feature branch (the engineer agent declares `isolation: worktree`; for test-engineer `test-task` dispatches the hub passes `isolation: "worktree"` on the Agent call; the hub keeps the feature branch checked out when dispatching). Branch names use the task ID verbatim: `sdd/F003-T-04`. Test-engineer tasks come before the engineer tasks that depend on them.
3. Each finished task gets a code review: `test-review` for test-engineer tasks (before engineers build against them) and `task-review` for engineer tasks. When it is approved, tech-lead (`integrate`) merges it into the feature branch, runs the tests, and pushes. The draft PR is kept updated.
4. After 3 failed fix attempts on a task, tech-lead (`unblock`) re-scopes, re-sequences, routes upstream, or escalates.
5. When all tasks are merged and green, the feature moves to Verify.

## Verify

code-reviewer runs a `feature-review` of the integrated diff (M/L). test-engineer (`verify`) runs the full suite, `sdd.py trace --phase verify --junit`, every NFR verification, mutation testing on changed modules (class L; surviving mutants in AC code are `major`), and exploratory testing for UI or public APIs, then writes the evidence pack `specs/<f>/evidence/README.md`. product-lead's acceptance review judges the evidence pack, not just test results. **Flaky tests block Verify**; re-runs are for diagnosis only.

## Model per mode

Agents declare a default model; the hub overrides it at dispatch where judgment matters more than volume:
- test-engineer: **opus** for `testability-review`, `plan-review` and `verify`; sonnet for `test-plan`, `test-task` and `diagnose`.
- engineer: **opus** for tasks marked `risk: high` and for fix attempts 2–3 of any task; sonnet otherwise.
- code-reviewer: **opus** for `risk: high` tasks, `feature-review`, and re-reviews of disputed blocking findings; sonnet otherwise.

## Backward flow

A finding routed upstream reopens **only the affected artifact**. The owner revises and bumps its version; downstream artifacts become stale; the hub re-validates only the stale chain.

## Exit checks (before any gate)

| Phase | Mechanical check | Plus |
|---|---|---|
| Specify | `sdd.py trace --phase specify` clean; every Q has a default | no open blocking findings |
| Design | `sdd.py trace --phase design` clean; ADR for every D1+ architectural choice; threat model covers every external IF (L) | no open blocking findings |
| Plan | `sdd.py trace --phase plan` clean; every task has `surface` and `stack` | no open blocking findings |
| Build | lint, types, unit tests green (hooks) | per-task code review approved |
| Verify | `sdd.py trace --phase verify --junit …` clean | all lens reviews and the product-lead acceptance review approve |
| Release | rollback path documented and exercised; runbook exists | G3 approved |

## state.yaml

The hub writes it after every step so work can resume in any session. See `templates/state.yaml`.

## Commands (hub entry points)

| Command | Does |
|---|---|
| `/sdd init` | Greenfield bootstrap: constitution → product context (product-lead) → architecture baseline and stack G2 packages (architect) → challenger fairness review → human decides → ADRs, `.sdd/architecture/*` → scaffold, CI, fitness functions, deployable walking skeleton (platform-engineer) |
| `/sdd new <idea>` | Triage and create the spec folder |
| `/sdd` | Read state and advance autonomously until a gate or blocker |
| `/sdd status` | Where every feature stands |
| `/sdd gates` | Pending decision packages |

## Stack routing

The skills loaded into a builder are resolved from, in order: the task's `stack:` field → the stack profile in `.sdd/architecture/conventions.md` → `.sdd/config.yaml` `stack_routing`. If no skill exists for a chosen stack, the researcher writes `.sdd/briefs/<stack>.md` from current docs; the librarian may later promote it to a skill.
