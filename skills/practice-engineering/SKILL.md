---
name: practice-engineering
description: How an SDD engineer implements a task — loading the right stack skills, reading before writing, working in an isolated worktree on an sdd/ task branch, making acceptance tests pass without touching them, small conventional commits, refactoring only while green and within scope, errors/logging/metrics/validation as part of the feature, the local definition of done (full suite, lint, types, diff coverage, migrations, contracts), the fix loop, debugging method, and the handoff note. Use when implementing, fixing, debugging or refactoring code for an SDD task.
---

# Practice: Engineering

## 1. Start of task

1. **Branch.** You run in your own worktree. Create the task branch from the current HEAD (the feature branch): `git switch -c sdd/<F>-<T>` using the task ID verbatim (e.g. `sdd/F001-T-04`). Confirm with `git status`.
2. **Load skills.** Invoke the skills named by the task's `stack` / `surface` (e.g. `stack-python`); if none are named, use the stack profile in `.sdd/architecture/conventions.md`. If a stack has no skill, read `.sdd/briefs/<stack>.md`.
3. **Read before writing**, in this order: the task (refs, touches, done-when, depends), its ACs in `requirements.md`, the relevant `design.md` sections and ADRs, `contracts/`, `conventions.md`, the acceptance tests for your ACs, then the existing code you will touch and its callers.
4. **Run the acceptance tests first** and confirm they fail for the expected reason. If they pass already, or fail for a reason unrelated to your task, stop and report (`blocked`, finding to test-engineer).

## 2. Implementing

- Work in **small steps**, each leaving the build green except for the not-yet-passing acceptance tests. Commit at each meaningful step.
- Follow the design's module boundaries and the contract exactly (names, status codes, error codes, payloads).
- **Production concerns are part of the step**, not a later task: input validation at the edge, authorization on every object access, explicit error handling mapped to the contract's errors, timeouts on outbound calls, structured logs (no PII), the metrics the design names.
- **Unit tests** for non-trivial logic you add (branches, calculations, parsing, state transitions). Integration tests against real infrastructure where the design's failure modes need proving.
- Check any API you are not sure of in current documentation (context7) before using it.
- Do not add abstractions for hypothetical futures. Three similar lines beat a premature framework.

## 3. Scope

- Change only what the task's `touches` covers.
- **Refactor freely inside `touches`**, only while tests are green, as separate commits (`refactor:`).
- Outside `touches`: only mechanical changes (rename, import, call-site update) — list each in the handoff note.
- Anything larger outside scope: don't do it. Add a `DEBT-nn` proposal or an enabler-task suggestion in the handoff note.
- A design or contract that does not work: stop and file a change request to the architect with evidence (failing experiment, doc citation). Never silently deviate.
- An acceptance test that contradicts its AC or the contract: file a finding to test-engineer. **Never edit acceptance, contract, e2e or perf tests** — the guard blocks it.

## 4. Dependencies

- Runtime dependencies: only those approved in `.sdd/dependencies.yaml`. The guard blocks others. Need a new one → return `blocked` with a D2 escalation to security-engineer (name, version, purpose, license, alternatives).
- Dev-only tools (`uv add --dev`, `npm install -D`) are D1: add and log them in `specs/<f>/log.md`.

## 5. Local definition of done

Run and pass, in this order, before handoff:

| Check | Python example |
|---|---|
| Format | `uv run ruff format --check .` |
| Lint | `uv run ruff check .` |
| Types | `uv run pyright` |
| Full test suite (not just yours) | `uv run pytest --cov --cov-report=xml` |
| Diff coverage ≥ 85% on changed lines — **after committing** (diff-cover only sees committed changes; untracked files are invisible to it) | `uv run diff-cover coverage.xml --compare-branch=<feature branch> --fail-under=85` |
| Migrations up and down (if any) | `uv run alembic upgrade head`, `uv run alembic downgrade -1`, `uv run alembic upgrade head` |
| Architecture rules | `uv run lint-imports` (if configured) |

Use the equivalents from `conventions.md` for other stacks. No new lint/type suppressions without an inline reason. No debug prints, commented-out code, or `TODO` without a `DEBT-nn`.

## 6. Fix loop

At most **3 attempts** per failing check. Each attempt: read the failure fully, form one hypothesis, change one thing, re-run. After the third failed attempt, stop and return `failed` with: what fails (exact output), the hypotheses tried, the evidence, and what you think is needed. The hub may re-dispatch attempts 2–3 on a stronger model; tech-lead takes over after that.

## 7. Debugging (debug mode)

1. **Reproduce** with a failing automated test at the lowest level that shows the bug.
2. **Localize**: read the stack trace, bisect (inputs, commits, code paths), add temporary logging if needed (remove it after).
3. **Fix the cause**, not the symptom; check for the same bug elsewhere.
4. The reproduction test stays as a regression test.

## 8. Commits

Conventional Commits, one logical change each, with the trailer:

```
feat(identity): hash passwords with argon2id

Refs: F001:T-04
```

Use `git commit -m "<subject>" -m "Refs: F001:T-04"`. Do not push — tech-lead integrates.

## 9. Handoff note (in the return envelope `summary`)

- **Changed:** what and where (modules, migrations, config).
- **Verified:** each check from §5 with its result; acceptance tests passing (IDs).
- **Outside touches:** mechanical changes made, if any.
- **Risks / follow-ups:** DEBT proposals, change requests filed, anything reviewers should look at first.
- **Skills loaded:** the stack/surface skills you invoked (or the brief you read).
- **Branch:** `sdd/<F>-<T>` (the task ID verbatim, e.g. `sdd/F002-T-02`) and the head commit SHA.
