---
artifact: architecture
owner: architect
status: draft
version: 1
---

# Architecture: <product>

> The canonical explanation of how the system works. Only what genuinely helps someone understand and work on it.
> Technologies are listed in `.sdd/stack.yaml`; decisions and their reasons in `docs/adr/`.

## 1. Purpose and context
<!-- What the system does, who and what it interacts with. One context diagram. -->

## 2. Building blocks
<!-- Modules / services and their responsibilities, what data each owns, and how they depend on each other. -->

| Module | Responsibility | Owns data | Public interface | Depends on |
|---|---|---|---|---|

## 3. Key runtime flows
<!-- The few flows that explain how the system behaves (sequence diagrams where useful). -->

## 4. Data
<!-- Main entities, where they live, ownership, retention, classification (public / internal / personal / sensitive). -->

## 5. Cross-cutting concepts
<!-- Identity and authorization, error handling, observability, configuration and secrets, internationalization — how the system does each, once. -->

## 6. Deployment and operations
<!-- Environments, how it runs, how it is deployed and rolled back.
     Service level objectives (journey → indicator → target) and expected capacity, when defined. -->

## 7. Conventions
<!-- What someone changing the code must follow: structure, naming, error and logging conventions,
     architecture rules enforced in CI (one line each), how to run things (see stack.yaml commands). -->

## 8. Key decisions
<!-- ADR index: one line each with a link. -->

## 9. Known debt and risks
<!-- DEBT-nn: what, why it was accepted, what makes fixing it urgent. Open architectural risks. -->
