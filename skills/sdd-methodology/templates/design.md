---
artifact: design
feature: [feature ID]
status: [draft | approved | superseded]
version: [version]
upstream: [brief.md@version, requirements.md@version]
---

# Design: <feature name>

> Describes how a feature will be built: the components and interfaces it adds or changes, its data, the technologies it uses, how it meets its qualities and handles failure, and the tasks that will build it.
> Once approved, it is the approach every task is built and reviewed against. It must meet the approved requirements; it never changes them.
> Describe the feature's change to the system, not the whole system: the architecture description holds the system as a whole and is brought up to date in Document.

---

## Conventions

Every component and interface is defined by a heading that starts with its ID:

- Components: `### C-01: [Name]`
- Interfaces: `### IF-01: [Name]`

Each one names, in its **Covers** field, the requirements and non-functional requirements it serves. Every requirement and non-functional requirement MUST be covered by at least one component or interface.

IDs MUST remain stable once referenced by other artifacts. A withdrawn item keeps its ID and its heading, with `[withdrawn]` appended. Withdrawn IDs are never reused.

Assumption (`ASM`), open-question (`OQ`) and risk (`RISK`) IDs continue the numbering already used in the feature's brief and requirements.

---

## 1. Context

Describe the starting point this design builds on.

- The parts of the existing system the feature touches, as they are today. For a new system, the starting point.
- The sections of `architecture.md` and the ADRs that apply.
- The constraints the design must respect: the brief's constraints, the constitution's rules, and the technologies fixed in `stack.yaml`.

Reference these sources rather than restating them.

---

## 2. Overview

Explain, in one or two paragraphs, how the feature works as a whole: the main components, how they interact, and the principal flow.

Include a diagram where it makes the structure or the flow easier to understand.

---

## 3. Components

Describe each component the feature adds or changes. Document components according to meaningful responsibilities, not every class, function, or file.

### C-01: [Component name]

- **Responsibility:** [What it does, in one sentence]
- **Covers:** [REQ-nn, NFR-nn]
- **Status:** [New | Changed | Existing, used as is]
- **Owns:** [The data or state it owns, where applicable]
- **Depends on:** [Other components, interfaces, or external systems]
- **On failure:** [How it behaves when a dependency or its own work fails]

Repeat for each component.

---

## 4. Interfaces

Describe each interface the feature adds, changes, or relies on: APIs, events, commands, user interfaces, files, or internal boundaries between components.

For an interface used outside the feature, document everything a caller needs to know, and reference its machine-readable contract where one exists.

### IF-01: [Interface name]

- **Kind:** [API | Event | Command | User interface | File | Internal]
- **Covers:** [REQ-nn, NFR-nn]
- **Provided by:** [C-nn, or an external system]
- **Used by:** [C-nn, users, or external systems]
- **Operations:** [Each operation with its inputs, outputs, and errors]
- **Guarantees:** [Ordering, idempotency, consistency, limits, where relevant]
- **Compatibility:** [For an existing interface: what changes, and how existing callers are affected]

Repeat for each interface.

---

## 5. Data

Describe the data the feature introduces or changes.

- Entities, their relationships, and their invariants.
- Which component owns each piece of data.
- Retention, privacy, and access rules, where relevant.
- How existing data changes, and how that change is applied safely.

Omit this section only when the feature introduces or changes no data, and say so.

---

## 6. Technologies

Describe the technologies this design uses.

- **From the stack:** the `stack.yaml` concerns the feature relies on.
- **New:** any technology the feature adds, and why. A reversible choice is recorded in the stack; a hard-to-reverse choice is a one-way door, decided by the human and recorded in an ADR.
- **Skills:** the entries of the skills catalogue that apply to building and reviewing this design.

Technologies fixed in `stack.yaml` MUST NOT be changed.

---

## 7. Qualities

For each non-functional requirement, explain how the design meets it and how that will be verified. Reference each one by its ID; it is defined in the requirements, not here.

- **NFR-01:** [The design choices that meet it] Verified by: [test, measurement, inspection, or monitoring]

Repeat for each non-functional requirement. Add service levels and expected capacity where they matter to the feature.

---

## 8. Failure Modes

Identify how the feature can fail and what happens when it does. Focus on failures that affect users, data, or other parts of the system.

| Failure | How it is detected | What the system does | How it recovers |
|---|---|---|---|
| [Failure] | [Detection] | [Behavior] | [Recovery] |

---

## 9. Decisions

List the decisions this design rests on:

- **ADRs:** the ADRs written for this feature, and the existing ADRs it relies on.
- **Human decisions:** the one-way doors decided by the human, by their entry in the decisions record (`H-nn`).
- **Research:** the research notes the design relies on (`Q-nn`).

### 9.1 Alternatives Considered

For significant choices that don't warrant an ADR, record the alternatives considered and why they were not chosen.

- **[Choice]:** [Alternatives, and why the chosen approach was preferred]

---

## 10. Assumptions, Open Questions, and Risks

### ASM-01: [Assumption]

- **Basis:** [Reason or available evidence]
- **Impact if incorrect:** [What in the design would change]
- **Status:** [Unverified | Confirmed | Rejected]

### OQ-01: [Question]

- **Impact:** [What in the design depends on the answer]
- **Proposed default:** [Recommended answer, or TBD]
- **Status:** [Open | Resolved | Deferred]
- **Resolution:** [Confirmed answer or decision, when resolved]

### RISK-01: [Risk]

- **Likelihood:** [Low | Medium | High | Unknown]
- **Impact:** [Low | Medium | High | Unknown]
- **Mitigation:** [How the design reduces it, or TBD]

Repeat for each item.

---

## 11. Task List

List the tasks that will build the feature. This table is the overview the human approves with the design; each task is defined in detail, once, in the plan.

Each task MUST be small enough to build and review on its own. Every acceptance criterion MUST be delivered by at least one task. A task that delivers no acceptance criterion is an enabler, and says so.

| Task | Delivers | Acceptance criteria | Technologies | Depends on |
|---|---|---|---|---|
| T-01 | [What it delivers] | [AC-01.1, AC-01.2, or Enabler] | [stack.yaml concerns] | [T-nn, or None] |

---

## 12. Traceability and Coverage

Before this document is approved, verify that:

- Every requirement and non-functional requirement is covered by at least one component or interface.
- Every acceptance criterion is delivered by at least one task.
- Every non-functional requirement has a way to meet it and a way to verify it.
- No component or interface exists without a requirement it serves, unless it is explicitly an enabler.
- The design respects the brief's constraints, the constitution, and the technologies fixed in the stack.

Record the result:

- **Coverage gaps:** [None | Identified gaps]
- **Unresolved dependencies:** [None | Relevant questions or decisions]

---

## 13. Maintenance Guidelines

This document MUST remain aligned with the approved requirements and with the way the feature is actually being built.

Bump `version` on every change made after the first review or approval, and keep `upstream` pointing to the versions of the brief and the requirements it is built from. When either of them changes, check this design again: confirm it by updating `upstream`, or revise it.

A change to the approved approach MUST be approved again by the human. Every artifact that lists an older version of this document in its `upstream` becomes stale and MUST be checked again.

### Source of Truth

- This document is the canonical reference for how the feature is built.
- The requirements define what the feature must do; this design meets them and never changes them.
- The plan defines each task in detail; the task list here is its approved overview.
- ADRs record the significant decisions; `stack.yaml` records the technologies; `architecture.md` describes the system as a whole.

When information changes, update its authoritative source rather than maintaining competing copies across documents.
