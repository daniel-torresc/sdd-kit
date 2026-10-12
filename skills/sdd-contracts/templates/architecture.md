---
artifact: architecture
version: [version]
status: [draft | active | superseded]
owner: human | librarian
---

# Architecture: <product>

> Describes the system's architecture, including its boundaries, components, interactions, data flows, and cross-cutting concerns.
> This document is the canonical reference for understanding how the system is structured, how its parts work together, and the architectural decisions that shape its implementation.
> This is a living document. Keep it aligned with the architecture that actually exists, distinguishing implemented behavior from intended designs and proposed changes.
> Document architectural knowledge at the level necessary to understand the system and make informed engineering decisions. 
> Avoid duplicating technology inventories, product documentation, detailed specifications, or implementation-level documentation maintained elsewhere.

---

## 1. Architectural Overview

Provide a concise explanation of the system's overall architecture.

### 1.1 Architectural Summary

Explain the overall structure of the system, its principal architectural characteristics, and how its major parts work together.

Describe the architecture in terms that are meaningful for the system, rather than forcing it into a predefined architectural style.

Where useful, identify characteristics such as modularity, deployment boundaries, execution model, or distribution of responsibilities.

### 1.2 Architectural Drivers

Describe the most important requirements, constraints, and quality attributes that shape the architecture.

Examples may include security, reliability, performance, scalability, maintainability, interoperability, or deployment constraints.

Explain why these factors materially influence architectural choices.

Refer to `product.md`, `constitution.md`, or relevant specifications for the authoritative source of product needs and engineering obligations. Do not reproduce their contents.

### 1.3 Architectural Style and Patterns

Describe the architectural styles and patterns that characterize the system, where applicable.

Explain how these patterns are applied and what responsibilities they establish.

Examples might include layered architecture, modular monolith, event-driven architecture, ports and adapters, or distributed services.

Do not select a pattern merely to fill this section. Document the actual architectural approach and its relevant implications.

---

## 2. System Context and Boundaries

Explain where the system begins and ends, what surrounds it, and how it interacts with its environment.

### 2.1 System Boundary

Describe the responsibilities owned by the system and the responsibilities delegated to external actors, systems, or services.

Clarify important ownership boundaries and identify areas that must not be treated as internal responsibilities of the system.

For existing systems, describe the actual boundary. Distinguish planned boundary changes from the current implementation.

### 2.2 External Actors and Systems

Identify external actors, systems, services, or other dependencies that interact with the system.

For each significant external entity, document:

- **Name:** [Actor or system]
- **Purpose:** [Its role in relation to the system]
- **Interaction:** [How it interacts with the system]
- **Responsibility boundary:** [What the external entity owns versus what the system owns]

Keep the description focused on architecturally significant interactions. Maintain exhaustive integration inventories elsewhere if necessary.

### 2.3 System Context Diagram

Include a context diagram where it materially improves understanding.

The diagram should show the system boundary, principal external actors or systems, and the relationships between them.

Use a format that can be maintained alongside the source code or documentation, where practical.

If a diagram is not useful for the system, omit it.

---

## 3. Architectural Components

Describe the principal components that make up the system and the responsibilities assigned to each.

### 3.1 Component Inventory

For each architecturally significant component, document:

- **Name:** [Canonical component name]
- **Purpose:** [Why the component exists]
- **Responsibilities:** [What it owns and is accountable for]
- **Interfaces:** [How other components interact with it]
- **Dependencies:** [Important components or external systems on which it depends]
- **State ownership:** [Important state or data it owns, where applicable]
- **Status:** [Implemented | Partially implemented | Planned | Deprecated, where applicable]

Document components according to meaningful architectural responsibilities, not every class, function, module, or file.

Include only details that help developers understand system structure, responsibility boundaries, or the consequences of changing a component.

### 3.2 Component Relationships

Explain how the principal components relate to one another.

Describe important dependency directions, ownership boundaries, and restrictions on component interactions.

Identify architectural rules that prevent unwanted coupling, circular dependencies, or responsibility duplication.

If the system has a meaningful distinction between internal components and independently deployed services, make that distinction explicit.

### 3.3 Component Diagram

Include a diagram when it helps explain the system's structure.

Show the principal components, their responsibilities where useful, and the most important dependencies or interactions.

Distinguish logical components from deployment units when the difference matters.

