# SDD plugin — design decisions and review backlog

This file records every design decision behind the agent organization, so the complete system can be reviewed as a whole before testing and refinement.

- **Agreed** = decided together during the design conversation.
- **Default** = chosen while building the remaining capabilities (2026-10-06), using the established patterns. Each default is a candidate for review.

## 1. Architecture (agreed)

- Roles are agents; expertise is skills (`practice-*`, `stack-*`, `lens-*`); quality lenses are reviewer agents; phases are the hub's state machine; tools are CLIs, MCP servers and hooks.
- Hub-and-spoke: the main session runs `/sdd` and dispatches agents. Agents communicate only through artifacts and a strict return envelope. Agents don't dispatch other agents (policy).
- Contracts (`sdd-contracts`): artifacts and traceability IDs; findings schema and review rules; autonomy classes D0–D3; workflow with triage classes T/S/M/L, phase micro-cycle, loop caps (2 rounds for S/M, 3 for L; 3 fix attempts) and exit checks.
- Human gates only for D3: G1 intent, G2 foundations (the architect presents every option; **the human decides**), G3 production, risk acceptance, scope change, legal, deadlock, constitution changes, spend, external writes.
- Ownership guard (PreToolUse hook) enforces each agent's writes, shell commands and MCP access, and **auto-approves in-policy actions** (off switch: `permissions.auto_approve: false`). Project commands come from the `commands:` section of the committed `.sdd/stack.yaml`; runtime dependencies are approved in the design's dependency review (§6).
- Traceability script `sdd.py` (trace and stale checks).

## 2. Per-agent decisions

> Paths and artifacts in §2–§5 are as decided at the time; §6 consolidated the asset set and supersedes them where they differ.

| Agent | Agreed | Default (to review) |
|---|---|---|
| product-lead | `.sdd/product/` context; acceptance review in Verify; hybrid intent questions (≤3 before drafting); preparer writes the gate file | — |
| challenger | G2 fairness review; risk ranking orders G1 assumptions; findings budget; second-opinion mode | — |
| architect | `.sdd/architecture/`; machine-readable contracts for external/public interfaces; spikes; technology choices derived from context with a per-decision reference option (no defaults, see §4); one-page G2 brief | Lists runtime dependencies in `design.md` for security vetting; testability seams in every design |
| tech-lead | Integrator; test-first as separate tasks; git autonomy (`sdd/*` pushes and draft PRs autonomous, main is G3); max 3 parallel tasks | — |
| test-engineer | Mutation testing for L; exploratory testing + evidence pack; zero tolerance for flaky tests; sonnet/opus per mode | — |
| engineer | opus for `risk: high` and fix attempts 2–3; refactor only within `touches`; only approved runtime deps; ≥85% diff coverage | — |
| code-reviewer | sonnet/opus per mode; re-runs checks in a review worktree; test-review before engineers build; feature review in Verify | — |
| platform-engineer | dev/staging deploys autonomous, production via G3 + GitHub environment protection, adds/destroys/spend are D3; dev container per project; supply-chain gates block on critical CVEs and secrets; rolling deploy with auto-rollback, semver, Conventional Commits changelog | — |
| security-engineer | — | opus; ASVS L1 (M) / L2 (L or personal/financial/health data); threat model in parallel with design; reviews only when the security lens is active, but **every** runtime dependency goes through it; owns `tests/security/`; DAST (ZAP baseline) only against local/staging; risk acceptance with an expiry date; its severity verdict stands unless the architect shows the exploit scenario is invalid |
| reliability-engineer | — | opus; also covers performance; owns the SLO catalog and capacity (`.sdd/operations/`) and `perf-plan.md`; designs load/resilience tests, test-engineer runs them; burn-rate alerting; releasing with an exhausted error budget is D3 |
| ux-designer | — | opus; owns `ux.md` and the project design system; low-fidelity HTML prototypes; Figma read-only; writes research plans for the human and never invents research results; brand identity is D3 |
| researcher | — | opus; writes research notes and stack briefs only, never decides; every claim cited with a confidence rating; regulation is information, not legal advice |
| cartographer | — | sonnet, medium effort; read-only on code; `.sdd/map/` with commit SHA; context pack for every feature on existing code (dispatched at triage); `adopt` proposes and never writes others' artifacts |
| librarian | — | sonnet; owns README and `docs/` (except ADRs and runbooks), the knowledge base, retros and methodology improvement proposals (MIPs); external knowledge sync opt-in |
| incident-responder | — | opus; SEV1–4; recommends mitigation, **the human executes**; fast-path presentation; blameless postmortems for SEV1–2; every action item routed to an owner |
| consultant | — | One generic agent plus five lens skills (privacy, data-migration, ai-evals, finops, api-compat), selected per dispatch; opus |

