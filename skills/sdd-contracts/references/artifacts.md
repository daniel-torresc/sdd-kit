# Contract 1 — Artifacts & traceability

The methodology runs on a **small core** of artifacts that exist in every project and every feature, plus a few **on-demand** artifacts created only when their situation arises. Every artifact has exactly one owner.

## Layout

```
<project>/
├── .sdd/
│   ├── constitution.md      # human: principles, non-negotiables, project additions to the definition of done
│   ├── config.yaml          # human: triage signals, lens triggers, loop caps, environments, sync
│   ├── stack.yaml           # architect (+ human fixed entries): technologies, their skills, and the project commands
│   ├── product.md           # product-lead: why, for whom, principles, metrics, scope, glossary
│   ├── architecture.md      # architect: how the system works, conventions, key decisions, known debt
│   ├── design-system.md     # ux-designer (on demand, products with a UI)
│   └── incidents/           # incident-responder (on demand): INC-nnn-<slug>.md
├── docs/
│   ├── adr/                 # architect: ADR-NNNN-<slug>.md
│   ├── runbooks/            # platform-engineer
│   └── …                    # librarian: user and developer docs (with README.md)
└── specs/
    ├── 000-foundation/      # project foundation (/sdd init or /sdd adopt) — a feature like any other
    └── NNN-<slug>/          # one folder per feature; NNN → feature ID F<NNN>
        ├── state.yaml       # hub: where the feature stands (readable)
        ├── brief.md         # product-lead: problem, users, success metrics, scope
        ├── requirements.md  # product-lead: REQ / NFR / AC
        ├── ux.md            # ux-designer (on demand: UI features)
        ├── research/        # researcher, cartographer, architect (on demand): investigations, spikes, technology notes
        ├── design.md        # architect: how it will be built (incl. security, data and privacy, cost)
        ├── contracts/       # architect (when there are external or public interfaces)
        ├── tasks.md         # tech-lead: the work, one task per reviewable change
        ├── test-plan.md     # test-engineer: how it will be verified (incl. performance, resilience, evaluations)
        ├── evidence/        # test-engineer (+ security-engineer, reliability-engineer): Verify results and traceability
        ├── release.md       # platform-engineer (on demand: when the feature is released)
        ├── reviews/         # reviewers: findings, and the owners' answers
        └── decisions.md     # everyone: autonomous decisions, decisions waiting for the human, human decisions
```

