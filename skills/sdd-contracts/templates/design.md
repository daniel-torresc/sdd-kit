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
<!-- Machine-readable contracts in contracts/ (required for external/public interfaces): OpenAPI 3.1, AsyncAPI, JSON Schema. -->

## Runtime dependencies
<!-- New runtime packages/services this design needs: name, version range, purpose, alternatives considered.
     security-engineer vets each one (dependency-review) before Build. -->
| Dependency | Version | Purpose | Alternatives |
|---|---|---|---|

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

## Security considerations
<!-- Summary; details in threat-model.md when the security lens is active. -->

## Decisions
<!-- List ADRs created or relied on. One-way doors: G2 reference or why none. -->

## Spikes
<!-- SPK-nn: question → conclusion. -->

## Fitness functions and architecture updates
<!-- New FF-nn to add to .sdd/architecture/fitness.md; changes to overview.md / conventions.md on ship. -->

## Alternatives considered

## Assumptions

## Open questions
