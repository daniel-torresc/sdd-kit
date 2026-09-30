---
artifact: architecture-overview
owner: architect
status: draft
version: 1
upstream: []
---

# Architecture overview: <product>

## System context
<!-- Who and what the system talks to. -->
```mermaid
flowchart LR
  user([Customer]) --> app[<product>]
  app --> email[(Email provider)]
```

## Containers
<!-- Deployables and datastores, with the technology of each (link ADRs). -->

## Module map
| Module | Responsibility | Owns data | Public interface | Depends on |
|---|---|---|---|---|

## Cross-cutting
<!-- AuthN/AuthZ, configuration, logging/tracing, error format, time, IDs, i18n. -->

## Key decisions
<!-- ADR list with one line each. -->