Omit the diagram if a concise textual explanation is sufficient.

---

## 4. Interactions and Execution Flows

Explain how important interactions move through the system.

### 4.1 Interaction Model

Describe the principal ways components communicate.

Where applicable, explain the role of synchronous requests, asynchronous messages, events, scheduled execution, callbacks, or other interaction mechanisms.

Document architectural conventions that materially affect component interactions, such as ownership of orchestration, communication boundaries, or handling of asynchronous work.

Refer to `stack.yaml` for the technology inventory and to detailed specifications for feature-specific behavior.

### 4.2 Principal Execution Flows

Describe the execution flows that are essential to understanding the system's architecture.

For each significant flow, document:

- **Name:** [Flow name]
- **Trigger:** [What initiates the flow]
- **Participants:** [Principal components and external entities]
- **Sequence:** [The important steps and interactions]
- **Outcome:** [The resulting state, response, or side effect]
- **Failure behavior:** [Important failure paths and recovery behavior, where applicable]

Focus on flows that cross component boundaries or reveal important architectural behavior.

Examples include request processing, background execution, event handling, data ingestion, or interactions with external systems.

Do not document every possible user journey or duplicate the detailed functional flows maintained in specifications.

### 4.3 Execution Flow Diagrams

Include sequence diagrams, activity diagrams, or other suitable representations when they make important interactions easier to understand.

Use diagrams selectively and keep them aligned with the actual architecture.

If diagrams are maintained as separate files, link to their authoritative locations.

---

## 5. Data Architecture

Describe the architectural organization, ownership, and movement of data through the system.

### 5.1 Data Organization and Ownership

Explain how the system organizes and manages its important categories of data.

Identify significant data ownership boundaries and clarify which components or external systems are authoritative for particular information.

Where relevant, describe distinctions between operational data, reference data, derived data, cached data, and transient state.

Refer to `product.md` for business-domain definitions and to dedicated domain models or data documentation for detailed schemas.

### 5.2 Persistence and Data Access

Explain the architectural approach to persistence and data access.

Document important patterns, such as repositories, data access boundaries, transaction ownership, or separation between application logic and persistence concerns, where applicable.

Describe constraints on how components may access or modify shared data.

Do not duplicate the complete list of databases, libraries, or infrastructure technologies maintained in `stack.yaml`.

### 5.3 Data Flows and Transformations

Describe important architectural data flows, including how data enters the system, is validated or transformed, and reaches its destination.

Identify significant transformations, ownership transfers, consistency requirements, or dependencies between processing stages.

Link to detailed specifications or dedicated data documentation for feature-specific transformations and exhaustive schemas.

### 5.4 Consistency and Lifecycle

Document architectural decisions concerning data consistency, lifecycle, retention, and deletion where they materially affect system behavior.

Examples include transaction boundaries, eventual consistency, idempotency, data versioning, retention policies, or lifecycle management.

Distinguish established behavior from intended or proposed behavior, and reference the authoritative source of consequential business, legal, or regulatory obligations.

---

## 6. Cross-Cutting Concerns

Describe architectural mechanisms and conventions that affect multiple components or system-wide behavior.

Include only concerns relevant to the system.

### 6.1 Security and Authorization

Explain the architectural approach to security and access control.

Where applicable, document:

- Trust boundaries and security-sensitive components.
- Authentication and authorization responsibilities.
- Identity propagation between components.
- Enforcement of permissions at relevant boundaries.
- Protection of sensitive data.
- Treatment of untrusted inputs and external dependencies.
- Important security-related restrictions on component interactions.

Describe where security decisions are enforced and which components are responsible for enforcing them.

Refer to `constitution.md` for mandatory engineering constraints and to dedicated security documentation for detailed policies or control implementations.

### 6.2 Error Handling and Failure Management

Explain the system-wide approach to handling errors and failures.

Where relevant, document:

- Responsibility for detecting and handling failures.
- Error propagation across component boundaries.
- Retry, timeout, cancellation, and recovery conventions.
- Treatment of partial failures and unavailable dependencies.
- Idempotency and duplicate execution handling.
- Fallback behavior and conditions under which processing must stop.

Distinguish architectural conventions from feature-specific error behavior maintained in specifications.]

### 6.3 Observability and Diagnostics

Explain how the architecture supports understanding and diagnosing system behavior.

