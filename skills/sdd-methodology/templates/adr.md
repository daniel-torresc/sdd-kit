---
artifact: adr
id: ADR-[NNNN]
title: [Decision title]
status: [proposed | accepted | superseded | deprecated]
decided-by: [human | design]
decision: [decisions.md#H-nn, when the human decided]
date: [YYYY-MM-DD]
features: [feature IDs]
supersedes: []
superseded-by: []
---

# ADR-NNNN: <short title stating the problem and the chosen solution>

> Records one architecturally significant decision: the problem, the options considered, the choice made, and its consequences.
> ADRs belong to the project, not to a feature: they live in `docs/adr/`, are numbered across the whole project, and outlast the feature that wrote them.
> Once accepted, an ADR is never rewritten. A later decision that changes it is a new ADR that supersedes it.

---

## 1. Context and Problem Statement

Describe the forces at play and the problem to decide, in two or three sentences. State it as a question when that makes it clearer.

Reference the requirements, constraints, and earlier decisions involved. Requirement IDs from a feature carry the feature prefix, such as `F003:REQ-02`.

---

## 2. Decision Drivers

List the forces, constraints, and quality attributes the decision must satisfy.

- [Driver, with its source: F003:NFR-01, a constitution rule, a constraint from the brief, a fixed technology]

---

## 3. Considered Options

Describe every viable option with the same depth. Reference the research note that compares them, where there is one.

### Option A: [Name]

- **Description:** [What the option is, or a link to more information]
- **Pros:** [Arguments in favor]
- **Cons:** [Arguments against]
- **Fit:** [How well it meets the decision drivers]
- **Reversal cost:** [Low | Medium | High], [why]
- **Operational cost:** [Running, maintenance, licensing, support]

Repeat for each option.

---

## 4. Decision

Chosen option: "[Option X]", because [justification].

When the human made the decision, record their reasons in their own words and reference their entry in the decisions record.

---

## 5. Consequences

Describe what the decision makes easier, harder, or required.

- **Positive:** [Consequence]
- **Negative:** [Consequence, or new risk]
- **Required:** [New obligation, constraint, or follow-up work]

---

## 6. Confirmation

Describe how compliance with this decision will be verified: a review checklist item, an automated architecture test, a fitness function, or another check.

---

## 7. More Information

Reference the related ADRs, the research notes, and the evidence behind the decision.

State when, or under which conditions, this decision should be revisited.

---

## 8. Maintenance Guidelines

An ADR is immutable once accepted.

- Its content is never rewritten. Only its `status` and `superseded-by` change, when it is superseded or deprecated.
- A change to the decision is a new ADR, which lists this one in `supersedes`.
- A proposed ADR may be revised freely until it is accepted.

### Source of Truth

- This document is the canonical record of this decision and its reasoning.
- `architecture.md` summarizes the decisions that shape the system and references their ADRs.
- `stack.yaml` records the technologies chosen, and references the ADR that chose them.
- The decisions record of the feature holds the human's answer, when the human decided.
