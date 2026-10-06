# Contract 1 — Artifacts & traceability

## Layout

```
<project>/
├── .sdd/
│   ├── constitution.md          # principles, non-negotiables, Definition of Done (human)
│   ├── config.yaml              # loop caps, triage signals, lens triggers, environments, sync (human)
│   ├── active                   # folder name of the active feature (hub)
│   ├── state.yaml               # project-level state for init/adopt (hub)
│   ├── product/                 # product-lead: vision.md, personas.md (PER-nn), glossary.md; ux-designer: design-system.md
│   ├── stack.yaml               # architect + human: the project's technologies and the skills to load for each
│   ├── commands.yaml            # platform-engineer: project command registry by purpose (read by the guard)
│   ├── architecture/            # architect: overview.md, conventions.md, fitness.md (FF-nn), debt.md (DEBT-nn)
│   ├── operations/              # reliability-engineer: slos.md (SLO-nn), capacity.md
│   ├── dependencies.yaml        # security-engineer: approved runtime dependencies (guard-enforced)
│   ├── map/                     # cartographer: codebase map of existing code (structure, data, integrations, …)
│   ├── research/                # researcher: project-level research notes
│   ├── briefs/                  # researcher: stack briefs for stacks without a skill
│   ├── spikes/                  # architect: SPK-nn-<slug>/ throwaway experiments
│   ├── incidents/               # incident-responder: INC-nnn-<slug>/ incident.md, postmortem.md
│   ├── knowledge/               # librarian: lessons.md (LES-nn), decisions.md, faq.md, outbox/
│   ├── improvements.md          # librarian: methodology improvement proposals (MIP-nn)
│   ├── gates/                   # project-level decision packages (G2 stack, …)
│   ├── reviews/                 # reviews of project-level artifacts
│   └── log.md                   # project-level decision log
├── docs/
│   ├── adr/                     # architect: ADR-NNNN-<slug>.md
│   ├── runbooks/                # platform-engineer
│   └── …                        # librarian: guide/, api/, dev/
└── specs/NNN-<slug>/            # one folder per feature; NNN → feature ID F<NNN>
    ├── state.yaml               # hub durable state (resumable)
    ├── context.md               # cartographer: current behavior of existing code (brownfield)
    ├── brief.md                 # product-lead: problem, users, success metrics, non-goals
    ├── requirements.md          # product-lead: REQ / NFR / AC
    ├── research/                # researcher: Q-nn research notes
    ├── ux.md, prototypes/       # ux-designer: flows, screens, states; low-fi HTML prototypes
    ├── design.md, contracts/    # architect: design; OpenAPI / AsyncAPI / JSON Schema
    ├── threat-model.md          # security-engineer (security lens)
    ├── lens-<lens>.md, evals.md # consultant: lens analyses
    ├── tasks.md                 # tech-lead: T-nn dependency graph
    ├── test-plan.md             # test-engineer
    ├── perf-plan.md             # reliability-engineer: load profiles, resilience experiments
    ├── evidence/                # test-engineer (+ security/, reliability/ subfolders): Verify evidence pack
    ├── release.md               # platform-engineer
    ├── retro.md                 # librarian
    ├── trace.md                 # GENERATED — never edit
    ├── reviews/                 # <phase>-<agent>[-<lens>]-r<n>.md
    ├── gates/                   # G1/G2/G3 and risk-* decision packages
    └── log.md                   # append-only autonomous decision log
```

Class T work has no spec folder; it is recorded in a commit and in `.sdd/log.md`.
Class S work uses only `state.yaml`, `requirements.md` (REQ + AC), `reviews/`, `log.md`.

## Ownership