Where applicable, describe the roles of logs, metrics, traces, audit records, correlation identifiers, and health signals.

Identify important boundaries where observability information must be preserved across components or external interactions.

Describe architectural responsibilities rather than duplicating tool configurations or detailed operational procedures.

### 6.4 Reliability and Resilience

Describe the architectural mechanisms that support reliable operation, where relevant.

Examples include isolation of failures, bounded resource usage, graceful degradation, recovery, redundancy, or protection against overload.

Explain the failure modes these mechanisms address and any important limitations or trade-offs.

### 6.5 Configuration and Secrets

Explain how runtime configuration and sensitive configuration values are handled architecturally.

Where relevant, distinguish application configuration, environment- specific configuration, credentials, and secrets.

Document important boundaries governing configuration ownership, validation, propagation, and access.

Do not include actual credentials, secret values, or other sensitive operational data.

### 6.6 Other Cross-Cutting Concerns

Document additional concerns only when they materially affect multiple parts of the architecture.

Examples may include caching, concurrency, internationalization, accessibility, extensibility, or resource lifecycle management.

Explain the architectural approach and relevant constraints. Avoid creating empty subsections for concerns that do not apply.

---

## 7. Deployment and Runtime Architecture

Describe how the architecture maps to execution and deployment boundaries.

### 7.1 Runtime Model

Explain how the system executes at runtime.

Where applicable, distinguish request handling, background work, scheduled processes, asynchronous processing, and independently running components.

Describe important runtime relationships and resource ownership.

Do not duplicate the complete technology inventory or environment-specific configuration.

### 7.2 Deployment Units and Boundaries

Identify the principal deployment units and explain how they relate to the logical components described earlier.

Where relevant, document which components execute together, which are independently deployed, and which communicate across process or network boundaries.

For greenfield projects, distinguish the intended deployment model from what has actually been implemented.

### 7.3 Environments and Configuration Differences

Describe environment differences that materially affect the architecture, such as development, testing, staging, and production.

Document architectural implications of those differences, including relevant integration boundaries, dependencies, or runtime constraints.

Keep detailed environment variables, infrastructure definitions, deployment commands, and operational procedures in their authoritative artifacts.

---

## 8. Architectural Decisions and Trade-offs

Document the reasoning behind important architectural choices.

### 8.1 Key Decisions

For each significant architectural decision, document:

- **Decision:** [What was decided]
- **Context:** [The problem, constraint, or requirement]
- **Rationale:** [Why this approach was selected]
- **Alternatives:** [Important alternatives considered, where known]
- **Consequences:** [Benefits, limitations, and trade-offs]
- **Status:** [Proposed | Accepted | Superseded | Rejected]
- **Reference:** [Link to a dedicated decision record, if available]

Include decisions whose rationale is important for understanding, maintaining, or evolving the architecture.

Do not record every implementation choice.

If the project maintains Architecture Decision Records (ADRs), use this section as a concise index or summary rather than duplicating their full contents.]

### 8.2 Architectural Constraints

Document constraints that materially restrict architectural choices or system evolution.

Examples include required interoperability, unavoidable external dependencies, deployment limitations, or established compatibility requirements.

Identify the source of consequential constraints and distinguish mandatory obligations from preferences or recommendations.

Refer to `constitution.md` for engineering-wide rules and`stack.yaml` for the authoritative record of technology choices.

### 8.3 Known Trade-offs and Limitations

Describe important architectural compromises, limitations, or unresolved structural issues that influence engineering decisions.

Explain their practical consequences and why they remain acceptable, if known.

Distinguish intentional trade-offs from accidental complexity or technical debt.

Do not turn this section into a general defect list or backlog. Link to the appropriate tracking artifact for remediation work.

---

## 9. Current State and Architectural Evolution

Describe the architecture as it exists today and how it is expected to evolve.

### 9.1 Current Architecture

Summarize the architecture supported by the available evidence.

For existing systems, base this description on the repository, configuration, deployment definitions, tests, documentation, and other relevant evidence.

Distinguish verified behavior from assumptions or incomplete understanding.

For greenfield projects, describe the architecture's current implementation status, which may be limited to an approved design or initial development.

### 9.2 Gaps and Architectural Debt

Identify significant discrepancies between the current architecture and its intended design, established constraints, or engineering requirements.

Where useful, document:

