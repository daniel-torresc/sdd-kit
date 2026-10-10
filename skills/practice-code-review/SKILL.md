---
name: practice-code-review
description: How to perform effective code review in SDD, independent of technology — reviewing against the spec rather than taste, independent setup (never the author's reasoning), re-running the project's checks on the exact change, reading order, what to look for (correctness against ACs and contracts, error paths and boundaries, concurrency and data integrity, design conformance, maintainability, test quality, security, accessibility, production concerns, scope and dependency hygiene), severity, writing findings that teach, and modes for task, test, feature and re-reviews.
---

# Practice: Code review

A review exists to catch what would hurt users, operators or future maintainers, and to confirm quickly when a change is sound. The yardstick is the **spec** (task, ACs, contract, design, conventions, constitution), not personal preference. Findings follow the schema, severity rules and budget in `practice-critique` and the communication contract.

## 1. Set up independently

1. Read the task, its ACs, the relevant design sections, the contracts, the conventions and the approved dependencies. You are not given the author's handoff note: judge the change, not the story about it.
2. See the change as a whole first (commits, files changed), then in detail.
3. **Re-run the project's checks yourself** on the exact change, in an isolated checkout of the task branch: tests, linting, type checks, diff coverage, dependency audit when dependencies changed. A red check is a `major` finding, or `critical` if it hides an unmet AC. Clean up the checkout afterwards.

## 2. Reading order

1. **Tests**: what behavior do they claim, and does it match the ACs?
2. **Interfaces**: do they match the contract exactly (operations, inputs, outputs, errors)?
3. **Logic**: the core behavior.
4. **Wiring**: registration, configuration, migrations.
5. **Everything else**: docs, dependency manifests, configuration files.

## 3. What to look for

**Correctness against the spec.** Every AC in scope is implemented, including the unwanted behaviors. The contract is matched exactly. Nothing is implemented that no AC asks for.

**Error paths and boundaries.**
- External calls have timeouts.
- Failures map to the contract's errors.
- No error is swallowed by a catch-all.
- Boundaries are handled: empty, one, max, max+1, unusual characters, missing values.
- Retries only happen on idempotent operations.

**Concurrency and data integrity.**
- Read-modify-write sequences are protected.
- Transactions are scoped so failures leave no partial writes.
- Migrations are reversible and compatible with the previous release.

**Design conformance.**
- Module boundaries are respected.
- The design's testability seams are used.
- Observability is as designed: structured logs without sensitive data, the named metrics and traces.

**Maintainability.**
- Names say what things are.
- Units do one thing.
- No duplication of existing helpers, no dead code, no speculative abstractions.
- Types are precise at boundaries.
- Suppressions carry a reason.

**Test quality.**
- New logic and its branches are covered.
- Tests assert observable outcomes, not implementation details, without excessive mocking.
- Tests are deterministic.
- For test reviews: acceptance tests use only public interfaces, are tagged with their AC, show failure-before-implementation evidence, and assert exactly what the AC says.

**Security.** The principles in `practice-security`: validated and bounded inputs, no injection paths, authorization per object, correct token and secret handling, no sensitive data in logs or errors, safe parsing. Anything needing threat-specific analysis gets a one-line pointer to security-engineer.

**Accessibility (UI changes).**
- Semantic structure.
- Every control labeled and keyboard-operable, with visible focus.
- Errors identified in text.
- Sufficient contrast.
- No information conveyed by color alone.
- Focus managed on navigation and dialogs.

**Scope and hygiene.**
- Changed files fall within the task's `files` (plus any declared mechanical changes).
- Dependency changes add only approved runtime dependencies.
- No debug leftovers, no TODOs without a debt entry, no secrets.

## 4. Severity

| Severity | Typical examples |
|---|---|
| critical | Data loss or corruption; an injection path; missing authorization; an AC silently unmet; a broken contract; a journey blocked for keyboard or screen-reader users |
| major | Wrong error path; unhandled boundary; race; a required timeout, log or metric missing; a test that doesn't really test; design violation; unapproved dependency; red check; unexplained suppression |
| minor | Unclear naming; small duplication; a missing unit test for a branch |
| nit | Wording; readability the tooling can't catch |

"Different but valid" is **not** a finding. Preferences go under "Further polish" or nowhere.

## 5. Findings that teach

Give the location as `path:line`. Evidence quotes the code and the spec it violates. The recommendation is concrete: a short snippet is welcome, but you never commit it.

> **R1-02 (major, error-path)** `greeting/routes:18`: a catch-all handler turns every failure into `invalid_name`, so a database outage would be reported to clients as invalid input. Contract IF-01 defines that error only for invalid input. Recommendation: handle only the invalid-input error here and let others reach the global handler.

## 6. Modes

- **task-review / test-review**: §1–§5 on one task branch.
- **feature-review** (Verify, every class): the integrated change against the main branch. Focus on consistency across tasks, duplicated helpers, dead code, and design conformance as a whole. Re-run the checks on the feature branch.
- **re-review**: check each previous finding against the author's answer (answers file) first, then look only for regressions the fix introduced.

## 7. Notes (always, even when approving)

- Checks re-run and their results.
- Strengths to keep.
- Further polish (not findings).