## 3. Hub decisions

| Decision | Status |
|---|---|
| `/sdd` runs autonomously until a human decision or blocker; push notification on stop; gates as one-screen summary + AskUserQuestion; artifacts committed after every step; agent worktree cleanup after integration | Agreed |
| Subcommands `adopt`, `incident`, `retro`, `sync`; Evolve runs automatically after deploy | Default |
| Lens activation from `lens_triggers`; class L activates every plausible lens; new triggers found mid-flight add lenses and can raise the class | Default |
| External writes need one batched human approval per stop (now `external-write` entries in `decisions.md`, §6); only `sdd/*` pushes and draft PRs stay autonomous | Default |
| Fallbacks for missing agents removed; every role now has its agent | Default (follows the complete-system principle) |

## 4. Skills review (agreed 2026-10-06)

**Principle:** methodology skills explain *how to think and work*. They contain no technology, framework or tool guidance. Technology-specific knowledge comes from external skills that the harness loads when a task needs them. The plugin maintains no stack skills.

| Skill | Outcome |
|---|---|
| `sdd-methodology` | Renamed **`sdd-contracts`** (preloaded by every agent). Kept separate from `sdd` (the hub), so agents don't preload orchestration. Git conventions, integration rules and AC tagging moved into the contracts. |
| `sdd` | Kept (hub). Stack routing removed. |
| `practice-critique`, `practice-requirements`, `practice-discovery`, `practice-architecture` | Kept. Tool examples made neutral. |
| `practice-tech-selection` | Redesigned. No defaults or persisted baseline: criteria come from context. Each decision gets a **reference option derived from context** (what is already run, or the simplest viable option). Novelty budget, coupled decisions, G2 package and brief. |
| `practice-planning` | Rewritten as **deriving the plan from the design**: inventory → slices → sequence → tasks → check against the design. Git and integration moved to the contracts. |
| `practice-testing`, `practice-engineering`, `practice-code-review` | Rewritten without technology references. Testing and code review now include accessibility verification and checks. |
| `practice-security-basics` + `practice-security` | Merged into a **layered `practice-security`**: SKILL.md holds the principles everyone preloads, `references/` holds the security-engineer's procedures (threat modeling, dependency vetting, verification, risk acceptance). |
| `practice-reliability` | Kept. Gains the incident-response section (Operate). |
| `practice-incident` | Removed. Generic incident practice moved into `practice-reliability`; SDD specifics (artifacts, fast path, action-item routing) moved into the contracts and the incident-responder agent. |
| `practice-ux` | Deepened around UX reasoning and decision-making. Now **owns accessibility** (WCAG 2.2 AA). |
| `practice-research` | Generic research process. Stack briefs kept as project knowledge; promotion to skills removed. |
| `practice-cartography` | Kept, plus **changing existing code safely** (characterization tests, seams, strangler, incremental change). |
| `practice-documentation` + `practice-retrospective` | Merged into **`practice-knowledge`** (documentation, knowledge base, learning loop). The librarian's `promote` mode was removed. |
| `practice-platform` | Rebuilt without technology references, plus dependency and version maintenance. |
| `practice-release` | Expanded: readiness, release types incl. hotfixes, delivery strategies, flag lifecycle, data/contract changes across releases, after-release verification, communication. |
| `stack-python`, `stack-github-actions`, `stack-docker`, `stack-opentofu` | Removed. |
| `lens-accessibility` | Removed. Accessibility now lives in ux-designer / `practice-ux`, `practice-testing` and `practice-code-review`; the `ux` lens covers it. |
| `lens-data-migration`, `lens-ai-evals`, `lens-finops`, `lens-api-compat` | Expanded, without technology references. |
| `lens-privacy` | **Added** (data inventory, purpose and lawful basis → human, minimization, retention and deletion, data-subject rights, consent, processors and transfers, impact assessment). |

