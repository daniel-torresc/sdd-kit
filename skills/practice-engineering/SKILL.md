---
name: practice-engineering
description: How an SDD engineer approaches implementation work, independent of technology — understanding before changing, working from the task and its acceptance tests (never editing them), small verified steps, scope discipline, production concerns as part of every change, dependency discipline, the local definition of done, the fix loop, systematic debugging, refactoring safely, commits, and the handoff note. Use when implementing, fixing, debugging or refactoring code for an SDD task.
---

# Practice: Engineering

## 1. Understand before changing

Before writing anything, read in this order:
1. the task (`refs`, `touches`, `done-when`, `depends`);
2. its ACs;
3. the relevant design sections and ADRs;
4. the contracts;
5. the project conventions (`.sdd/architecture/conventions.md`) and stack (`.sdd/stack.yaml`);
6. the acceptance tests for your ACs;
7. the code you will touch, and its callers.

Then run the acceptance tests and confirm they fail for the expected reason. If they pass already, or fail for an unrelated reason, stop and report it.

When the change touches existing code you did not write, protect current behavior first: `practice-cartography` §6 (characterization tests, seams, incremental change).

When you are unsure how a library, framework or platform behaves, check its current documentation before relying on it. Memory of an API is not evidence.

## 2. The tests define done

The acceptance tests are the executable specification, and they are owned by test-engineer. **You never edit them.** If one contradicts its AC or the contract, file a finding to test-engineer and wait. Your own unit and integration tests cover the logic you add: branches, calculations, parsing, state transitions, and the failure modes the design names.

## 3. Small, verified steps

Work in steps that each leave the build green, apart from the acceptance tests that aren't passing yet. Commit each meaningful step. Make it work, then make it right: refactor only while tests are green, and in separate commits.

## 4. Production concerns are part of the change

Every change carries the following, as the design specifies:
- input validation at the boundary;
- authorization on every object access;
- explicit error handling mapped to the contract's errors;
- timeouts on outbound calls;
- structured logs without sensitive data;
- the metrics and traces the design names.

None of these is a later task.

## 5. Scope discipline

- Change what the task's `touches` covers.
- Inside that scope, improve freely while tests are green.
- Outside it, make only mechanical changes (rename, import, call-site update), and declare each one in the handoff.
- Anything larger outside scope: don't do it. Propose it as debt or as an enabler task.
- A design or contract that doesn't work in practice: stop and file a change request to the architect with evidence (a failing experiment, a documentation citation). Never deviate silently.
- No speculative abstractions. Build for the requirements in front of you, not imagined futures.

## 6. Dependencies

Only runtime dependencies approved in `.sdd/dependencies.yaml`. If you need a new one, return `blocked` with an escalation to security-engineer: name, version, purpose, license, alternatives. Development-only tools are your decision, and you log them.

## 7. Local definition of done

Before handoff, run the project's checks (the registered commands in `.sdd/commands.yaml`) and pass all of them:
- formatting and linting;
- type checking (where the stack has it);
- the **full** test suite, not just your tests;
- diff coverage at or above the configured minimum, measured **after committing**;
- migrations up and down, if you added any;
- architecture rules (fitness functions).

No new suppressions without an inline reason, no debug output, no commented-out code, and no TODO without a debt entry.

## 8. Fix loop

At most the configured number of attempts per failing check. Each attempt reads the failure fully, forms one hypothesis, changes one thing and re-runs. When attempts are exhausted, stop and return `failed` with:
- the exact failure;
- the hypotheses you tried;
- the evidence;
- what you think is needed.

## 9. Debugging

1. **Reproduce** with a failing automated test at the lowest level that shows the bug.
2. **Localize**: read the full error, bisect inputs, commits and code paths, and add temporary instrumentation (then remove it).
3. **Fix the cause**, not the symptom, and look for the same bug elsewhere.
4. Keep the reproduction as a regression test.

## 10. Commits and handoff

Follow the commit conventions in the workflow contract. Your return envelope's `summary` is the handoff note:
- **Changed**: what, where.
- **Verified**: each check and its result; the acceptance tests passing, by ID.
- **Outside touches**: the mechanical changes, if any.
- **Risks and follow-ups**: debt proposals, change requests filed, where reviewers should look first.
- **Branch**: the task branch and the head commit SHA.
