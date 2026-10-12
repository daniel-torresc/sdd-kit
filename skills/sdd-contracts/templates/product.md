---
artifact: product
version: [version]
status: [draft | active | superseded]
owner: human | librarian
---

# <Product>

> Describes the product's purpose, business context, users, capabilities, domain concepts, objectives, and boundaries.
> This document is the canonical reference for understanding what the product is, why it exists, whom it serves, and what it aims to achieve. It provides persistent product context for requirements discovery, specification writing, architectural decisions, and implementation.
> This is a living document. Keep it aligned with the product as it evolves, without duplicating detailed requirements, technical architecture, or implementation plans maintained elsewhere.

---

## 1. Product Overview

Provide a concise, high-level explanation of the product.

### 1.1 Purpose

Describe what the product is, the problem it solves, and why it exists.

### 1.2 Value Proposition

Explain the primary value the product provides and how it improves the situation of its intended users or stakeholders.

### 1.3 Product Vision

Describe the intended long-term direction of the product, where relevant. Keep this focused on the product's purpose and evolution rather than a detailed roadmap.

---

## 2. Business Context

Describe the business domain and circumstances that influence the product's purpose, behavior, and evolution.

### 2.1 Domain and Operating Context

Explain the relevant business domain, operational environment, and processes in which the product operates.

### 2.2 Problem and Opportunity

Describe the principal problems, unmet needs, or opportunities that motivated the product.

### 2.3 Existing Solutions and Processes

Describe relevant existing systems, tools, or manual processes that the product replaces, complements, or depends on.

For greenfield projects, explain the current situation the product is intended to improve. Omit this subsection if it adds no value.

---

## 3. Users and Stakeholders

Identify the user groups and stakeholders whose needs influence the product.

### 3.1 User Groups

For each significant user group, document:

- **Name:** [User group]
- **Role:** [Their relationship to the product]
- **Goals and needs:** [What they need to accomplish]
- **Relevant context:** [Important permissions, responsibilities, limitations, or usage circumstances]

Include only distinctions that materially affect product behavior or design. Do not create separate user groups for inconsequential differences.

### 3.2 Other Stakeholders

Identify relevant business owners, operators, administrators, external organizations, or other stakeholders who influence the product or are affected by its outcomes.

Explain their interests or responsibilities where necessary.

---

## 4. Product Capabilities

Describe the product's major capabilities and the value they provide.

For each significant capability, document:

- **Name:** [Capability name]
- **Purpose:** [What it enables and why it matters]
- **Primary users:** [Relevant user groups, if applicable]
- **Scope:** [The principal responsibilities or outcomes covered]
- **Status:** [Current | Planned | Retired, where applicable]

Organize capabilities around meaningful product responsibilities or user outcomes, not individual tickets, implementation tasks, or low-level technical components.

For greenfield projects, describe the intended initial capabilities. For brownfield projects, distinguish existing capabilities from planned or retired ones. Do not present aspirations as implemented functionality.

---

## 5. Domain Concepts and Business Rules

Document the domain knowledge that developers need to understand consistently across multiple capabilities.

### 5.1 Key Domain Concepts

For each essential concept, document:

- **Term:** [Canonical name]
- **Definition:** [Meaning in the product's domain]
- **Relationships:** [Important relationships to other concepts] (where applicable)

Include only concepts whose meanings materially affect product behavior, requirements, or business decisions.

Use consistent terminology throughout the project. Link to a dedicated domain model or glossary if more detailed definitions are maintained elsewhere.

### 5.2 Business Rules

Document enduring business rules that govern product behavior across capabilities.

For each significant rule, document:

- **Identifier:** [Stable identifier, if useful]
- **Rule:** [Clear statement of the business rule]
- **Rationale:** [Why the rule exists, where known]
- **Applicability:** [Relevant conditions, users, or domain concepts] (where necessary)
- **Source:** [Authoritative policy, stakeholder, or reference, where applicable]

Include rules that must remain consistent across multiple workflows or specifications.

Distinguish confirmed rules from proposed or unverified interpretations. Detailed workflow behavior, exceptions, acceptance criteria, and verification scenarios belong in the relevant specifications.

If the rules are extensive, maintain a dedicated business-rules artifact and reference it here.

---

## 6. Objectives and Success Criteria

Describe the outcomes the product is intended to achieve and how their achievement can be evaluated.

For each significant objective, document:

- **Objective:** [Desired product or business outcome]
- **Rationale:** [Why the outcome matters]
- **Success criteria:** [Observable evidence of success, where defined]
- **Measurement:** [Relevant metric, evaluation method, or evidence, where applicable]

Distinguish product outcomes from delivery milestones and implementation activities.

Use measurable criteria where meaningful and feasible. Do not invent targets or metrics that have not been established.

If objectives or targets are provisional, identify them as such. Detailed experimentation and measurement plans belong in their appropriate artifacts.

---

## 7. Scope and Boundaries

Define the responsibilities and limits of the product.

### 7.1 In Scope

Describe the principal responsibilities, capabilities, and outcomes that the product is intended to cover.

### 7.2 Out of Scope

Identify important responsibilities, capabilities, or problems that the product is explicitly not intended to address.

Focus on exclusions that help prevent misunderstandings or unintended scope expansion.

### 7.3 External Dependencies and Responsibility Boundaries

Describe relevant external actors, services, systems, or processes on which the product depends, including important boundaries between the product and those dependencies.

Keep technology-specific integration details in `stack.yaml`, `architecture.md`, or their dedicated artifacts.

---

## 8. Constraints, Assumptions, and Dependencies

Record business and operational conditions that materially influence the product's definition or evolution.

### 8.1 Constraints

Document confirmed constraints such as business policies, contractual obligations, regulatory requirements, operational limitations, or delivery conditions that affect the product.

Distinguish product-level constraints from engineering rules maintained in `constitution.md` and technical constraints maintained in`stack.yaml` or `architecture.md`.

Identify the source of consequential obligations where possible.

### 8.2 Assumptions and Open Questions

Document assumptions or unresolved questions that could materially affect product scope, behavior, or objectives.

For each significant item, identify:

- **Description:** [The assumption or question]
- **Status:** [Unverified | Under investigation | Resolved]
- **Impact:** [What may be affected if it is incorrect or unresolved]
- **Next step:** [How it will be validated or resolved, where known]

Do not use this section as a general list of every minor uncertainty. Move resolved items into the appropriate authoritative section and remove obsolete assumptions.

### 8.3 External Dependencies

Document significant business, organizational, or operational dependencies that affect product outcomes.

Avoid duplicating the integration inventory or infrastructure dependencies maintained in technical artifacts.

---

## 9. Product State and Direction

Describe the product's current state and intended evolution.

### 9.1 Current State

Summarize the product's current maturity and the status of its principal capabilities.

For greenfield projects, describe the initial state, such as concept, discovery, or initial development.

For brownfield projects, describe the product as it actually exists. Distinguish verified capabilities from undocumented or unverified behavior.

### 9.2 Known Gaps and Limitations

Identify significant gaps between the current product and its intended capabilities or outcomes.

Focus on limitations that influence requirements, scope, or development decisions. Keep detailed defect lists and remediation tasks in their appropriate artifacts.

### 9.3 Intended Evolution

Describe important future directions, capability expansions, or changes in product responsibilities that provide context for current decisions.

Distinguish established commitments from proposals and longer-term aspirations. Do not turn this section into a detailed roadmap, prioritized backlog, or implementation plan.

---

## 10. References

Link to authoritative sources that provide additional product context, such as business documentation, domain glossaries, regulatory policies, research, detailed business rules, or related SDD artifacts.

For each reference, identify its purpose and, where useful, its authority or relationship to this document.

Avoid duplicating content that is already maintained in those sources.

---

## 11. Maintenance Guidelines

This document MUST remain aligned with the product's intended purpose, scope, and behavior.

Update it when changes materially affect:

- The product's purpose, value proposition, or business context.
- The needs or responsibilities of its primary users.
- Its major capabilities or product boundaries.
- Shared domain concepts or enduring business rules.
- Product objectives or success criteria.
- Important business constraints, assumptions, or dependencies.
- The distinction between current capabilities and intended evolution.

When a change affects a single feature without changing the broader product context, document the change in the relevant specification rather than expanding this file unnecessarily.

When product discovery or implementation reveals that an established assumption is incorrect, update the affected sections and review any dependent specifications or decisions.

### Source of Truth

- This document is the canonical reference for persistent, product-level context.
- `constitution.md` governs enduring engineering principles, mandatory constraints, practices, and governance.
- `stack.yaml` records the project's technology stack and technical choices according to its defined schema.
- `architecture.md` describes the system's architecture and how its components work together.
- Individual specifications define detailed requirements, expected behavior, and acceptance criteria for particular capabilities or changes.
- Other specialized artifacts MAY provide more detailed information for their respective areas of responsibility.

When information changes, update its authoritative source rather than maintaining competing copies across documents.

If a change creates a contradiction between this document and another artifact, identify the conflict and reconcile the affected documents.

Do not present planned capabilities, unverified assumptions, or proposed business rules as established facts.