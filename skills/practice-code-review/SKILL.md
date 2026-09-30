---
name: practice-code-review
description: How to review code changes in SDD — independent setup (task, ACs, design, contract, conventions; never the author's reasoning), re-running checks in a temporary review worktree, diff-reading order, checklists for correctness, error paths, boundaries, concurrency, data integrity, design conformance, maintainability, test quality (unit and acceptance tests), production concerns and scope/dependency hygiene, a severity guide, anti-patterns, and example findings. Use for task reviews, test reviews, whole-feature reviews and re-reviews.
---

# Practice: Code review

The yardstick is the **spec** — task, ACs, contract, design, conventions, constitution — not your taste. Findings use the schema, severity rules and budget in `practice-critique` and the communication contract.

## 1. Set up (independently)

1. Read the task (`refs`, `touches`, `done-when`), its ACs, the relevant `design.md` sections, `contracts/`, `conventions.md`, and `.sdd/dependencies.yaml`. You are **not** given the author's handoff note; don't go looking for it.
2. See the change: `git log --oneline <feature>..<task-branch>`, `git diff --stat <feature>...<task-branch>`, then the full diff.
3. **Re-run the checks** on the exact branch in a temporary worktree:
   ```
   git worktree add --detach .claude/worktrees/review-<T> <task-branch>
   uv run --directory .claude/worktrees/review-<T> pytest -q --cov --cov-report=xml
   uv run --directory .claude/worktrees/review-<T> ruff check .
   uv run --directory .claude/worktrees/review-<T> ruff format --check .
   uv run --directory .claude/worktrees/review-<T> pyright
   uv run --directory .claude/worktrees/review-<T> diff-cover coverage.xml --compare-branch=<feature> --fail-under=85
   uv run --directory .claude/worktrees/review-<T> pip-audit          (if dependencies changed)
   git worktree remove --force .claude/worktrees/review-<T>
   ```
   Use the `conventions.md` equivalents for other stacks. Record each result in the review notes. A red check is a `major` finding (or `critical` if it hides a broken AC).

## 2. Reading order

1. **Tests first** — what behavior do they claim? Do they match the ACs?
2. **Interfaces** — routes, schemas, public functions: do they match the contract exactly (paths, status codes, error codes, payloads, headers)?
3. **Logic** — services and domain code.
4. **Wiring** — registration, config, dependency injection, migrations.
5. **Everything else** — docs, lockfile, config files.

## 3. Checklists

**Correctness against the spec**
- [ ] Every AC in the task's `refs` is implemented, including the unwanted-behavior ACs
- [ ] Contract matched exactly; no undocumented fields, codes or behaviors
- [ ] Nothing implemented that no AC asks for (scope creep)

**Error paths and boundaries**
- [ ] Every external call has a timeout; failures map to the contract's errors
- [ ] No bare/catch-all exception handlers that swallow errors
- [ ] Boundaries handled: empty, one, max, max+1, unicode, whitespace, None/missing
- [ ] Retries only for idempotent operations

**Concurrency and data**
- [ ] Read-modify-write sequences protected (constraints, locks, transactions)
- [ ] Transactions scoped in the service layer; no partial writes on failure
- [ ] Migrations reversible and backward compatible with the previous release

**Design conformance**
- [ ] Module boundaries respected (only public `api` imports across modules)
- [ ] Testability seams used (injected clock/IDs, drainable workers)
- [ ] Observability as designed: structured logs without PII, named metrics, trace context

**Maintainability**
- [ ] Names say what things are; functions do one thing
- [ ] No duplication of existing helpers; no dead or commented-out code
- [ ] No speculative abstractions or configuration nobody asked for
- [ ] Types precise at boundaries; no unexplained `Any`, casts or suppressions

**Test quality**
- [ ] Unit tests cover new logic and its branches, not just the happy path
- [ ] Tests assert observable outcomes, not implementation details; no over-mocking
- [ ] Deterministic: no real time, randomness, sleeps or order dependence
- [ ] (test-review) Acceptance tests use only public interfaces, are tagged with their AC, show failure-for-the-right-reason evidence, and assert exactly what the AC says

**Security basics** — apply the `practice-security-basics` quick-check. Anything beyond it (threat-specific analysis) → one `pointer/security` finding.

**Scope and hygiene**
- [ ] Files changed ⊆ task `touches` (plus declared mechanical changes)
- [ ] Lockfile changes only add approved runtime deps or dev tools
- [ ] No debug output, leftover TODOs without `DEBT-nn`, or secrets

## 4. Severity guide

| Severity | Typical examples |
|---|---|
| critical | Data loss/corruption; injection; missing authorization; an AC silently unmet; a broken contract |
| major | Wrong error path; unhandled boundary; race; missing required timeout/log/metric; a test that doesn't really test; design violation; unapproved dependency; red check; unexplained suppression |
| minor | Unclear naming; small duplication; missing unit test for a branch |
| nit | Wording; readability the linter can't see |

"Different but valid" is **not** a finding. Put preferences in "Further polish" or leave them out.

## 5. Writing findings

Location as `path:line`. Evidence quotes the code and the spec it violates. Recommendation is concrete — a short code snippet is welcome, but you never commit it.

> **R1-02 (major, correctness/error-path)** `src/app/greeting/routes.py:18` — `except Exception:` returns 422 for every failure, so a database outage would be reported to clients as `invalid_name` (contract IF-01 defines 422 only for invalid input). Recommendation: catch `InvalidNameError` only; let other errors reach the global handler (500 problem details).

## 6. Modes

- **task-review / test-review**: §1–§5 on one task branch.
- **feature-review** (Verify, M/L): the integrated diff `main...<feature>`; focus on cross-task consistency (patterns, error handling, naming), duplicated helpers, dead code, conformance to the design as a whole. Re-run the full checks on the feature branch.
- **re-review**: verify each previous finding against the author's resolution first; then only regressions introduced by the fix.

## 7. Notes (mandatory, even when approving)

- Checks re-run and their results.
- Strengths to keep.
- Further polish (not findings).
