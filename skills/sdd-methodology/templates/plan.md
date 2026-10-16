---
artifact: plan
feature: [feature ID]
status: [draft | checked | superseded]
version: [version]
upstream: [design.md@version, requirements.md@version]
---

# Plan: <feature name>

> Describes how to approach each task in the design's task list: what it delivers, what it depends on, the technologies, skills and files it involves, how it is checked, and its risks.
> It is the approved design made concrete, detailed enough that a task can be started without guessing. It contains no code.
> Each task is defined here once. The design's task list is the overview the human approved; this plan never changes the design.

---

## Conventions

Every task is defined by a heading that starts with its ID: `### T-01: [Title]`.

The tasks and their IDs MUST match the design's task list. A task added later, such as a fix task after Verify, takes the next free number and is added to both.

IDs MUST remain stable once referenced by other artifacts, including commits and tests. A withdrawn task keeps its ID and its heading, with `[withdrawn]` appended. Withdrawn IDs are never reused.

---

## 1. Tasks

Define each task in the design's task list.

Each task MUST state what it delivers, what it depends on, the technologies and files it involves, and how it will be checked. Keep each task small enough to build and review on its own.

### T-01: [Short title]

- **Delivers:** [AC-01.1, AC-01.2, or Enabler: what groundwork it lays]
- **Implements:** [C-nn, IF-nn from the design]
- **Depends on:** [T-nn, or None]
- **Stack:** [stack.yaml concerns]
- **Skills:** [Skills catalogue entries to load for this task, or None]
- **Files:** [Files and folders it creates or changes]
- **Fixes:** [Review finding IDs, for a fix task only]

**Approach:** [What to build and in what order; the interfaces from the design it implements or uses]

**How it is checked:** [The tests that will show each acceptance criterion holds, and any other check]

**Technical requirements:** [Constraints from the design: error handling, limits, compatibility, security]

**Risks:** [What could go wrong, and what to watch for]

Repeat for each task.

---

## 2. Order

Summarize the order the dependencies impose. Tasks in the same group don't depend on each other and can be built in parallel.

| Group | Tasks | Waits for |
|---|---|---|
| 1 | [T-01, T-02] | None |
| 2 | [T-03] | [Group 1] |

---

## 3. Consistency Check

Before Build starts, verify that:

- The tasks match the design's task list, with the same IDs.
- Every acceptance criterion is delivered by at least one task.
- Every task names what it delivers, its stack, and its files.
- Every task implements components or interfaces from the design, or is an enabler.
- The dependencies have no cycles.
- Tasks that can run in parallel don't change the same files, or the overlap is intended and stated.

Record the result:

- **Consistency:** [Clean | Issues found]
- **Issues:** [None | Each issue, and how it was resolved]

---

## 4. Maintenance Guidelines

This document MUST remain aligned with the approved design and the requirements.

Bump `version` on every change, and keep `upstream` pointing to the versions of the design and the requirements it is built from. When either of them changes, check this plan again: confirm it by updating `upstream`, or revise it.

The plan has no approval of its own: its status becomes `checked` once it passes the consistency check. A change that would alter the approved design is a change to the design, and goes back to the human through it.

### Source of Truth

- This document is the canonical reference for how each task is approached.
- The design defines the approach and the task list; this plan details it and never changes it.
- The requirements define the acceptance criteria each task delivers.
- The feature's state record tracks the status of each task during Build.

When information changes, update its authoritative source rather than maintaining competing copies across documents.
