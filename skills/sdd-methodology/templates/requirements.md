---
artifact: requirements
feature: [feature ID]
status: [draft | approved | superseded]
version: [version]
upstream: [brief.md@version]
---

# Requirements: <feature name>

> Defines the observable behavior a feature must provide, the acceptance criteria that demonstrate it, and the quality attributes it must meet.
> Once approved, these requirements and the brief they are built from are the contract every later artifact of the feature is checked against.
> Describe WHAT the system must do, never HOW it is built. Keep requirements verifiable and traceable, without duplicating the brief, the design, or project-level documentation.

---

## Conventions

Every requirement, acceptance criterion, and non-functional requirement is defined by a heading that starts with its ID:

- Functional requirements: `### REQ-01: [Title]`
- Acceptance criteria: `#### AC-01.1: [Title]`. `AC-nn.m` belongs to `REQ-nn`.
- Non-functional requirements: `### NFR-01: [Title]`

IDs MUST remain stable once referenced by other artifacts. A withdrawn item keeps its ID and its heading, with `[withdrawn]` appended. Withdrawn IDs are never reused.

Assumption (`ASM`), open-question (`OQ`) and risk (`RISK`) IDs are shared by the whole feature: continue the numbering already used in the brief; never restart at 01.

---

## 1. Functional Requirements

Define the observable behavior the system must provide.

Each requirement MUST:

- Express one coherent, independently identifiable obligation.
- Describe what the system must do, not how it must be implemented.
- Be unambiguous and verifiable.
- Have a priority.
- Include acceptance criteria that demonstrate compliance.

Use the smallest useful set of requirements. Avoid duplicating requirements or combining unrelated obligations into one item.

Express each requirement with the EARS pattern that states it most clearly:

- **Ubiquitous:** The [system] shall [response].
- **Event-driven:** When [trigger], the [system] shall [response].
- **State-driven:** While [state], the [system] shall [response].
- **Unwanted behavior:** If [condition], then the [system] shall [response].
- **Optional feature:** Where [feature or condition applies], the [system] shall [response].

Do not force every requirement into the same form when another is clearer.

Use acceptance criteria to clarify expected behavior under relevant conditions, including boundary cases and failure scenarios. Acceptance criteria MUST be observable and verifiable. Avoid implementation prescriptions unless they represent an explicit constraint.

### REQ-01: [Short title]

[Requirement statement, using an EARS pattern.]

- **Priority:** [Must | Should | Could]
- **Source:** [Brief section, decision, or other upstream source]
- **Rationale:** [Why this requirement matters, if not self-evident]

#### AC-01.1: [Short title]

- **Given** [Initial context or preconditions]
- **When** [Trigger or action]
- **Then** [Observable, verifiable outcome]

Repeat for each acceptance criterion of the requirement, and for each requirement.

---

## 2. Non-Functional Requirements

Define measurable quality attributes and feature-wide constraints that cannot be adequately expressed as individual functional requirements.

Examples include performance, reliability, security, privacy, accessibility, usability, compatibility, maintainability, and resource consumption.

Include only qualities relevant to this feature. Consider the relevant quality attributes before concluding that none apply.

Every non-functional requirement MUST state how compliance will be verified. Define a measurable target where feasible, and distinguish confirmed targets from provisional ones.

If a quality obligation is already established by `constitution.md` or another authoritative project artifact, reference it rather than creating a conflicting or redundant requirement.

### NFR-01: [Short title]

The [system] shall [measurable quality property].

- **Priority:** [Must | Should | Could]
- **Source:** [Brief section, project artifact, policy, or other source]
- **Target:** [Measurable threshold, defined condition, or TBD]
- **Conditions:** [Relevant workload, environment, operating conditions, or scope]
- **Verify:** [Test, measurement, inspection, audit, monitoring, or other verification method]
- **Rationale:** [Why this quality attribute matters, if not self-evident]
- **Status:** [Confirmed | Provisional]

Repeat for each non-functional requirement.

---

## 3. Quality Attributes Considered

Record quality attributes that were explicitly evaluated but are not applicable to this change.

Use this section to make relevant analysis visible, not to produce an exhaustive checklist for every feature. Do not list a quality attribute as not applicable merely because its requirements have not yet been established.

- **[Quality attribute]:** [Reason it is not applicable to this change]

---

## 4. Scope Exclusions

Identify exclusions relevant to interpreting these requirements.

The brief remains the authoritative source for the feature's non-goals. Record only exclusions that needed to be clarified or added while writing the requirements.

Do not duplicate the entire brief or use this section as a backlog.

- [Explicit exclusion]

---

## 5. Assumptions and Open Questions

Record the assumptions and unresolved questions that materially affect the interpretation, completeness, or validity of these requirements.

Prefer resolving questions before finalizing requirements when their answers could change required behavior or scope. Reference the brief when the information is already maintained there.

### ASM-01: [Assumption]

- **Basis:** [Reason or available evidence]
- **Impact:** [Requirements or behavior affected]
- **Status:** [Unverified | Confirmed | Rejected]
- **Resolution:** [Evidence or decision, when available]

Repeat for each assumption.

### OQ-01: [Question]

- **Impact:** [Requirements or decisions affected]
- **Proposed default:** [Recommended answer, or TBD]
- **Status:** [Open | Resolved | Deferred]
- **Resolution:** [Confirmed answer or decision, when resolved]

Repeat for each open question.

---

## 6. Traceability and Coverage

Record only meaningful coverage gaps or traceability notes.

Before this document is approved, verify that:

- Every in-scope outcome of the brief is addressed by one or more requirements, or is explicitly identified as unresolved.
- No requirement introduces scope the brief does not include, or contradicts an established obligation.
- Every functional requirement has relevant acceptance criteria.
- Every non-functional requirement has a verification method.
- Important assumptions and unresolved questions are visible.
- Withdrawn requirements keep their IDs and are not silently removed.

Record the result:

- **Coverage gaps:** [None | Identified gaps]
- **Unresolved dependencies:** [None | Relevant questions or decisions]

---

## 7. Maintenance Guidelines

This document MUST remain aligned with the approved brief and with the behavior the feature is intended to have.

Bump `version` on every change made after the first review or approval, and keep `upstream` pointing to the version of the brief these requirements are built from. When the brief's version changes, check these requirements again: confirm them by updating `upstream`, or revise them.

A change to the required behavior, the scope, or the acceptance criteria MUST be approved again by the human. Every artifact that lists an older version of this document in its `upstream` becomes stale and MUST be checked again.

### Source of Truth

- This document is the canonical reference for the feature's required behavior and qualities.
- The feature's brief defines why the feature exists, its desired outcome, and its scope.
- The feature's design defines how the requirements are met; it never changes them.
- `constitution.md` governs engineering principles and mandatory constraints that apply to every feature.

When information changes, update its authoritative source rather than maintaining competing copies across documents.
