# Contract 4 — Workflow (hub state machine)

The hub is the main Claude Code session running the `/sdd` workflow. Agents are dispatched by the hub, write artifacts, and return an envelope. By policy, agents do not dispatch other agents, except read-only helper delegation explicitly listed in their own definition (e.g. an owner asking the researcher a question). Every cross-role handoff goes through the hub so state, gates and loop caps stay in one place.

## Triage classes

Assigned at intake from the signals in `.sdd/config.yaml`. **Any single signal of a higher class raises the class.** The class may be raised mid-flight (e.g. an engineer discovers a data migration); it is never silently lowered.

| Class | Typical signals | Flow | Human gates |
|---|---|---|---|
| **T** Trivial | typo, config value, patch dependency bump, docs | build → code-review → done | none |
| **S** Small | localized; no new interface, data model or dependency, and no change existing callers can observe | mini-spec (REQ+AC) → test-first build → code-review → verify | none (G1 only if ambiguous) |
| **M** Standard | new capability, new interface or data model | full flow, with brief and requirements written and reviewed together in Specify; lenses only when triggered | G1, G3 |
| **L** Critical | auth, money, PII, destructive migration, public API, greenfield, hard to reverse | full flow with a separate Discover (brief challenged before requirements); all assurance lenses; threat model | G1, G2, G3 |

## Phases

| # | Phase | Owner | Contributors | Reviewers | Human gate |
|---|---|---|---|---|---|
| 0 | Triage | hub | cartographer (`context`, existing code) | — | — |
| 1 | Discover (L only) | product-lead | researcher (`domain`, `question`), cartographer | challenger | — |
| 2 | Specify | product-lead | ux-designer (`flows`, UI features), architect (`consult`), researcher | challenger, test-engineer (`testability-review`), reliability-engineer (`nfr-review`, reliability lens), consultants (`specify-review`, active lenses) | **G1 intent** (M, L) |
| 3 | Design | architect | security-engineer (`threat-model`, security lens), reliability-engineer (`slo`, `capacity`), researcher (`options`), consultants (`analysis`) | challenger, security-engineer (`design-review`), reliability-engineer (`design-review`), consultants (`design-review`) | **G2 foundations** (one-way doors) |
| 4 | Plan | tech-lead | architect, reliability-engineer (`perf-plan`), test-engineer (`test-plan`) | test-engineer, architect (`plan-review`), challenger (L), consultants (`plan-review`) | — |
| 5 | Build | engineer ×N, platform-engineer, test-engineer (tests first) | security-engineer (`dependency-review`, `secret-review` on request) | code-reviewer (`test-review`, `task-review`), security-engineer (`code-review`, security lens, `risk: high` tasks) | — |
| 6 | Verify | test-engineer | engineer (fixes) | code-reviewer (`feature-review`), security-engineer (`verify`), ux-designer (`ux-review`), consultants (`verify`), product-lead (`accept`: M, L), architect (`conformance`: L) | — |
| 7 | Release | platform-engineer (`release`) | librarian (`docs`) | reliability-engineer (`release-review`) | **G3 production** |
| 8 | Operate | incident-responder | reliability-engineer, platform-engineer, engineer (`debug`) | — | mitigation execution (fast-path D3) |
| 9 | Evolve | librarian (`docs`, `knowledge`, `retro`) | architect (`evolve`), cartographer (`refresh`), reliability-engineer (SLO review) | — | constitution and gate changes (MIPs) |

## Lens activation

At triage (and whenever new information appears) the hub matches `lens_triggers` in `.sdd/config.yaml` and records active lenses in `state.yaml`. Class L activates every lens whose trigger plausibly applies. Each active lens adds its agent to the reviewer panels of the phases above:

| Lens | Agent | Phases |
|---|---|---|
| security | security-engineer | Design (threat model + review), Build (code review of security-relevant tasks), Verify |
| reliability | reliability-engineer | Specify (NFRs), Design, Plan (perf plan), Release |
| ux (includes accessibility) | ux-designer | Specify (flows), Verify (ux-review) |
| privacy, data-migration, ai-evals, finops, api-compat | consultant + lens skill | Specify through Verify, as the lens skill describes |

Dependency approvals (`security-engineer · dependency-review`) apply to every feature, lens or not.

## Reviewer independence