Result: 31 → 24 skills (`sdd`, `sdd-contracts`, 17 practices, 5 lenses).

### Project stack and command registry (agreed 2026-10-06)

- **`.sdd/stack.yaml`** (template in `sdd-contracts/templates/`) is the per-project place for its technologies.
  - Each concern has: a choice, version, status, `decided-by` (human, human-at-G2, architect, existing), ADR or gate, stack brief, and the **technology skills** to load.
  - **Who writes it:** the human writes `fixed: true` constraints (also captured by the hub at `/sdd init`); the architect records G2 outcomes and smaller choices; the researcher proposes candidate skills.
  - **How it's used:** the hub resolves each task's `stack:` concerns to skills and names them in the dispatch; missing skills become install requests to the human (`skill-sources`).
  - **Protection:** the hub refuses to commit changes to `fixed` entries.
- **`.sdd/commands.yaml`** (template too) is the project command registry by purpose, owned by platform-engineer and reviewed by the architect.
  - The guard reads the **committed** file and allows each agent only the purposes in its policy (`project_commands` in `hooks/ownership.json`).
  - A global denylist always applies.
  - Runtime additions through `deps-add` are checked against `.sdd/dependencies.yaml`.
  - This removed every hard-coded toolchain pattern (uv, npm, docker, tofu, scanners) from the guard policies and agent shell sections.
- The code-reviewer now runs in an isolated worktree, checks out the task branch detached, and writes its review to the main checkout. The guard allows SDD artifacts (`specs/`, `.sdd/`) to be written back from worktrees.
- Remaining assumptions, deliberately kept:
  - GitHub as the forge (`gh` for draft PRs and pipeline runs);
  - conventional platform paths (`.github/`, `infra/`, container files) in the engineer's write exclusions;
  - `uv` to run the plugin's own `sdd.py`.

## 5. Agent review (agreed 2026-10-06)

Consistency audit (mechanical): guard permissions aligned with agent instructions; every mode now has a dispatch trigger; artifact ownership tables match the guard.

| Decision | Detail |
|---|---|
| Docs ownership | README and `docs/` belong to the librarian; engineers keep docstrings and in-code docs and report a **Docs impact** list in their handoff, which the hub collects into `log.md` |
| Class M Discover + Specify merged | Brief and requirements are written in one dispatch and reviewed together; class L keeps a separate Discover |
| Technology constraints from requests | Escalated by product-lead; the hub confirms with the human and records them as `fixed` entries in `stack.yaml` |
| UX decisions and Build-time review | `ux.md` records decisions, proposed acceptance criteria and research plans; ux-designer reviews the first delivery of each new screen in Build (worktree, runs the app) as well as Verify |
| Simplest-structure principle | The architecture skill keeps a principle, not a default: one deployable with clear module boundaries; distribution must be justified by an NFR or constraint in an ADR |
| Architect integrates parallel work | Threat model, SLOs, capacity and lens analyses are folded into the design before review; designs list runtime dependencies (→ dependency review) and infrastructure/spend (→ env-plan) |
| Explicit per-task reviewers | Tasks declare `reviews:` (ux, security, lens names), validated by `sdd.py`; the hub dispatches exactly those reviewers alongside code-reviewer |
| Command registry integrity | The guard reads `.sdd/commands.yaml` from the main checkout (feature branch), so registry changes take effect only after architect review and integration; new tooling is registered in its own task before use |
| New modes and triggers | architect `review-commands`; researcher `skills`; env-plan after hosting decisions and for designs that need resources; risk packages for deferred critical/major findings; cartographer `impact`; product-lead `evolve` with an Outcome section in the brief |

## 6. Asset consolidation (agreed 2026-10-07)

