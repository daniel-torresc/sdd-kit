---
name: practice-cartography
description: Codebase mapping for SDD in existing (brownfield) projects — project maps (structure, modules, entry points, data stores, integrations, build/run/test commands, conventions actually in use, test landscape, hotspots from git churn), feature context packs (relevant files, current behavior with file:line citations, callers, tests, conventions to follow), impact analysis for proposed changes, and adoption of an existing codebase into SDD. Use when onboarding a codebase, before specifying or designing a change to existing code, or when assessing the blast radius of a change.
---

# Practice: Cartography

Describe **what is**, with citations (`path:line`), never what should be. Opinions go in a separate "Observations" section.

## 1. Project map (`.sdd/map/`)

| File | Contents |
|---|---|
| `structure.md` | Top-level layout, languages and frameworks (with versions from lockfiles), deployables, modules/packages with one-line responsibilities, entry points (HTTP routes, CLIs, jobs, consumers) |
| `data.md` | Datastores, schemas/models, migrations tooling, data ownership by module, external data flows |
| `integrations.md` | External services and APIs called, how (client, auth, timeouts), configuration and secrets references (names only) |
| `conventions.md` | Conventions **observed**: naming, error handling, logging, DI, test layout, formatting/linting config — with example locations |
| `operations.md` | Build, run, test, lint commands that actually work; CI pipelines; deployment config found |
| `tests.md` | Test frameworks, levels present, how to run, rough coverage signal, flaky or skipped areas |
| `hotspots.md` | Files with highest churn (git log) × size/complexity; areas with no tests; TODO/FIXME clusters |

Methods: read manifests/lockfiles first, then entry points, then follow calls; `git log --since=… --name-only` for churn; grep for routes, models, config keys. Verify commands by reading CI config, not by guessing.

## 2. Feature context pack (`specs/<f>/context.md`)

Before Specify/Design on existing code:
- **Current behavior** of the area the request touches, cited.
- **Relevant files** with roles; **callers and dependents** (who breaks if this changes).
- **Existing tests** covering it, and gaps.
- **Contracts in force** (public APIs, events, schemas) and their consumers if discoverable.
- **Conventions to follow** in that area (from the map).
- **Risks**: fragile code, hotspots, missing tests, data migration needs.

## 3. Impact analysis

For a proposed change (from a design, a CR, or an incident fix): list affected modules, interfaces, data, tests and consumers; classify as compatible / breaking; estimate blast radius; suggest characterization tests to add before changing untested code.

## 4. Adoption (brownfield onboarding)

When SDD is introduced to an existing project: produce the project map, then **propose** (as findings to the owners) an initial `.sdd/architecture/overview.md` and `conventions.md` (architect), a baseline of current behavior for critical journeys (product-lead), characterization-test targets (test-engineer), and CI/tooling gaps (platform-engineer). You don't write their artifacts.

## 5. Keeping maps fresh

Maps carry the commit SHA they describe. When a feature ships, update affected sections (or the hub dispatches a refresh); stale maps are worse than none.