When dispatching a reviewer, the hub passes **only** the target artifact@version, its upstream artifacts, the phase, the round number and (round ≥2) the previous review file with the author's resolutions. It never passes the author's return envelope, summary or reasoning. When several reviewers run in parallel, the hub merges their findings, removes duplicates (keeping the most severe, crediting both) and routes each to its `route_to`.

## G1 and G2 preparation

- **G1:** the challenger's "assumptions ranked by risk" (from its specify review) sets the order of the assumptions table in `gates/G1-intent.md`; the riskiest come first and are marked for the human's attention.
- **G2:** the architect's options package is reviewed by the challenger for **fairness and completeness** (all viable options, symmetric pros/cons, accurate fit matrix, recommendation separated) before the hub presents it to the human.

## Second opinion

The hub may dispatch the challenger in `second-opinion` mode (a) on any disputed blocking finding before sending it to an arbiter, and (b) on any D1 decision in `log.md` of a class L feature at the phase exit. The second opinion informs the arbiter or the human; it does not decide.

## Intent questions (hybrid)

Before drafting the brief (in Discover for L, in Specify for M), product-lead may return `needs-input` with **at most 3** intent questions, and only when the request has materially different interpretations (different users, problem, or success criteria). The hub asks the human, then re-dispatches product-lead with the answers. Every other gap becomes an `ASM-nn` and is confirmed at G1.

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

## Git conventions

| Thing | Convention |
|---|---|
| Feature branch | `sdd/F<NNN>-<slug>`, created from the main branch at intake |
| Task branch | `sdd/F<NNN>-T-<nn>` (task ID verbatim), one worktree per task, branched from the feature branch |
| Commits | Conventional Commits (`feat`, `fix`, `test`, `refactor`, `chore`, `docs`, `perf`; `!` for breaking), one logical change each, trailer `Refs: F<NNN>:T-<nn>` |
| Artifact commits | `chore(sdd): <agent> <mode> <what>` by the hub |
| Task → feature | merge commit (`--no-ff`), in dependency order, by tech-lead |
| Feature → main | only through G3 |
| Remote | pushing `sdd/*` branches and draft PRs are autonomous; merges to main, force-pushes and remote branch deletion are human decisions |

## Integration

Integrate each task as soon as its review approves — never in batches at the end. After each merge, run the full suite on the feature branch. Only mechanical conflicts (both sides added entries, regenerated lockfiles) are resolved by tech-lead; anything touching logic is aborted and returned to the later task's engineer. A merge that turns the feature branch red is reverted and routed to that task. Each integration is recorded in `reviews/integration-tech-lead-<n>.md`.

## Verify

code-reviewer runs a `feature-review` of the integrated diff (M/L). test-engineer (`verify`) runs the full suite, `sdd.py trace --phase verify --junit`, every NFR verification, mutation testing on changed modules (class L; surviving mutants in AC code are `major`), and exploratory testing for UI or public APIs, then writes the evidence pack `specs/<f>/evidence/README.md`. product-lead's acceptance review judges the evidence pack, not just test results. **Flaky tests block Verify**; re-runs are for diagnosis only.

## Operate

`/sdd incident <description>` (or an alert routed by the human) opens `.sdd/incidents/INC-nnn-*`. incident-responder (`triage`) classifies and returns a **fast-path mitigation package**; the hub presents it immediately (no batching with other gates). The human executes or approves the mitigation. Then `investigate` → `postmortem` → action items routed into the workflow (new T/S features via `/sdd new`, change requests, debt, alerting, tests, runbooks, lessons) → `follow-up`.

## Evolve

After G3 (and after abandoned features): librarian `docs` and `knowledge`; architect `evolve` (architecture overview, conventions, debt); cartographer `refresh` of affected map sections (existing code); librarian `retro` → lessons and methodology improvement proposals (`.sdd/improvements.md`). Periodically (`/sdd retro --all`), librarian `cross-retro`. MIPs are decided by their named decider; constitution and gate changes are D3.

## Existing codebases

`/sdd adopt` runs cartographer `adopt` (project map + proposals to architect, product-lead, test-engineer, platform-engineer), then the owners create `.sdd/architecture/*`, `.sdd/product/*`, characterization tests and CI gaps as normal work. For every feature on existing code, triage dispatches cartographer `context` before Discover.

## External sync

Writes to systems outside the repository — issue trackers, PR review comments, release notes, knowledge bases, design tools — are prepared by the owning agent or the hub as an **outbox** and performed by the hub only after the human approves them (one batched approval per stop, configured in `.sdd/config.yaml` `sync`). Pushing `sdd/*` branches and updating draft PRs remain autonomous.

