---
name: practice-cartography
description: Codebase investigation for SDD in existing (brownfield) projects — investigating a whole system or a feature's area (structure, behavior, data, integrations, commands that work, conventions in use, tests, hotspots) and recording it as cited research notes for the owners of the canonical documents, impact analysis for proposed changes, adoption of an existing codebase into SDD, and how to change existing code safely (characterization tests, seams, strangler, incremental change). Use when onboarding a codebase, before specifying or designing a change to existing code, or when assessing the blast radius of a change.
---

# Practice: Cartography

Describe **what is**, with citations (`path:line`), never what should be. Opinions go in a separate "Observations" section.

## 1. Whole-system investigation (adopt)

When an existing codebase adopts SDD, investigate it as a whole and write research notes (kind `codebase-investigation`), each aimed at the owner who will turn it into a canonical document:

| Note | Covers | For |
|---|---|---|
| Structure and behavior | Layout, languages and frameworks (versions from lockfiles), deployables, modules and their responsibilities, entry points (routes, CLIs, jobs, consumers), key runtime flows | architect → `architecture.md` |
| Data and integrations | Datastores, models, migrations tooling, data ownership, external services and how they are called (client, auth, timeouts), configuration and secret names | architect → `architecture.md` |
| Technologies and commands | The stack in use and the build, run, test, lint commands that actually work (from CI and manifests) | architect → `stack.yaml` (`decided-by: existing`) |
| Conventions in use | Naming, error handling, logging, dependency wiring, test layout, formatting and linting config — with example locations | architect → `architecture.md` (conventions) |
| Capabilities and users | What the product does today, for whom, as observable from the code and UI | product-lead → `product.md` |
| Tests and risk | Test frameworks and levels, how to run them, coverage signal, flaky or skipped areas, high-churn and untested hotspots | test-engineer (characterization tests), architect (debt) |
| Delivery | CI pipelines, build artifacts, deployment configuration | platform-engineer |

Methods: read manifests and lockfiles first, then entry points, then follow calls; use history (`git log`) for churn; search for routes, models and configuration keys. Verify commands from CI configuration, not by guessing.

## 2. Feature investigation

Before Specify and Design on existing code, write one research note on the affected area:
- **current behavior** of what the request touches, cited;
- **relevant files** with their roles; **callers and dependents** (who breaks if this changes);
- **existing tests** covering it, and gaps;
- **contracts in force** (public APIs, events, schemas) and their consumers, if discoverable;
- **conventions to follow** in that area;
- **risks**: hotspots, fragile code, missing tests, data migration needs.

## 3. Impact analysis

For a proposed change (from a design, a change request, or an incident fix), write a research note listing affected modules, interfaces, data, tests and consumers; classify the change as compatible or breaking; estimate the blast radius; and suggest characterization tests to add before changing untested code.

## 4. Adoption handoffs

After the whole-system investigation (§1), the owners do the work: the architect writes `architecture.md` and the `stack.yaml` entries and commands; product-lead writes `product.md`; test-engineer plans characterization tests; platform-engineer closes CI gaps. You never write their documents.

## 5. Findings age

Every note records the commit SHA it describes. When a note is older than the code it describes in the affected area, re-investigate rather than rely on it — a stale description is worse than none.

## 6. Changing existing code safely

Investigation is for understanding; changing existing code needs its own discipline. Agents use these rules when the work touches code they did not write. The cartographer recommends them in its investigation and impact notes.

1. **Understand → protect → change.** First understand the current behavior (§2). Then protect it with **characterization tests** that pin down what the code does today, even where that behavior is odd. Only then change it.
2. **Find seams.** Look for places where behavior can be substituted without editing the logic: interfaces, injection points, configuration, module boundaries. Where none exists, a small preparatory refactoring that creates one is its own task.
3. **Change incrementally.** Prefer the *strangler* approach: build the new path beside the old one, route traffic gradually, and remove the old path when nothing uses it. Avoid big-bang rewrites.
4. **Keep it releasable.** Every step leaves the system working and deployable. Use feature flags or branch-by-abstraction for long transitions.
5. **Preserve contracts.** External behavior and interfaces stay compatible unless a requirement says otherwise (see the api-compat lens).
6. **Leave a trail.** Record unknowns, oddities and deliberately preserved quirks in the research notes and, as debt, in `architecture.md` (via the architect), so the next change starts from knowledge rather than archaeology.