Class T work has no spec folder; it is recorded in a commit (and, if a decision was needed, in the hub's report).
Class S uses only `state.yaml`, `requirements.md` (REQ + AC), a short `tasks.md`, `evidence/`, `reviews/` and `decisions.md`.

## Templates

All templates live in `sdd-contracts/templates/` and are named after the artifact, except: `research.md` → `research/Q-nn-<slug>.md`, `incident.md` → `.sdd/incidents/INC-nnn-<slug>.md`, `review.md` → `reviews/<phase>-<agent>-r<n>.md`, `adr.md` → `docs/adr/ADR-NNNN-<slug>.md`, `evidence.md` → `evidence/README.md`.

## Ownership

| Artifact | Owner | Reviewers |
|---|---|---|
| constitution.md, config.yaml | human (agents propose changes as decisions) | — |
| stack.yaml | architect; `fixed: true` entries only by the human (recorded by the hub) | challenger (G2 fairness), human (G2) |
| product.md | product-lead | challenger |
| architecture.md, docs/adr/ | architect | challenger |
| design-system.md | ux-designer | challenger |
| brief.md, requirements.md | product-lead | challenger, test-engineer, reliability-engineer (NFRs), active lenses |
| ux.md | ux-designer | challenger, test-engineer |
| research/ | the investigating agent (researcher, cartographer, architect for spikes) | the asking agent |
| design.md, contracts/ | architect | challenger, security-engineer, reliability-engineer, active lenses |
| tasks.md | tech-lead | test-engineer, architect, challenger (L) |
| test-plan.md, acceptance/contract/e2e/perf tests, tests/support/, evidence/ | test-engineer | code-reviewer, reliability-engineer (performance section) |
| source code (incl. docstrings and in-code docs), unit/integration tests, migrations | engineer | code-reviewer, task `reviews:` |
| tests/security/ | security-engineer | code-reviewer |
| pipeline, infrastructure, containers, dev environment, docs/runbooks/, release.md | platform-engineer | code-reviewer, reliability-engineer (release) |
| README.md, docs/ (except adr, runbooks) | librarian | — |
| .sdd/incidents/ | incident-responder | reliability-engineer |
| reviews/ | each reviewer its own file; owners answer inside | — |
| decisions.md | append-only by every agent; entries waiting for the human are written by the preparing agent; the hub records the human's answers | challenger (G2 fairness) |
| state.yaml | hub | — |

Only the owner edits an artifact. Anyone else files a finding (communication contract) with `route_to: <owner>`.

## Frontmatter (every markdown artifact except decisions.md)

```yaml
---
artifact: design            # brief | requirements | ux | design | tasks | test-plan | release | research | product | architecture | adr | review
feature: F003
owner: architect
status: draft               # draft | in-review | approved | superseded
version: 3                  # integer, bumped on every change after first review
upstream: [requirements.md@2, ux.md@1]   # versions this version was built against
---
```

### Staleness

If an upstream artifact's `version` is greater than the version recorded in a downstream artifact's `upstream:` list, the downstream artifact is **stale**. Its owner re-validates it (bump `upstream:` if still valid, otherwise revise) before any phase exit check passes. Only the affected chain is reopened.

## ID scheme

IDs are local to a feature; fully qualified across features as `F003:REQ-02`. IDs are never reused.

| ID | Meaning | Defined in |
|---|---|---|
| `REQ-nn` | Functional requirement (EARS form) | requirements.md |
| `NFR-nn` | Non-functional requirement, measurable, with `verify:` | requirements.md |
| `AC-nn.m` | Acceptance criterion (Given/When/Then); `nn` = parent REQ | requirements.md |
| `UX-nn` | Flow or screen | ux.md |
| `C-nn` / `IF-nn` | Component / interface | design.md |
| `T-nn` | Task | tasks.md |
| `Q-nn` | Question (with default) or research note | any / research/ |
| `ASM-nn` | Assumption | any |
| `RISK-nn` | Risk (incl. deferred findings) | any |
| `G1`–`G3` / `H-nn` | Gate / other decision waiting for or taken by the human (risk, scope, legal, deadlock, external write, mitigation, methodology) | decisions.md |
| `ADR-NNNN` | Architecture decision (global) | docs/adr/ |
| `PER-nn` | Persona (global) | product.md |
| `DEBT-nn` | Technical debt (global) | architecture.md |
| `INC-nnn` | Incident (global) | .sdd/incidents/ |

### How links are carried outside artifacts

- **Tests** reference the AC (or NFR) they verify with its fully qualified ID (`F003:AC-02.1`), using the test framework's tagging mechanism or the test's name, placed **directly above or in** the test definition. The trace script maps it to the nearest following test definition; JUnit-format results link it to pass/fail.
- **Commits** carry a trailer: `Refs: F003:T-04` (multiple allowed, comma-separated).

## Markup conventions (machine-readable)

The trace script depends on these; follow them exactly.

1. **Definition** — an ID is defined by a markdown heading (level 2–4) that starts with the ID: `### REQ-02: User can reset password`, `#### AC-02.1: Expired token is rejected`, `### T-04: Implement token issuance`. Everything until the next heading of the same or higher level is that item's block.
2. **Withdrawn** — append `[withdrawn]` to the heading.
3. **Links** — design elements: `refs: REQ-02, NFR-01`. Tasks: `delivers: AC-02.1, REQ-03` or `delivers: enabler`.
4. **Task fields** — `depends`, `owner`, `files`, `stack`, `done-when`, and optionally `reviews`, `risk`, `test-first` (see the tasks template).
5. **NFR verification** — `verify: <method and threshold>` (or reference the NFR from a test).

## Traceability rules (checked by `sdd.py trace`)

| Rule | Checked from phase |
|---|---|
| No duplicate IDs; every reference is defined | specify |
| Every REQ has ≥1 AC; every NFR has `verify:` or a test | specify |
| Every REQ/NFR is referenced by ≥1 C/IF | design |
| Every task has `delivers` (or `enabler`), `owner`, `files`, `stack`, `done-when`; every AC is delivered by a task; engineer tasks depend on test-engineer tasks covering their ACs; no dependency cycles; `reviews` names are valid | plan |
| Every AC (and NFR referenced by tests) has a passing test (with `--junit`) | verify |
| No stale artifacts | all |

The script prints its result; it writes a file only when asked (`--report evidence/traceability.md` at Verify).
