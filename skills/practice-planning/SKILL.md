---
name: practice-planning
description: How to turn an SDD design into an executable build plan and run it — vertical slicing, walking skeleton, dependency graphs, task sizing, risk-first ordering, test-first pairing with separate test-engineer tasks, conflict detection via touches, done-when criteria, parallelism limits, re-planning triggers, integration of parallel worktree branches, and git branch/commit conventions. Use when writing or reviewing tasks.md, coordinating the Build phase, or integrating task branches.
---

# Practice: Planning and integration

## 1. From design to slices

1. List the ACs and group them into **vertical slices**: each slice is a user-observable behavior that crosses every layer it needs (UI → API → logic → storage) and can be tested end to end.
2. Order slices: **walking skeleton** → **riskiest slice** (most uncertain design, external dependency, performance-critical path) → **highest-value slices** → the rest.
3. Identify **enablers** the slices need: scaffolding, CI, migrations, contract wiring, fitness functions, observability. Make each an explicit `refs: enabler` task placed just before its first consumer — not all up front.
4. Write the slice table at the top of `tasks.md`: slice → tasks → ACs → why this position.

Never slice by layer ("all models", "all endpoints", "all screens"). Never leave integration or "wire it together" for the end.

## 2. Walking skeleton (T-01)

The thinnest path that exercises the whole architecture (its `.gitignore` includes `.claude/worktrees/`, where agent worktrees live): the app starts, one trivial request goes through every layer that exists in the design (including the database and the deployed environment), CI runs lint, types and tests on it. For brownfield work, the skeleton is the thinnest path through the *changed* parts. If none makes sense, say why.

## 3. Tasks

Each task has (machine-checked by `sdd.py trace --phase plan`):

| Field | Rule |
|---|---|
| `refs` | REQ/AC IDs it delivers, or `enabler` |
| `depends` | Tasks that must be **merged** before it starts |
| `agent` | `engineer`, `test-engineer`, or `platform-engineer` |
| `surface` / `stack` | Used by the hub to load skills |
| `touches` | Paths or modules it will change — as specific as possible |
| `done-when` | Observable: named ACs passing, specific checks green |
| `risk` (optional) | `high` for security-sensitive, concurrency, data-migration or riskiest-slice work — the engineer runs on opus |

**Size**: one concern; roughly ≤ 400 changed lines; one reviewer can understand it in one sitting. Bigger → split by sub-behavior, by AC, or by "make the change easy, then make the easy change" (a preparatory refactor task first).

## 4. Test-first pairing

For each slice:
- a **test-engineer task** writes the acceptance tests for the slice's ACs (they must fail for the right reason);
- the **engineer task** that implements those ACs `depends` on it.

Tests for slice n+1 can be written while slice n is implemented. Unit tests stay with the engineer. Waiving test-first (`test-first: waived — <reason>`) needs test-engineer agreement and a logged reason (e.g. a pure refactor covered by existing tests).

## 5. Parallelism and conflicts

- Tasks with no dependency path between them may run in parallel, up to `parallelism.max_parallel_tasks` in `.sdd/config.yaml`.
- Parallel tasks must have **non-overlapping `touches`**. The trace script warns on overlap; resolve by adding a dependency, narrowing `touches`, or accepting the merge-order risk explicitly in the slice table.
- Shared hot files (router registration, dependency injection wiring, migration heads, lockfiles) are the usual conflict sources: give their changes to one task or sequence them.
- Migrations: one migration head at a time — tasks that add migrations are sequenced.

## 6. Re-planning triggers

Re-plan (new `tasks.md` version) when: a task fails its fix loop; a task discovers a design or requirements gap (after the change request is resolved); a task is much larger than planned; an upstream artifact changes (stale). Keep completed task IDs; add new IDs; mark dropped tasks `[withdrawn]`.

## 7. Stepping in after a failed fix loop

When an engineer task fails its fix-attempt cap: read the failing output, the diff and the task. Decide one of:
1. **Re-scope** — the task was too big: split it.
2. **Re-sequence** — a missing prerequisite: add an enabler task first.
3. **Upstream** — the design or an AC is wrong/infeasible: change request to the owner, pause the task.
4. **Re-assign context** — the engineer lacked context: re-dispatch with the specific files, contract or error explained.
5. **Escalate** — none of the above works within the loop cap: D3.
Log the decision.

## 8. Git conventions

| Thing | Convention |
|---|---|
| Feature branch | `sdd/F003-<slug>` from the main branch |
| Task branch | `sdd/F003-T-04` (task ID verbatim), in its own worktree, from the feature branch |
| Commits | Conventional Commits (`feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`) with trailer `Refs: F003:T-04` |
| Merge of task → feature | `git merge --no-ff sdd/F003-T-04` (keeps task boundaries visible) |
| Feature → main | Only through G3 (human) |

Autonomy: local branches, worktrees and merges into `sdd/*` branches are autonomous; pushing `sdd/*` branches and opening **draft** PRs is autonomous; merging into the main or release branch requires the human (G3).

## 9. Integration

Integrate each task as soon as it is approved by code review — not in batches.

1. On the feature branch, merge task branches **in dependency order**.
2. After each merge, run the full test suite (and lint/types). Record the result.
3. **Conflicts**: resolve only trivial, mechanical ones yourself (both sides added imports/registrations/list entries; whitespace; lockfile regenerated by the tool). Anything touching logic → abort the merge (`git merge --abort`) and route to the engineer who owns the later task, with the conflict listed.
4. **Red after merge** → identify the offending merge (the last one, or bisect), revert it on the feature branch if needed, route the failure to that task's engineer.
5. Write `reviews/integration-tech-lead-<n>.md`: merged tasks, commit SHAs, test results, open problems.
6. Push the feature branch and keep a draft PR updated so CI runs.

## 10. Plan self-review

- [ ] `sdd.py trace --phase plan` clean; overlap warnings resolved or accepted in the slice table
- [ ] T-01 is a walking skeleton (or the reason there isn't one is stated)
- [ ] Vertical slices; riskiest work early; no integration left to the end
- [ ] Every task ≤ one concern / ~400 lines; `done-when` observable
- [ ] Test-engineer task precedes every engineer task for the same ACs
- [ ] Enablers present: CI, migrations, contract wiring, fitness functions, observability
- [ ] Hot files and migrations sequenced
- [ ] You planned the *what* and the *order* — not the implementation