**Principle:** start from a small, well-defined set of core assets and expand only when a real need appears. Knowledge lives in canonical documents, never in a separate knowledge base. Templates went from 38 to 20.

**Project assets (`.sdd/`)**

| Asset | Owner | Replaces |
|---|---|---|
| `constitution.md` | human | — (technology constraints moved to `stack.yaml`) |
| `config.yaml` | human | — |
| `stack.yaml` | architect (human's `fixed` entries) | also absorbs `commands.yaml` (a `commands:` section) and `dependencies.yaml` (approvals live in the design's dependency review) |
| `product.md` | product-lead | `.sdd/product/` (vision, personas, glossary) |
| `architecture.md` | architect | `.sdd/architecture/` (overview, conventions, fitness functions, debt), `.sdd/operations/` (service levels, capacity), `.sdd/map/` |
| `docs/adr/` | architect | — |
| `design-system.md`, `incidents/` | ux-designer, incident-responder | on demand; postmortem is a section of the incident file |

**Foundation and state.** `/sdd init` and `/sdd adopt` run the foundation as a feature, `specs/000-foundation/` on `sdd/F000-foundation`. No project-level state: the active feature is the checked-out `sdd/*` branch (no `.sdd/state.yaml`, no `.sdd/active`).

**Feature assets (`specs/NNN-slug/`).** `state.yaml` (simplified: status, waiting-for-human, next, phases, lenses, review-rounds, tasks, stale, history), `brief.md`, `requirements.md`, `ux.md`, `research/`, `design.md`, `contracts/`, `tasks.md`, `test-plan.md`, `evidence/`, `release.md`, `reviews/`, `decisions.md`.

| Change | Replaces |
|---|---|
| **`decisions.md`** per feature: autonomous decisions, entries waiting for the human (G1–G3 and `H-nn`: risk, scope, legal, deadlock, external write, mitigation, methodology, spend, setup), the human's answers, docs impact | `gates/` (G1-intent, G2 packages, G2-brief, G3, risk-*), `log.md`, `.sdd/outbox.md`, MIPs |
| **Research notes** (one rich template; kinds: question, technology-options, technology-reference, codebase-investigation, spike, domain) | stack briefs, spikes, cartographer `context.md` and `impact-*` |
| Specialist input as **review findings** folded into the design's sections (Security, Data and privacy, Cost, failure modes) and the test plan (Performance and resilience, Evaluations) | threat model, `lens-<lens>.md`, `evals.md`, `perf-plan.md`, SLO/capacity files |
| Traceability report written only on request (`sdd.py trace … --report evidence/traceability.md`) | `trace.md` |
| Tasks use `delivers` (IDs) and `files` (paths) | `refs`, `touches` |
| Retros route findings to the owners of canonical documents and list methodology proposals in `decisions.md` | knowledge base, `lessons`, `improvements`, `retro.md`, knowledge sync |

**Mode changes.** cartographer `investigate`/`impact`/`adopt` (was `context`/`refresh`/…); librarian `docs`/`retro` only; researcher `technology-reference` (was `stack-brief`); security-engineer's threat analysis is part of `design-review`; reliability-engineer `perf-review` (was `slo`/`capacity`/`perf-plan`); architect `review-commands` removed (it registers commands proposed by platform-engineer or task owners as findings).

**Guard.** Commands from the committed `stack.yaml`; dependency-approval checks removed; write policies rebuilt for the new paths; the hub may also write `.sdd/constitution.md` and `.sdd/config.yaml` (copied at init, later only human-approved changes).

**Fixed during the reference sweep.** Librarian `docs` runs in Release (in parallel with the release plan) so the docs merge with the feature; it was listed in both Release and Evolve.

## 7. End-to-end workflow review (agreed 2026-10-07)

Every class (T, S, M, L) and path (init, adopt, feature, incident, retro) walked through the contracts, dispatch table and hub.

