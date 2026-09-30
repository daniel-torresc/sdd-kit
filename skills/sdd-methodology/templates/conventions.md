---
artifact: conventions
owner: architect
status: draft
version: 1
upstream: []
---

# Engineering conventions

## Stack profile
<!-- Machine-readable: the hub routes skills from this. Every entry links the ADR that decided it. -->
```yaml
stack:
  backend: { language: python, framework: fastapi, adr: ADR-0001 }
  persistence: { db: postgresql, orm: sqlalchemy, migrations: alembic, adr: ADR-0002 }
  frontend: { rendering: <tbd>, framework: <tbd>, adr: <tbd> }
  hosting: { platform: <tbd>, adr: <tbd> }
skills:
  backend: [stack-python]
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
