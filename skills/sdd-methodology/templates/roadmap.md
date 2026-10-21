---
artifact: roadmap
version: [version]
status: [draft | active | superseded]
owner: [responsible role or team]
---

# Roadmap: <Product>

> Describes how the product will grow: the small, independently deliverable increments that come next, in the order the human has chosen, and the ones already delivered, split or dropped.
> Each item is a future feature: one increment, specified, built and released on its own. The roadmap is where the next feature is chosen from, and where work deferred by a feature goes so that it is not lost.
> It plans the order of change, not the product itself. It never restates the product description, the requirements or the design: it points to them by ID.

---

## 1. Focus

Describe, in a few sentences, what the next items work towards: the product objectives and the capabilities they advance, referenced by ID from `product.md` (for example `CAP-02`).

State only the current direction. The product's purpose, vision and objectives belong in `product.md`.

---

## 2. Sequence

The items the human has placed, in priority order: the first item is the next feature to build.

The items near the top MUST be `ready` (section 5). Items further down MAY be coarse: a short outcome is enough until they come close to the top, when they are refined and, if needed, split.

For each item:

### RM-01: [Short name of the increment]

- **Status:** [candidate | ready]
- **Outcome:** [One sentence: what a named user group can do or observe once it is delivered]
- **Capability:** [CAP-nn from `product.md`, or "enabler" for groundwork with no user-visible outcome, with what it unblocks]
- **Why:** [The value it brings, or what it unblocks, and why it sits at this place in the order]
- **Depends on:** [RM-nn items that must be delivered first, or none]
- **Boundaries:** In: [what it covers] / Not in: [what is left to other items]
- **Origin:** [onboarding | the human | F<NNN> follow-up | split from RM-nn]
- **Notes:** [Open questions, risks or one-way doors it will meet, where known]

Repeat for each item, in order. Leave fields a coarse item cannot fill yet as `TBD`.

---

## 3. Inbox

Candidates not yet placed in the sequence: the follow-ups features leave behind, parts deferred when an item was split or narrowed, and ideas raised along the way. Each uses the item structure of section 2, with status `candidate`; an outcome and an origin are enough.

The inbox has no order. Only the human places an item in the sequence, or drops it.

---

## 4. Closed

Items that are no longer planned, kept so their IDs and history stay traceable. Move an item here when it closes, with one of:

- **Delivered:** [F<NNN>, and the date it was merged]
- **Split:** [into RM-nn, RM-nn, with the reason]
- **Dropped:** [the reason, and the human's decision]

Never delete an item, and never reuse its ID.

---

## 5. Readiness

An item is `ready`, and can be picked as the next feature, when:

- Its outcome is one sentence, for one user group, along one main flow, and can be shown working on its own.
- The product still works, and could be released, if work stops after it.
- It is a vertical slice through what users or callers observe, not a layer of the system.
- Every item it depends on is delivered.
- It needs at most one hard-to-reverse choice (one-way door).
- None of the size signals in the methodology applies, and it respects any sizing practice the constitution sets.

An item that is not ready is refined first, and split when it is too large. The methodology reference describes the size signals and the ways to split an item.

---

## 6. Maintenance Guidelines

This document MUST stay aligned with the product description, with what has been delivered, and with the human's priorities.

- The order of the sequence, placing an item from the inbox, and dropping an item are the human's decisions.
- A feature that narrows or splits its item, or defers part of its scope, adds the remainder to the inbox, on its own branch.
- The Document phase of every feature closes the item it delivered and adds the feature's follow-ups to the inbox.
- Whether an item is in progress is not recorded here: it is the feature whose state record names it.
- Bump `version` on every change.

### Source of Truth

- This document is the canonical reference for which increments come next, their order, and which are delivered, split or dropped.
- `product.md` describes the product as a whole and its capabilities, current and planned. An item names the capability it advances; it does not describe it.
- A feature's brief and requirements define what an item turns out to mean in detail, once it is picked.
- A feature's state record says whether its item is in progress.
- `architecture.md` holds the known technical debt; an item that pays some of it off points to it.

When information changes, update its authoritative source rather than maintaining competing copies across documents.