| # | Problem found | Decision |
|---|---|---|
| 1 | Work after the merge to main (deploy record, outcome, retro, `done`) had no branch; incidents were committed onto unrelated feature branches | architect `evolve` moves into Release (with librarian `docs`), so both merge with the feature. Post-release work goes on `sdd/F<NNN>-followup`, incidents on `sdd/INC-nnn-<slug>`, both from `origin/<main>` with docs-only draft PRs the human merges. Nothing is committed to main directly |
| 2 | Test-first tasks make the feature branch red by design, but integration reverted red merges | "Green" = all tests pass except those listed by the new `sdd.py expected-failing` (ACs whose implementation task has no `Refs:` commit on the branch yet); the list must be empty at the end of Build |
| 3 | Class S had no tasks and no merge gate | Explicit phases-per-class matrix. S: REQ+AC → short `tasks.md` (no panel) → Build → test-engineer Verify → G3 (lite: no `release.md`). `sdd.py` now checks S plans |
| 4 | Class T had nowhere to record its gate | T: `sdd/T-<slug>` → engineer (`sdd/T-<slug>-impl`) → code-review (in the envelope) → tech-lead pushes a draft PR → the human's PR merge is the gate |
| 5 | Init/adopt couldn't be resumed by `/sdd` | The foundation runs as class L through the normal phases (Discover: product; Design: G2, stack, architecture; Plan/Build: skeleton or characterization tests and CI gaps; Release: G3 lite) |
| 6 | The hub couldn't see the remote main | Hub may `git fetch`; branches start from `origin/<main>`; merges detected with `git branch -r --merged` |
| 7 | Code investigation ran before triage, without a folder | Triage → open the feature → cartographer `investigate` (S/M/L only) |
| 8 | Verify findings had no fix path | tech-lead turns them into fix tasks → Build loop → test-engineer re-verifies; reviewers re-check only their findings; review-round cap |
| 9 | Design exit didn't require dependency verdicts or the env-plan decision | Added to the Design exit check, plus no pending G2 |
| 10 | `test-plan.md` was unreviewed | Written first in Plan; reviewed by architect (and challenger for L) in the plan panel |
| 11 | Lens findings for the test plan arrived before it existed | The hub holds them and passes them to `test-plan` |
| 12 | G2 listed only for class L | G2 applies to any class when a one-way door appears |

Also fixed: `sdd.py` matched skip-directories against the absolute path, so projects under a `build`/`dist`/`.claude` folder had all tests ignored.

## 8. Review backlog (before testing)

From the human's instructions for the review phase:

1. ~~Reuse existing skills~~: done as the skills review (§4). Selecting external stack skills is a separate, later step.
2. ~~End-to-end workflow review~~: done (§7).
3. ~~Agent review~~: done (§5).
4. ~~Assets review~~: done (§6).
5. ~~Capability and dependency gaps~~: closed 2026-10-07.
   - Brain-vault integration: **dropped** (no separate knowledge base; knowledge lives in the repository).
   - Issue tracker: **none for now** (`sync.issue_tracker: none`); any tracker works later through its connector as approved external writes.
   - Local platform tooling: per-project commands in `stack.yaml`, installed by the human per test stage; nothing ships with the plugin.
   - Stack skills: external, declared per project in `stack.yaml`.
   - Hub re-read: added local-only projects (no `origin`), empty-repository init, follow-up `done` state, feature switch to the follow-up branch.
   - Packaging (rename to sdd-kit, README, version, marketplace): after testing.
6. **Testing**. Stage 1 done 2026-10-07: `tests/guard_cases.py` (229 cases + 4 controls) and `tests/sdd_cases.py` (28 checks), all passing. Two policy fixes from it: platform-engineer no longer writes anything under `src/` (the entry point and health endpoints are an engineer walking-skeleton task); authors answer reviews in a separate `<review-file>-answers.md`, so each reviewer's verdict can only be written by that reviewer. Stages, cheap to expensive: (1) guard policies and `sdd.py` against a fixture; (2) class T and S on a small local-only fixture; (3) class M with a GitHub remote, through the follow-up branch; (4) `/sdd init` greenfield.
7. **Packaging**, after testing.

## 9. Methodology simplification review (in progress, started 2026-10-09)

The human is reviewing the whole methodology to make it simpler and cheaper in tokens. The decisions below were **applied on 2026-10-09** to the agents, skills, templates, guard and tests. The open questions at the end are still open.

