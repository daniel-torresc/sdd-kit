---
name: practice-planning
description: How to derive an implementation plan from an approved SDD design — inventorying the work the design implies (components, interfaces, contracts, data changes and migrations, NFR budgets, failure handling, observability, fitness functions, enablers), grouping it into vertical slices that each deliver observable acceptance criteria, sequencing slices (walking skeleton, riskiest, most valuable), turning slices into small task specifications with test-first pairing, and checking the plan against the design for completeness. Use when writing or reviewing tasks.md, and when re-planning during Build.
---

# Practice: Deriving the plan from the design

A plan is the design translated into an order of work that delivers observable value early, retires risk early, and never leaves integration to the end. It describes **what** is built and **in which order**, never **how** (that is the design's and the engineer's job).

## 1. Inventory the work the design implies

Walk the approved design and list every unit of work it implies, with its source:

| Design element | Work it implies |
|---|---|
| Each component (`C-nn`) | Creating or changing it; its module boundary |
| Each interface (`IF-nn`) and contract | Implementing it exactly; contract tests |
| Data model changes | Schema changes and migrations (each step of expand → migrate → contract), backfills |
| NFR budgets and quality scenarios | Work to meet them (caching, async processing, limits) and to verify them |
| Failure-mode table | Timeouts, retries, degradation paths, recovery behavior |
| Observability section | Logs, metrics, traces, alerts, dashboards |
| Testability seams | Clock, ID generators, drainable workers, fakes for external systems |
| Fitness functions | Wiring each new architecture rule into CI |
| Runtime dependencies | Introduction (after dependency review) |
| Security mitigations (threat model) | Each control and its verification |
| UX states (ux.md) | Every state of every screen, not just the success path |
| Enablers | Scaffolding, environments, CI, test infrastructure, data fixtures |

Every inventory item must trace to a design element and, through it, to REQ/NFR IDs. An item that traces to nothing is scope creep. A design element with no work items is a gap in the plan.

## 2. Group into vertical slices

A slice is the smallest set of inventory items that makes one or more **acceptance criteria observable end to end**, through every layer they need. Group by:
- user-visible behavior (one flow or one AC cluster), happy path first, then the essential unwanted behaviors;
- never by technical layer ("all the data model", "all the endpoints").

Each slice states the ACs it makes pass. Enablers attach to the first slice that needs them, not to an up-front "setup phase".

## 3. Sequence the slices

1. **Walking skeleton**: the thinnest path that exercises the whole architecture (entry point → logic → storage → response, built, tested and deployable). Integration problems surface on day one.
2. **Riskiest slice next**: the most uncertain design decision, the least-known dependency, the performance-critical path. Learn while there is still time to change course.
3. **Highest-value slices**: those that move the brief's primary metric.
4. **The rest**, ordered by dependency.

Sequential constraints are real dependencies only: shared migrations, shared contracts, a component another slice builds on.

## 4. Turn slices into tasks

Each task is one reviewable change: one concern, small enough to understand in one sitting. Split larger work by sub-behavior, by AC, or with a preparatory refactoring task ("make the change easy, then make the easy change").

Every task specifies (machine-checked by `sdd.py trace --phase plan`):

| Field | Meaning |
|---|---|
| `refs` | REQ/AC IDs it delivers, or `enabler` |
| `depends` | Tasks that must be integrated first |
| `agent` | engineer, test-engineer or platform-engineer |
| `surface`, `stack` | Where it lives and which technologies are involved (descriptive) |
| `touches` | Paths or modules it will change, as precisely as possible, to detect conflicts between parallel tasks |
| `done-when` | Observable completion: named ACs passing, specific checks green |
| `risk` | `high` for security-sensitive, concurrency, data-migration or riskiest-slice work |

**Test-first pairing:** for every slice, a test-engineer task writes the acceptance tests for its ACs, and the engineer task depends on it. Tests for the next slice can be written while the current one is built.

**Parallelism:** tasks without a dependency path may run in parallel if their `touches` don't overlap. Shared hotspots (registration and wiring files, migration heads, lockfiles) are sequenced or owned by a single task.

## 5. Check the plan against the design

- Every inventory item from §1 is in exactly one task.
- Every AC is delivered by a task and tested by a test task that precedes it.
- Every design element has work, and every task traces to the design.
- The skeleton comes first, risk comes early, and integration is continuous.
- Nothing in the plan decides *how* to implement. If a task needs a design decision, that is a design gap: route it to the architect.

## 6. Re-planning

Re-plan (a new `tasks.md` version) when a task fails its fix loop, reveals a design or requirements gap, turns out much larger than planned, or when an upstream artifact changes. Keep completed task IDs, add new IDs, and mark dropped tasks `[withdrawn]`. When a task is stuck, decide one of the following, and log the decision:
- re-scope it (split);
- re-sequence it (add the missing prerequisite);
- send it upstream (design or requirements defect);
- re-dispatch it with better context;
- escalate.