- **Gap:** [Description of the discrepancy]
- **Impact:** [Architectural or engineering consequences]
- **Status:** [Known | Under investigation | Being addressed]
- **Reference:** [Related specification, issue, decision record, or other authoritative source]

Focus on issues that materially influence future changes or architectural decisions.

Avoid duplicating detailed defect reports or technical-debt backlogs.

### 9.3 Intended Architecture and Evolution

Describe important architectural changes that are planned, approved, or under consideration.

Explain the intended direction and the architectural reasons for the change.

Distinguish clearly between:

- The architecture that exists today.
- Approved changes that have not yet been implemented.
- Proposals and longer-term possibilities.

Do not present proposed designs as established architecture.

Avoid turning this section into a detailed implementation plan or delivery roadmap.

### 9.4 Architectural Invariants

Identify architectural properties that must remain true as the system evolves, where applicable.

Examples include dependency direction, ownership boundaries, isolation requirements, or restrictions on communication between components.

Distinguish these architectural invariants from engineering-wide rules maintained in `constitution.md` and from requirements specific to individual features.

For each significant invariant, explain its purpose and how compliance can be assessed, where known.

---

## 10. Codebase Organization and Architectural Mapping

Help developers navigate the implementation and connect the architectural description to the actual codebase.

### 10.1 Repository Structure

Describe the principal directories, modules, packages, or repositories and their architectural responsibilities.

Focus on the organization needed to understand where a change belongs and which parts of the system it may affect.

Avoid reproducing the complete file tree or documenting every source file.

For monorepos or multi-repository systems, clarify the relevant repository boundaries.

### 10.2 Architecture-to-Code Mapping

Map the principal architectural components to their implementation locations.

For each significant component, identify the relevant directories, modules, entry points, or configuration files, where useful.

Distinguish architectural responsibilities from incidental implementation details that may change frequently.

For brownfield projects, identify important discrepancies between the documented architecture and the implementation.

### 10.3 Important Entry Points and Execution Boundaries

Identify the entry points through which significant execution flows begin, where applicable.

Examples include application entry points, API boundaries, message consumers, scheduled jobs, command-line interfaces, or event handlers.

Explain their architectural roles and where processing is delegated next.

Do not duplicate API documentation or detailed function-level documentation.

---

## 11. References

Link to authoritative sources that provide additional architectural detail.

Examples include:

- Architecture Decision Records.
- System context, component, or sequence diagrams.
- Detailed data models and schemas.
- API and integration contracts.
- Security and operational architecture documentation.
- Infrastructure and deployment definitions.
- Relevant specifications.
- External architecture constraints or standards.

For each reference, identify its purpose and, where useful, its authority or relationship to this document.

Prefer links to maintained sources over duplicated content.

---

## 12. Maintenance Guidelines

This document MUST remain aligned with the architecture that exists and the architectural direction that has been established.

Update it when changes materially affect:

- System boundaries or external responsibilities.
- Major components or their ownership boundaries.
- Dependencies or communication patterns between components.
- Important execution flows.
- Data ownership, persistence, or consistency guarantees.
- Cross-cutting architectural mechanisms.
- Runtime or deployment boundaries.
- Significant architectural decisions or trade-offs.
- Architectural invariants.
- The relationship between the architecture and its implementation.

A change does not require an update to this document merely because it modifies code.

Update `architecture.md` when the change alters architectural understanding, introduces a meaningful architectural decision, or invalidates information that developers rely on when making other changes.

### Source of Truth

- This document is the canonical reference for persistent architectural knowledge.
- `constitution.md` governs engineering principles, mandatory constraints, practices, and governance.
- `stack.yaml` records technology choices according to its defined schema.
- `product.md` provides project-specific context and setup, describes the product's purpose, users, capabilities, domain concepts, business rules, and objectives.
- Individual specifications define detailed requirements, expected behavior, and acceptance criteria for particular capabilities or changes.
- Architecture Decision Records, diagrams, contracts, and other specialized artifacts MAY contain more detailed information within their respective areas of responsibility.

When information changes, update its authoritative source rather than maintaining competing copies across documents.

When a change creates a contradiction between this document and another artifact, identify the conflict and reconcile the affected documents.

Do not describe planned architecture as implemented, infer unverified behavior as fact, or silently treat undocumented assumptions as established decisions.