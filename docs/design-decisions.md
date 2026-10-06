# SDD plugin — design decisions and review backlog

This file records every design decision behind the agent organization, so the complete system can be reviewed as a whole before testing and refinement.

- **Agreed** = decided together during the design conversation.
- **Default** = chosen while building the remaining capabilities (2026-10-06), using the established patterns. Each default is a candidate for review.

## 1. Architecture (agreed)

- Roles are agents; expertise is skills (`practice-*`, `stack-*`, `lens-*`); quality lenses are reviewer agents; phases are the hub's state machine; tools are CLIs, MCP servers and hooks.
- Hub-and-spoke: the main session runs `/sdd` and dispatches agents. Agents communicate only through artifacts and a strict return envelope. Agents don't dispatch other agents (policy).
- Contracts (`sdd-methodology`): artifacts and traceability IDs; findings schema and review rules; autonomy classes D0–D3; workflow with triage classes T/S/M/L, phase micro-cycle, loop caps (2 rounds for S/M, 3 for L; 3 fix attempts) and exit checks.
- Human gates only for D3: G1 intent, G2 foundations (the architect presents every option; **the human decides**), G3 production, risk acceptance, scope change, legal, deadlock, constitution changes, spend, external writes.
- Ownership guard (PreToolUse hook) enforces each agent's writes, shell commands and MCP access, and **auto-approves in-policy actions** (off switch: `permissions.auto_approve: false`). Runtime dependencies are enforced against `.sdd/dependencies.yaml`.
- Traceability script `sdd.py` (trace and stale checks).

## 2. Per-agent decisions

| Agent | Agreed | Default (to review) |
|---|---|---|
| product-lead | `.sdd/product/` context; acceptance review in Verify; hybrid intent questions (≤3 before drafting); preparer writes the gate file | — |
| challenger | G2 fairness review; risk ranking orders G1 assumptions; findings budget; second-opinion mode | — |
| architect | `.sdd/architecture/`; machine-readable contracts for external/public interfaces; spikes; baseline stack as "option A to beat"; one-page G2 brief | Lists runtime dependencies in `design.md` for security vetting; testability seams in every design |
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
| librarian | — | sonnet; owns README and `docs/` (except ADRs and runbooks), the knowledge base, retros and methodology improvement proposals (MIPs); promotes proven stack briefs to `.claude/skills/stack-*` after architect review (D2); external knowledge sync opt-in |
| incident-responder | — | opus; SEV1–4; recommends mitigation, **the human executes**; fast-path presentation; blameless postmortems for SEV1–2; every action item routed to an owner |
| consultant | — | One generic agent plus five lens skills (accessibility, data-migration, ai-evals, finops, api-compat), selected per dispatch; opus |

## 3. Hub decisions

| Decision | Status |
|---|---|
| `/sdd` runs autonomously until a human decision or blocker; push notification on stop; gates as one-screen summary + AskUserQuestion; artifacts committed after every step; agent worktree cleanup after integration | Agreed |
| Subcommands `adopt`, `incident`, `retro`, `sync`; Evolve runs automatically after deploy | Default |
| Lens activation from `lens_triggers`; class L activates every plausible lens; new triggers found mid-flight add lenses and can raise the class | Default |
| External writes go through an outbox with one batched human approval per stop; only `sdd/*` pushes and draft PRs stay autonomous | Default |
| Fallbacks for missing agents removed; every role now has its agent | Default (follows the complete-system principle) |

## 4. Review backlog (before testing)

From the human's instructions for the review phase:

1. **Reuse existing skills.** Inventory the human's existing skills (Python coding, architecture patterns, other practices) and decide, per overlap, whether to reuse, merge or drop the plugin's version: `stack-python`, `practice-architecture`, `practice-engineering`, `practice-security-basics`, `practice-testing`, and the others.
2. **End-to-end workflow review.** Walk every class (T, S, M, L) and every path (greenfield init, adopt, feature, incident, retro) through the dispatch table and contracts. Look for missing handoffs, ownership gaps, circular waits and duplicated reviews.
3. **Agent review.** For every agent, check responsibilities, inputs, outputs, interactions, boundaries, guard policy versus instructions, and model and effort.
4. **Assets review.** All templates, skills, prompts, the hub, the guard policies and `sdd.py`, for consistency of names, IDs, paths and modes.
5. **Capability and dependency gaps** across the whole system. Known candidates:
   - Frontend stack skills: `stack-typescript` and framework skills, possibly reused from existing skills.
   - Cloud stack skills, once a hosting platform is chosen.
   - Brain-vault integration for the librarian.
   - Issue-tracker connectors for the sync outbox.
   - Local platform tooling: actionlint, hadolint, trivy, syft, gitleaks, OpenTofu, pre-commit, Docker.
   - Packaging: rename to sdd-kit, README, version, marketplace entry.
6. **Then testing**, systematically and with the complete system.