**Hub.** The hub stays a pure coordinator. `skills/sdd/SKILL.md` was rewritten for readability, with an overview of the methodology and a glossary. The human's simplifications are kept: no per-mode model choice, no local-only mode, and a missing technology skill stops the dispatch until the human installs it.

**Discover runs for S, M and L, never for T.** This replaces "L only; for M the brief is written in Specify" (§5). Discover is led by the human through a question loop:

1. The hub dispatches product-lead. It reads the request, the constitution, `product.md`, related specs and ADRs, and the cartographer's note.
2. product-lead writes its questions to a file. There is **no limit** on the number of questions or rounds; this replaces "at most 3 intent questions, one round, only if ambiguous". The rule is: ask every question whose answer would change the brief, and never ask what you can find yourself (`product.md`, the code, the cartographer's note, the researcher). Each question has a recommended answer. Questions are batched and grouped by topic to keep rounds few.
3. The hub passes the questions to the human unchanged and records the answers word for word in `decisions.md`. It does not re-explain the problem.
4. A fresh product-lead reads the request and the full question-and-answer history from the files, and either asks more questions or drafts `brief.md`.
5. The loop ends when product-lead has no open questions, or when the human says "use your recommendations for the rest".
6. The human approves `brief.md`. This is a recorded decision entry in `decisions.md`. If changes are requested, product-lead revises and the human approves again. The challenger no longer reviews the brief.

Kept from the current design: product-lead can route research questions to the researcher, escalates technology constraints for `stack.yaml`, and reports triage signals.

**Human decisions: all kept, plus the new ones.** The human is involved whenever there is a real decision to make. Every existing point where the workflow waits for the human stays, and the brief approval and G1 acceptance above are added:

- intent: brief approval (Discover) and G1 (Specify);
- G2 foundations, for one-way doors in any class;
- G3 production, then the human's merge of the feature;
- spend or new resources (platform-engineer `env-plan`);
- risk acceptance, when a critical or major finding is deferred;
- scope changes beyond the approved spec, and legal questions (licenses, regulated data);
- deadlock, when the review cap is exhausted with no neutral arbiter;
- incident mitigation, presented immediately;
- external writes (`/sdd sync`);
- installing a missing technology skill (the dispatch waits);
- confirming technology constraints the human stated, before they become `fixed: true` in `stack.yaml`;
- methodology proposals from the retro;
- merging the PRs for class T, follow-up branches and incidents.

**Reviews: fewer reviewers and fewer rounds, and only where tests and `sdd.py trace` can't check.**

| Phase | Decision |
|---|---|
| Discover | The human approves the brief (above) |
| Specify | No agent review panel. The human accepts the requirements and acceptance criteria at G1. G1 gets lighter, because the brief was already agreed |
| Design | The challenger reviews for S, M and L, up to 3 rounds. The security or reliability reviewer joins only when that lens is active. G2 stays for one-way doors |
| Plan | No panel. `sdd.py trace --phase plan`, plus the test-engineer's own check while writing the test plan. Untestable acceptance criteria go back to product-lead as change requests |
| Build | Tests first, plus one code review per task. Re-review only for a critical finding |
| Verify | Test evidence, plus one review of the whole feature |

**Guard and trace script: more freedom.**
- `guard.py` stays a PreToolUse hook but flips from an allowlist to a short **denylist**. Every agent's calls are approved automatically, including any file, any command and chaining. The guard denies only what is irreversible or the human's to decide: committing to or merging into main, force-pushing, deleting remote branches, production deploys, infrastructure applies, destructive deletes, and writes to outside systems (those go through `/sdd sync`). Per-agent write ownership is no longer enforced mechanically; it stays a rule in the agents' instructions. The hub's "simple git forms" rule in `SKILL.md` can then be removed.
- `sdd.py` stays (zero tokens; it replaces the Plan review panel; `expected-failing` defines "green" in test-first Build) but becomes **advisory**: violations become findings the owner fixes, not a hard block on the phase. Re-evaluate after testing.

**Dispatches are real handoffs.** The hub writes each dispatch the way a lead hands work to a colleague: plain natural language with as much context as possible. That covers the goal, why this step is happening now, what happened just before (earlier rounds, decisions the human made, assumptions overturned), the human's own words where relevant, what is blocked on this work, what "done" looks like, and what happens next. The identifiers (mode, spec folder, artifact@version, round, task ID, branches, lens, technology skills) are woven into that text, not sent as a bare list. Two limits:
- Context that lives in a file is passed as the file's path, never pasted in.
- Reviewers get the same rich context except the author's envelope, summary or reasoning.

`SKILL.md` ("How to dispatch an agent", step 2) and the "Pass" column of `dispatch.md` change to describe this.

**After every return:**
- Routing gains the Discover loop. When product-lead returns questions, the hub asks the human, records the answers word for word in `decisions.md`, and dispatches a fresh product-lead. When the brief is ready, the hub asks the human to approve it.
- The stack check widens into a **changed-files check**. Before committing, the hub reviews the changed files (`git status`) and confirms the agent touched only files it owns, plus that no `fixed: true` entry in `stack.yaml` changed. It replaces the ownership enforcement the guard no longer does.
- `communication.md` drops the "max 3" limit on intent questions.

Consequences to apply later: remove the modes that only existed for the dropped panels (test-engineer `testability-review` and `plan-review`, reliability-engineer `nfr-review`, architect `plan-review`, consultant `specify-review` and `plan-review`), and shrink the arbiter, second-opinion and deadlock rules.

**Open questions:**
- What Discover covers.
- Whether to merge S and M. With the decisions above they run the same phases and differ only in depth: brief length, a separate test plan, a lite or full release, and the follow-up outcome and retro.

**Resolved when applying (2026-10-09):** the hub passes a worktree for test tasks, code reviews and the Build-time UX review again; the hub adds lenses and raises the class mid-flight; in Build and Verify, specialists review only when their lens is active, and product-lead's acceptance review and the architect's conformance check are dropped; model-per-mode marks and local-only support are removed everywhere (the stage 2 fixture gets a local bare repository as `origin`); the `setup` entry type stays for a missing technology skill; `hooks/ownership.json` is deleted.

## 10. Rebuild from scratch: roster and capabilities (agreed 2026-10-10, not yet applied)

The communication map showed too many conversations to scale. The methodology is rebuilt from the simplest version and grown one step at a time.

**Roster: 16 agents → 7.** Kept: product-lead, ux-designer, researcher, architect, challenger, engineer, librarian.
- Merged into **engineer**: test-engineer, code-reviewer, platform-engineer, security-engineer, reliability-engineer. Independence comes from separate dispatches, not separate personas: tests are written in a dispatch that never reads the implementation, and code is reviewed by a different dispatch than the one that wrote it, never seeing the author's reasoning.
- **tech-lead** removed: the architect writes the task plan as the last part of the design; an engineer integrates; the hub schedules ready tasks.
- Removed: cartographer (the architect reads existing code itself), consultant and all lens skills (later), incident-responder.
- The reliability design concerns (service levels, capacity, failure modes) belong to the architect.

**No agent modes.** Every agent is a generic persona: who it is, what it is responsible for, its boundaries, how it reports. How to do each job lives in skills; the hub's handoff names the skills to load for the job.

**Agents communicate only through artifacts.** One agent reads another's files (e.g. the architect reads the product-lead's); nobody talks to another agent directly.

**Commands:** only the core ones stay; `init`, `adopt`, `incident`, `retro`, `sync`, `gates` and `feature` are dropped for now.

**Target flow (agreed 2026-10-10):** the full design is in `docs/rebuild-plan.md`. Key points: product-lead owns the brief and the requirements, both non-technical, each approved by the human (`ux.md` approved with the requirements); the architect writes the design with a full task list, the challenger reviews it (up to 3 rounds), then the architect writes a detailed per-task plan without code; the engineer follows strict TDD per task (write tests → review → implement → review → merge, each a separate dispatch with its own skill); after Verify the librarian updates all documentation, including the product and architecture overviews; the human merges. ADRs and the other useful files stay. Classes: T and standard. Commands: `/sdd new` and `/sdd`.