| Artifact | Owner | Reviewers |
|---|---|---|
| .sdd/product/vision, personas, glossary | product-lead | challenger |
| .sdd/product/design-system.md | ux-designer | challenger |
| brief.md, requirements.md | product-lead | challenger, test-engineer (testability), reliability-engineer (NFRs), active lenses |
| ux.md, prototypes/ | ux-designer | challenger, test-engineer (testability of accessibility and states) |
| research/, .sdd/research/, .sdd/briefs/ | researcher | the asking agent |
| context.md, impact-*.md, .sdd/map/ | cartographer | — |
| .sdd/stack.yaml | architect (entries with `fixed: true` are written only by the human and never changed by agents) | challenger (G2 fairness), human (G2) |
| .sdd/commands.yaml | platform-engineer | architect (D2); takes effect once committed |
| design.md, contracts/*, docs/adr/*, .sdd/architecture/*, .sdd/spikes/* | architect | challenger, security-engineer, reliability-engineer, active lenses |
| threat-model.md, .sdd/dependencies.yaml, tests/security/ | security-engineer | architect |
| .sdd/operations/*, perf-plan.md | reliability-engineer | architect, test-engineer |
| lens-*.md, evals.md | consultant | owners of the affected artifacts |
| tasks.md | tech-lead | test-engineer, architect, challenger (L) |
| test-plan.md, acceptance/contract/e2e/perf tests, evidence/ | test-engineer | code-reviewer |
| source code, unit/integration tests, migrations | engineer | code-reviewer, active lenses |
| infra, CI, containers, dev container, runbooks, release.md | platform-engineer | code-reviewer (tasks), reliability-engineer (release) |
| .sdd/incidents/* | incident-responder | reliability-engineer |
| README, docs/ (except adr, runbooks), .sdd/knowledge/*, .sdd/improvements.md, retro.md | librarian | — |
| gates/* | the preparing agent (G1 product-lead, G2 architect, G3 platform-engineer, risk-* security-engineer or the deferring owner, incident mitigation incident-responder); the hub records only `status`, `decided-by`, `decided-on` and the Decision section | challenger (G2 fairness) |
| state.yaml, .sdd/active, trace.md | hub | — |
| log.md | append-only by any agent | — |
| .sdd/constitution.md, .sdd/config.yaml | human (D3; changes proposed via MIPs) | — |

Only the owner edits an artifact. Anyone else files a finding (see communication.md) with `route_to: <owner>`.

## Frontmatter (every artifact except state.yaml, trace.md, log.md)

```yaml
---
artifact: design            # brief | requirements | ux | design | threat-model | tasks | test-plan | release | adr | review | gate
feature: F003
owner: architect
status: draft               # draft | in-review | approved | superseded
version: 3                  # integer, bumped on every change after first review
upstream: [requirements.md@2, ux.md@1]   # versions this version was built against
---
```

### Staleness

If an upstream artifact's `version` is greater than the version recorded in a downstream artifact's `upstream:` list, the downstream artifact is **stale**. A stale artifact must be re-validated by its owner (bump `upstream:` if still valid, otherwise revise) before any phase exit check passes. Only the affected chain is reopened.

## ID scheme

IDs are local to a feature; fully qualified across features as `F003:REQ-02`. IDs are never reused.

| ID | Meaning | Defined in | Must link to |
|---|---|---|---|
| `REQ-nn` | Functional requirement (EARS form) | requirements.md | — |
| `NFR-nn` | Non-functional requirement, measurable | requirements.md | `verify:` method |
| `AC-nn.m` | Acceptance criterion (Given/When/Then); `nn` = parent REQ | requirements.md | parent REQ (implicit) |
| `UX-nn` | Flow or screen | ux.md | REQ |
| `C-nn` | Component | design.md | REQ / NFR |
| `IF-nn` | Interface / contract | design.md | REQ / NFR |
| `THR-nn` | Threat | threat-model.md | C / IF |
| `T-nn` | Task | tasks.md | REQ / AC, or `enabler` |
| `Q-nn` | Open question (with default) | any | — |
| `ASM-nn` | Assumption | any | — |
| `RISK-nn` | Risk (incl. deferred findings) | any | — |
| `ADR-NNNN` | Architecture decision (global, 4 digits) | docs/adr/ | features |
| `PER-nn` | Persona (global) | .sdd/product/personas.md | — |
| `FF-nn` | Fitness function (global) | .sdd/architecture/fitness.md | ADR / NFR |
| `DEBT-nn` | Technical debt item (global) | .sdd/architecture/debt.md | ADR / finding |
| `SPK-nn` | Spike (global) | .sdd/spikes/SPK-nn-*/README.md | Q / design |
| `SLO-nn` | Service level objective (global) | .sdd/operations/slos.md | NFRs |
| `INC-nnn` | Incident (global) | .sdd/incidents/INC-nnn-*/ | — |
| `LES-nn` | Lesson learned (global) | .sdd/knowledge/lessons.md | retro / incident |
| `MIP-nn` | Methodology improvement proposal (global) | .sdd/improvements.md | retro evidence |

### How links are carried outside artifacts

- **Tests** reference the AC (or NFR) they verify with its fully qualified ID (`F003:AC-02.1`), using the test framework's tagging mechanism (marker, tag, annotation) or the test's name, placed **directly above or in** the test definition. The trace script finds the ID in test files and maps it to the nearest following test definition; JUnit-format results link it to pass/fail.
- **Commits** carry a trailer: `Refs: F003:T-04` (multiple allowed, comma-separated).

## Markup conventions (machine-readable)

The trace script depends on these; follow them exactly.

1. **Definition** — an ID is defined by a markdown heading (level 2–4) that starts with the ID:
   ```markdown
   ### REQ-02: User can reset password
   ### AC-02.1: Expired token is rejected
   ### T-04: Implement token issuance
   ```
   Everything until the next heading of the same or higher level is that item's block.
2. **Withdrawn** — append `[withdrawn]` to the heading: `### REQ-05: Magic links [withdrawn]`.
3. **Links** — inside the block, a line `refs: REQ-02, NFR-01`.
4. **Task fields** — `depends: T-01, T-02` and, for tasks with no requirement, `refs: enabler`.
   Also `surface: <backend|frontend|data|infra|…>` and `stack: <technologies involved>`.
5. **NFR verification** — `verify: load test against staging, p95 < 200ms @ 100 rps` (or reference an NFR from a test).

## Traceability rules (checked by `sdd.py trace`)

| Rule | Checked from phase |
|---|---|
| No duplicate IDs; every `refs:` target is defined | specify |
| Every REQ has ≥1 AC | specify |
| Every NFR has a `verify:` line or is referenced by a test | specify |
| Every REQ/NFR is referenced by ≥1 C/IF | design |
| Every task has `refs:` (or `enabler`); every AC is covered by a task (directly or via its REQ) | plan |
| Task `depends:` graph has no cycles | plan |
| Every AC is referenced by ≥1 test; with `--junit`, those tests pass | verify |
| No stale artifacts | all |
