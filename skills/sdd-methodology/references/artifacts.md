# Contract 1 — Artifacts & traceability

## Layout

```
<project>/
├── .sdd/
│   ├── constitution.md          # principles, non-negotiables, Definition of Done
│   ├── config.yaml              # loop caps, triage signals, lens triggers, stack routing
│   ├── product/                 # product-level context, owned by product-lead
│   │   ├── vision.md            # why the product exists, for whom, strategy
│   │   ├── personas.md          # PER-nn user types
│   │   └── glossary.md          # canonical domain terms
│   ├── gates/                   # project-level decision packages (e.g. stack G2)
│   ├── reviews/                 # reviews of project-level artifacts (product context, stack ADRs)
│   ├── architecture/            # project architecture, owned by architect
│   │   ├── overview.md          # context/container diagrams, module map
│   │   ├── conventions.md       # layout, coding/API conventions, stack profile (skill routing)
│   │   ├── fitness.md           # FF-nn architecture rules enforced in CI
│   │   └── debt.md              # DEBT-nn technical debt register
│   ├── dependencies.yaml        # approved runtime dependencies (guard-enforced for engineers)
│   ├── spikes/                  # SPK-nn-<slug>/ throwaway experiments (never imported by product code)
│   └── briefs/                  # researcher stack briefs (skill candidates)
├── docs/adr/                    # ADR-NNNN-<slug>.md — project-wide, outlive features
└── specs/NNN-<slug>/            # one folder per feature; NNN → feature ID F<NNN>
    ├── state.yaml               # hub durable state (resumable)
    ├── brief.md                 # problem, users, success metrics, non-goals
    ├── requirements.md          # REQ / NFR / AC
    ├── ux.md                    # flows, screens, states (if UI)
    ├── design.md                # components, interfaces, data model, NFR budgets
    ├── contracts/               # OpenAPI / AsyncAPI / JSON Schema (required for external/public IFs)
    ├── threat-model.md          # if security lens active
    ├── tasks.md                 # T-nn dependency graph
    ├── test-plan.md             # test levels, AC → test mapping
    ├── evidence/                # Verify evidence pack: JUnit reports, NFR measurements, screenshots, README.md
    ├── trace.md                 # GENERATED — never edit
    ├── reviews/                 # <phase>-<agent>-r<n>.md
    ├── gates/                   # G<n>-<slug>.md human decision packages
    ├── log.md                   # append-only autonomous decision log
    └── release.md
```

Class T work has no spec folder; it is recorded in a commit and in `.sdd/log.md`.
Class S work uses only `state.yaml`, `requirements.md` (REQ + AC), `reviews/`, `log.md`.

## Ownership

| Artifact | Owner | Reviewers |
|---|---|---|
| .sdd/product/* | product-lead | challenger |
| brief.md, requirements.md | product-lead | challenger, test-engineer (testability) |
| ux.md | ux-designer | challenger, a11y lens |
| design.md, contracts/*, docs/adr/* | architect | challenger, security-engineer, reliability-engineer |
| .sdd/architecture/*, .sdd/spikes/* | architect | challenger |
| .sdd/dependencies.yaml | security-engineer (architect may add `provisional` entries until security-engineer exists) | — |
| threat-model.md | security-engineer | architect |
| tasks.md | tech-lead | test-engineer, architect |
| test-plan.md, acceptance/contract/e2e/perf tests, evidence/ | test-engineer | code-reviewer |
| unit tests | engineer | code-reviewer |
| source code, unit/integration tests, migrations | engineer | code-reviewer + active lenses |
| infra, CI, containers, dev container, runbooks, release.md | platform-engineer | code-reviewer (tasks), reliability-engineer or architect (release) |
| gates/G<n>-* | the preparing agent (G1 product-lead, G2 architect, G3 platform-engineer); the hub records only `status`, `decided-by`, `decided-on` and the Decision section | — |
| state.yaml, trace.md | hub | — |
| log.md | append-only by any agent | — |
| .sdd/constitution.md | human (D3) | — |

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

### How links are carried outside artifacts

- **Tests** reference the AC (or NFR) they verify with its fully qualified ID:
  - Python: `@pytest.mark.ac("F003:AC-02.1")` directly above the test function.
  - Other stacks: the ID in the test name or a tag/comment inside the test, e.g. `it("F003:AC-02.1 rejects expired token", …)`.
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
   Also `surface: backend` and `stack: python, fastapi`.
5. **NFR verification** — `verify: load test k6, p95 < 200ms @ 100 rps` (or reference an NFR from a test).

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