## Model per mode

Agents declare a default model; the hub overrides it at dispatch where judgment matters more than volume:
- test-engineer: **opus** for `testability-review`, `plan-review` and `verify`; sonnet for `test-plan`, `test-task` and `diagnose`.
- engineer: **opus** for tasks marked `risk: high` and for fix attempts 2–3 of any task; sonnet otherwise.
- code-reviewer: **opus** for `risk: high` tasks, `feature-review`, and re-reviews of disputed blocking findings; sonnet otherwise.
- platform-engineer: **opus** for `release`; sonnet otherwise.
- All other agents run on their declared model (opus for judgment roles, sonnet for cartographer and librarian).

## Backward flow

A finding routed upstream reopens **only the affected artifact**. The owner revises and bumps its version; downstream artifacts become stale; the hub re-validates only the stale chain.

## Exit checks (before any gate)

| Phase | Mechanical check | Plus |
|---|---|---|
| Specify | `sdd.py trace --phase specify` clean; every Q has a default | no open blocking findings |
| Design | `sdd.py trace --phase design` clean; ADR for every D1+ architectural choice; threat model covers every external IF (security lens); SLOs exist for new journeys (reliability lens) | no open blocking findings |
| Plan | `sdd.py trace --phase plan` clean; every task has `surface` and `stack` | no open blocking findings |
| Build | lint, types, unit tests green (hooks) | per-task code review approved |
| Verify | `sdd.py trace --phase verify --junit …` clean | all lens reviews and the product-lead acceptance review approve |
| Release | rollback rehearsed and recorded in `release.md`; runbook updated; reliability release-review approves | G3 approved |
| Evolve | docs updated; retro written | — |

## state.yaml

The hub writes it after every step so work can resume in any session. See `templates/state.yaml`.

## Commands (hub entry points)

| Command | Does |
|---|---|
| `/sdd init` | Greenfield bootstrap: constitution → product context (product-lead) → foundational technology decisions as G2 packages (architect) → challenger fairness review → human decides → ADRs, `.sdd/architecture/*` → scaffold, CI, fitness functions, deployable walking skeleton (platform-engineer) |
| `/sdd new <idea>` | Triage and create the spec folder |
| `/sdd` | Read state and advance autonomously until a gate or blocker |
| `/sdd status` | Where every feature stands |
| `/sdd gates` | Pending decision packages |
| `/sdd adopt` | Bring an existing codebase into SDD (cartographer map + proposals) |
| `/sdd incident <description>` | Open and drive an incident |
| `/sdd retro [F \| --all]` | Retrospective for a feature, or across features |
| `/sdd sync` | Review and approve the external-sync outbox |
| `/sdd feature <F>` | Switch the active feature |

## Technology context

The methodology skills describe *how to work*; technology-specific knowledge comes from technology skills declared per project.

- **`.sdd/stack.yaml`** is the single place that declares the project's technologies: one entry per concern (language, frameworks, datastore, testing, pipeline, infrastructure, cloud, frontend, …), each with its version, status, who decided it, its ADR or pending gate, and the **skills** to load for it.
  - The **human** may write entries at any time; `fixed: true` entries are constraints that agents never change and every technology decision must respect.
  - The **architect** records decisions: G2 outcomes (`decided-by: human-at-G2`) and smaller reversible choices (`decided-by: architect`, logged), always with an ADR when significant.
  - The **researcher** may propose candidate skills for a technology in a research note; the human chooses.
- **Skill loading:** at every dispatch the hub resolves the technologies the task involves (the task's `stack:` concerns, or the agent's area for non-task work) to their `skills` in `stack.yaml` and names them in the dispatch; agents load them before working. If a listed skill isn't installed, the hub asks the human to install it (from `skill-sources`); meanwhile agents rely on official documentation and any stack brief.
- **Stack briefs:** when a decided technology is unfamiliar and no adequate skill exists, the researcher writes `.sdd/briefs/<technology>.md` from current official documentation and links it from the entry.
- **`.sdd/commands.yaml`** is the project's command registry by purpose (install, test, lint, build, migrate, scan, deploy-nonprod, …), written by platform-engineer when tooling is introduced and reviewed by the architect. The guard lets each agent run only the registered commands for the purposes in its policy, read from the **committed** file, with a global denylist.
