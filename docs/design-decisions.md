# SDD plugin — design decisions and review backlog

This file records every design decision behind the agent organization, so the complete system can be reviewed as a whole before testing and refinement.

- **Agreed** = decided together during the design conversation.
- **Default** = chosen while building the remaining capabilities (2026-10-06), using the established patterns. Each default is a candidate for review.

## 1. Architecture (agreed)

- Roles are agents; expertise is skills (`practice-*`, `stack-*`, `lens-*`); quality lenses are reviewer agents; phases are the hub's state machine; tools are CLIs, MCP servers and hooks.
- Hub-and-spoke: the main session runs `/sdd` and dispatches agents. Agents communicate only through artifacts and a strict return envelope. Agents don't dispatch other agents (policy).
- Contracts (`sdd-contracts`): artifacts and traceability IDs; findings schema and review rules; autonomy classes D0–D3; workflow with triage classes T/S/M/L, phase micro-cycle, loop caps (2 rounds for S/M, 3 for L; 3 fix attempts) and exit checks.
- Human gates only for D3: G1 intent, G2 foundations (the architect presents every option; **the human decides**), G3 production, risk acceptance, scope change, legal, deadlock, constitution changes, spend, external writes.
- Ownership guard (PreToolUse hook) enforces each agent's writes, shell commands and MCP access, and **auto-approves in-policy actions** (off switch: `permissions.auto_approve: false`). Runtime dependencies are enforced against `.sdd/dependencies.yaml`.
- Traceability script `sdd.py` (trace and stale checks).

## 2. Per-agent decisions

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
| External writes go through an outbox with one batched human approval per stop; only `sdd/*` pushes and draft PRs stay autonomous | Default |
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

## 6. Review backlog (before testing)

From the human's instructions for the review phase:

1. ~~Reuse existing skills~~: done as the skills review (§4). Selecting external stack skills is a separate, later step.
2. **End-to-end workflow review.** Walk every class (T, S, M, L) and every path (greenfield init, adopt, feature, incident, retro) through the dispatch table and contracts. Look for missing handoffs, ownership gaps, circular waits and duplicated reviews.
3. ~~Agent review~~: done (§5).
4. **Assets review.** All templates, skills, prompts, the hub, the guard policies and `sdd.py`, for consistency of names, IDs, paths and modes.
5. **Capability and dependency gaps** across the whole system. Known candidates:
   - Frontend stack skills: `stack-typescript` and framework skills, possibly reused from existing skills.
   - Cloud stack skills, once a hosting platform is chosen.
   - Brain-vault integration for the librarian.
   - Issue-tracker connectors for the sync outbox.
   - Local platform tooling: actionlint, hadolint, trivy, syft, gitleaks, OpenTofu, pre-commit, Docker.
   - Packaging: rename to sdd-kit, README, version, marketplace entry.
6. **Then testing**, systematically and with the complete system.
