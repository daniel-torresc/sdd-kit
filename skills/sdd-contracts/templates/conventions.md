---
artifact: conventions
owner: architect
status: draft
version: 1
upstream: []
---

# Engineering conventions

## Stack profile
<!-- The technologies in use (descriptive context for agents and the harness). Every entry links the ADR that decided it. -->
```yaml
stack:
  backend: { language: <language>, framework: <framework>, adr: ADR-NNNN }
  persistence: { db: <datastore>, data-access: <library>, migrations: <tool>, adr: ADR-NNNN }
  frontend: { rendering: <tbd>, framework: <tbd>, adr: <tbd> }
  hosting: { platform: <tbd>, adr: <tbd> }
  frontend: []
```

## Repository layout

## Coding conventions
<!-- Naming, error handling, logging, configuration, dependency injection, where tests live. -->

## API conventions
<!-- Error format, pagination, idempotency, versioning, time and money formats. -->

## Tooling and commands
| Purpose | Command |
|---|---|
| Install | |
| Lint / format | |
| Type check | |
| Test | |
| Run locally | |

## Definition of Done additions
