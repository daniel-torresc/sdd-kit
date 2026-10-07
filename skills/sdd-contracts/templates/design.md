---
artifact: design
feature: F000
owner: architect
status: draft
version: 1
upstream: [requirements.md@1]
---

# Design: <feature name>

## Context
<!-- Current system (brownfield) or baseline (greenfield). Relevant ADRs. -->

## Overview
<!-- One diagram (mermaid) + one paragraph. -->

## Components

### C-01: <component>
refs: REQ-01
responsibility: <one sentence>
<!-- Owns which data; depends on what; failure behavior. -->

## Interfaces

### IF-01: <interface / endpoint / event>
refs: REQ-01, NFR-01
<!-- Signature or schema, errors, idempotency, auth, versioning. -->

## Contracts
<!-- One file per external or public interface in contracts/: operations, inputs, outputs, errors, guarantees and boundaries,
     in clear markdown. Use a machine-readable format (e.g. OpenAPI, AsyncAPI, JSON Schema) only when something consumes it:
     generated clients, contract-testing tools, external consumers. -->

## Runtime dependencies
<!-- New runtime packages/services this design needs: name, version range, purpose, alternatives considered.
     security-engineer vets each one (dependency-review) before Build. -->
| Dependency | Version | Purpose | Alternatives |
|---|---|---|---|

## Infrastructure and spend
<!-- New environments, resources or paid services this design needs, with an order-of-magnitude monthly cost.
     The hub dispatches platform-engineer env-plan for these (human decision on resources and spend). -->

## Data model
<!-- Entities, invariants, ownership, retention, migrations. -->

## Quality-attribute scenarios and NFR budgets
<!-- Per NFR: source → stimulus → artifact → environment → response → measure. -->
| NFR | Scenario | Budget allocation | How it is verified |
|---|---|---|---|

## Failure modes
| Failure | Detection | Behavior | Recovery |
|---|---|---|---|

## Observability
<!-- Logs, metrics, traces, alerts per interface. -->

## Security
<!-- Threats per entry point and the mitigation for each (from security-engineer's design review when the security lens is active),
     authorization model, data classification and handling. -->

## Data and privacy
<!-- Personal data handled, purpose, retention and deletion, processors (from the privacy lens when active). -->

## Cost
<!-- Cost drivers and monthly estimate when new resources or paid services are involved (from the FinOps lens when active). -->

## Decisions
<!-- ADRs created or relied on; one-way doors (G2 entry in decisions.md) or why none; research notes (incl. spikes) relied on. -->

## Architecture updates
<!-- What architecture.md must reflect once this ships (new modules, flows, conventions, debt), and architecture rules to enforce in CI. -->

## Alternatives considered

## Assumptions

## Open questions
