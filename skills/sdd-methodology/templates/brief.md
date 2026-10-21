---
artifact: brief
feature: [feature ID]
status: [draft | approved | superseded]
version: [version]
upstream: []
---

# Brief: <feature name>

> Describes the problem or opportunity behind a feature, who it affects, the outcome it must achieve, how success is measured, and the boundaries of the change.
> Once approved, this document and the requirements built from it are the contract every later artifact of the feature is checked against.
> It describes what is needed and why, never how it is built. Keep it to what is needed to understand and bound the change, without duplicating product, architecture, or requirements content maintained elsewhere.

---

## 1. Problem

Describe the problem or opportunity motivating this change.

Explain:

- What is wrong, missing, or could be improved.
- Who is affected, and how.
- What evidence supports the problem statement.

For brownfield projects, describe the relevant current behavior. Distinguish observed facts from reported problems or interpretations.

---

## 2. Users and Context

Identify the users or stakeholders affected by this change and the context in which the problem occurs.

Focus on their goals, needs, and relevant circumstances. Include only information that helps explain the problem or shape the desired outcome.

Use the user groups and domain terms defined in `product.md` where they apply.

---

## 3. Desired Outcome

Describe the observable change expected when this feature is delivered.

Explain what users should be able to accomplish, what should improve, or what problem should be resolved.

Describe the intended outcome, not the implementation approach.

---

## 4. Success Criteria

Describe how to determine whether the desired outcome has been achieved.

Prefer observable, verifiable criteria. Use measurable targets where meaningful and feasible. If success cannot yet be measured precisely, describe the evidence that would demonstrate a satisfactory outcome.

Distinguish established targets from proposed ones. Do not invent baselines, metrics, or targets without supporting evidence.

### SC-01: [Success criterion]

- **Measurement:** [Metric, verification method, or evidence]
- **Baseline:** [Current value, or how it will be obtained, where applicable]
- **Target:** [Target value, or TBD]

Repeat for each success criterion.

---

## 5. Scope

### 5.1 In Scope

List the capabilities, behaviors, or outcomes this change must address to achieve its objective.

Keep the scope at the level of the requested change, not individual implementation tasks. Aim for the smallest scope that delivers the desired outcome, within the roadmap item the feature delivers: the scope may narrow the item, never widen it.

- [In-scope item]

### 5.2 Non-Goals

Identify relevant exclusions to prevent misunderstandings or unintended scope expansion.

Include only exclusions that materially clarify the boundaries of this change. An exclusion worth a later feature names the roadmap item that holds it.

- [Excluded item]

---

## 6. Constraints

Record confirmed conditions that the solution MUST respect.

Examples include:

- Business or regulatory obligations.
- Compatibility and interoperability requirements.
- Operational limitations.
- Deadlines or budget constraints.
- Existing system boundaries, mandatory dependencies, or technologies fixed in `stack.yaml`.

Distinguish mandatory constraints from preferences. Do not restate the rules of `constitution.md`; reference them when they matter to this change.

### CON-01: [Constraint]

- **Source:** [Why it applies, or where it originates]

Repeat for each constraint.

---

## 7. Assumptions

Record material assumptions that are being used to proceed despite incomplete evidence.

Include only assumptions that could affect scope, requirements, or the validity of the proposed change.

### ASM-01: [Assumption]

- **Basis:** [Reason or available evidence]
- **Default:** [What is assumed unless contradicted]
- **Impact if incorrect:** [Consequence, where relevant]
- **Status:** [Unverified | Confirmed | Rejected]

Repeat for each assumption.

---

## 8. Open Questions

Record unresolved questions whose answers could materially affect the change.

Where possible, propose a default answer to support progress. A default is not a confirmed decision.

Do not list questions that can already be answered from available documentation, repository evidence, or established project context.

### OQ-01: [Question]

- **Why it matters:** [Impact on the change]
- **Proposed default:** [Recommended answer, or TBD]
- **Status:** [Open | Resolved | Deferred]
- **Resolution:** [Confirmed answer or decision, when resolved]

Repeat for each open question.

---

## 9. Risks

Record significant risks that could prevent the desired outcome, invalidate assumptions, or materially affect delivery.

Focus on risks relevant to understanding and defining the change, rather than maintaining a comprehensive project risk register.

### RISK-01: [Risk]

- **Likelihood:** [Low | Medium | High | Unknown]
- **Impact:** [Low | Medium | High | Unknown]
- **Mitigation:** [Proposed mitigation, or TBD]

Repeat for each risk.

---

## 10. References

Link to the sources supporting this brief, where available.

Examples include:

- Stakeholder input or business documentation.
- Existing behavior observed in the repository.
- User research, incidents, or operational evidence.
- Related product documentation, specifications, or research notes.
- Relevant policies or external dependencies.

### REF-01: [Source or reference]

- **Purpose:** [What it supports in this brief]

Repeat for each reference.

Identify important limitations in the available evidence. Do not duplicate information maintained in referenced sources.

---

## 11. Maintenance Guidelines

This document MUST remain aligned with the feature's agreed intent.

Bump `version` on every change made after the first review or approval. A change to the problem, the scope, the desired outcome, or the success criteria MUST be approved again by the human. Every artifact that lists an older version of this brief in its `upstream` becomes stale and MUST be checked again.

IDs are never reused. An item that no longer applies keeps its heading, marked `[withdrawn]`.

### Source of Truth

- This document is the canonical reference for why the feature exists and what it must achieve.
- The feature's requirements define the exact, observable behavior that delivers it.
- `roadmap.md` holds the item this feature delivers, named in the feature's state record, and the later items that hold what this brief leaves out.
- `product.md` describes the product as a whole; `constitution.md` governs engineering principles and mandatory constraints; `stack.yaml` records the technologies in use.
- The feature's decisions record holds the questions, answers, and approvals behind this brief.

When information changes, update its authoritative source rather than maintaining competing copies across documents.
