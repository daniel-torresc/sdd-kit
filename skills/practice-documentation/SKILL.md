---
name: practice-documentation
description: Documentation and knowledge practice for the SDD librarian — documentation types by audience (README, user guides, API reference from contracts, developer guides; runbooks stay with platform-engineer), docs-as-code rules, keeping docs in sync with shipped behavior, the project knowledge base (lessons learned, decision index, FAQ), promoting researcher stack briefs into project skills, and optional sync of knowledge to an external knowledge base. Use when writing or updating docs, recording lessons, or promoting a brief to a skill.
---

# Practice: Documentation and knowledge

## 1. Know the audience

| Doc | Audience | Lives in | Source of truth |
|---|---|---|---|
| README | New developers and evaluators | `README.md` | conventions, operations commands |
| User guide | End users / API consumers | `docs/guide/` | requirements (behavior), ux.md (copy) |
| API reference | Integrators | `docs/api/` | `contracts/` (generated, then explained) |
| Developer guide | Contributors | `docs/dev/` | conventions, architecture overview, ADRs |
| Runbooks | Operators | `docs/runbooks/` | platform-engineer (not yours) |
| Changelog / release notes | Users | `CHANGELOG.md` | platform-engineer generates; you edit for clarity when asked |

## 2. Docs as code

Markdown in the repo, reviewed like code; examples are tested or copied from tests; every page states what version/behavior it describes; no duplicated facts — link to the source artifact instead. Write in plain language with the glossary's terms; task-oriented ("How to reset a password") over feature lists.

## 3. Keep docs in sync (on ship)

When a feature passes G3, update the docs its behavior touches: README commands/config, user guide pages for changed flows, API reference from the changed contract (including errors and examples), developer guide for new conventions. Diff the feature's requirements and contracts against the docs to find what changed.

## 4. Knowledge base (`.sdd/knowledge/`)

- `lessons.md` — `LES-nn`: what happened, why it matters, what to do differently, links (retro, incident, review). Only lessons that would change future behavior.
- `decisions.md` — an index of ADRs and human gate decisions (one line each, link), so agents find precedent quickly.
- `faq.md` — recurring questions from reviews and escalations, with answers and sources.

Agents read these at the start of related work; keep them short and current.

## 5. Promoting a stack brief to a skill

When a stack brief (`.sdd/briefs/<stack>.md`) has been used successfully in at least one shipped feature: draft a project skill at `.claude/skills/stack-<name>/SKILL.md` (frontmatter `name`, a trigger-rich `description`; body from the brief plus lessons learned in practice). It is a **D2**: the architect reviews it before it is committed, because skills change how every agent works.

## 6. External knowledge sync (optional)

If `.sdd/config.yaml` enables `knowledge.external_sync`, prepare a sync bundle (decisions, lessons, feature summaries) in `.sdd/knowledge/outbox/`; the hub pushes it to the configured knowledge base after the human approves (external write).
