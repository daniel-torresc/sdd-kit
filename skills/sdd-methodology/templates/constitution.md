---
artifact: constitution
version: [version]
status: [draft | active | superseded]
owner: [responsible role or team]
---

# Project Constitution

> Defines the enduring engineering principles, mandatory constraints, and practices governing the evolution of this software system. All specifications, designs, implementations, and verification activities MUST respect the applicable rules established here.

---

## 1. Principles

Define the fundamental principles that guide decisions throughout the project lifecycle.

Principles MUST express actionable expectations rather than vague aspirations. Each principle MUST explain its rationale and implications.

### PR-001 — [Principle Name]

**Statement**
[State the fundamental expectation clearly and concisely.]

**Rationale**
[Explain why this principle matters and what problem, risk, or trade-off it addresses.]

**Implications**
[Explain how this principle should influence specifications, architectural decisions, implementation, verification, and maintenance.]

**Normative level**
[MUST | SHOULD | GUIDANCE]

Repeat for each principle.

---

## 2. Non-Negotiable Constraints

Define the mandatory rules and prohibited behaviors that all applicable implementations MUST respect.

Constraints MUST be unambiguous, actionable, and verifiable wherever reasonably possible.

### NC-001 — [Constraint Name]

**Rule**
[State the mandatory requirement using MUST or MUST NOT.]

**Rationale**
[Explain why the constraint is mandatory.]

Repeat for each constraint.

---

## 3. Practices

Define the practices that translate the principles and constraints into repeatable development behavior. How this project wants the work done, on top of the methodology.

Examples: write the tests before the code; every public function documented; pair every migration with a rollback.

### EP-001 — [Practice Name]

**Practice**
[Describe the expected engineering behavior.]

**Normative level**
[MUST | SHOULD | MAY]

**Applicability**
[Define when the practice applies.]

Repeat for each practice.

---

## 4. Quality and Verification

Establish cross-cutting expectations for software quality and the evidence required to demonstrate compliance with this constitution.

- Applicable mandatory constraints MUST have an identifiable verification method.
- Verification MUST be proportionate to the risk and impact of the change.
- Mandatory requirements MUST have appropriate verification evidence before the relevant change is accepted.
- Automated checks SHOULD be used when they provide reliable, repeatable evidence.
- Engineering judgment MAY be required when a principle cannot be assessed mechanically.
- Material verification gaps MUST be resolved or handled through an explicitly authorized exception, where permitted.

[Add only project-wide quality expectations that are not already expressed by the principles or constraints above.]

Detailed quality targets, feature-specific acceptance criteria, and verification procedures MUST be defined in their respective SDD artifacts rather than duplicated here.

---

## 5. Conflict Resolution and Exceptions

### 5.1 Conflict Resolution

When principles, requirements, or constraints appear to conflict:

1. Applicable legal, regulatory, security, and organizational obligations MUST be respected according to their authority.
2. Applicable non-negotiable constraints MUST be satisfied unless a deviation is explicitly permitted by an authorized exception.
3. Requirements and designs MUST be reconciled with the constitution before implementation proceeds.
4. When principles conflict, decisions SHOULD prioritize the applicable constraints, required outcomes, and material risks while avoiding unnecessary complexity.
5. Material unresolved conflicts MUST be escalated to the appropriate decision owner.
6. Significant decisions that establish precedents MUST be recorded in the appropriate decision artifact.

### 5.2 Exceptions

Deviations from mandatory constraints MUST NOT be treated as informal permissions or implicit changes to the constitution.

Where exceptions are permitted, each exception MUST document:

- **Affected rule:** [Constraint identifier]
- **Scope:** [Exact boundary of the exception]
- **Justification:** [Why compliance is not currently feasible]
- **Risk and compensating controls:** [Assessment and mitigations]
- **Approver:** [Authorized role]
- **Expiry or review trigger:** [Date or explicit condition]
- **Remediation:** [Required corrective action, if applicable]

Exceptions MUST be limited to the smallest feasible scope and MUST NOT override applicable higher-authority obligations.

Departures from recommended practices do not automatically require formal exceptions, but SHOULD be justified when they materially affect engineering risk or maintainability.

Existing implementation patterns MUST NOT automatically be treated as desirable standards. Legacy deviations MUST be evaluated against the intended engineering principles and constraints.

Repeated exceptions SHOULD trigger a review of the affected rule, architecture, or underlying technical debt.

---

## 6. Governance and Evolution

### 6.1 Authority

This constitution is the authoritative source of the project's enduring engineering principles and constraints.

Specifications, technical plans, architecture documents, and implementation details MAY refine how these rules are satisfied but MUST NOT silently override them.

### 6.2 Amendments

Changes to this constitution MUST:

- Have an explicit rationale.
- Identify affected principles, constraints, and practices.
- Assess implications for existing specifications and implementations.
- Be reviewed and approved by the authorized owner or stakeholders.
- Be versioned and communicated to affected contributors.

Changes to mandatory obligations MUST be explicitly identified.

### 6.3 Versioning

The project MUST maintain a version history of the constitution.

- **Major:** Changes that materially alter existing obligations or their interpretation.
- **Minor:** Additions or changes that introduce or refine engineering expectations without materially weakening existing ones.
- **Patch:** Editorial corrections or clarifications that do not change the meaning of existing obligations.

[Adapt this scheme if the project uses a different versioning policy.]

### 6.4 Review

The constitution SHOULD be reviewed when significant architectural, security, regulatory, or engineering changes indicate that its principles or constraints may no longer be appropriate.

Repeated exceptions, recurring compliance failures, and evidence that a principle is ineffective SHOULD trigger reconsideration.