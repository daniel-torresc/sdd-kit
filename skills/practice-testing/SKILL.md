---
name: practice-testing
description: How to verify software in SDD — risk-based test strategy, test levels and when to use each, turning Given/When/Then acceptance criteria into executable tests, proving tests fail for the right reason, fixtures and test data, determinism, contract testing, e2e and accessibility testing, NFR verification (load, timing, availability), mutation testing, exploratory charters, the evidence pack, flaky-test policy, and testability review. Use when writing test-plan.md or tests, reviewing requirements for testability, reviewing test tasks, diagnosing failing tests, or running the Verify phase.
---

# Practice: Testing

## 1. Strategy: test by risk

For each slice, ask: what would hurt users most if it broke, and what is most likely to break? Spend test effort there. Write the answer in `test-plan.md` → *Strategy*.

| Level | Proves | Owner | Use when |
|---|---|---|---|
| Unit | A function/class behaves | engineer | Pure logic, edge cases, fast feedback |
| **Acceptance** | An AC holds through public interfaces (HTTP/UI/CLI/events) with real infrastructure | **test-engineer** | Every AC |
| **Contract** | The implementation matches `contracts/` (and consumers' expectations) | **test-engineer** | Every external/public interface |
| Property-based | Invariants hold for generated inputs | test-engineer or engineer | Parsers, validators, money/time math, state machines |
| **E2E (UI)** | A user journey works in a real browser | **test-engineer** | Critical journeys only — few, stable |
| **Accessibility** | WCAG 2.2 AA automated checks | **test-engineer** | Every UI screen (axe via Playwright) |
| **NFR** | Performance, timing, resilience, availability measures | **test-engineer** (thresholds reviewed by reliability-engineer) | Every NFR with an executable `verify:` |
| Mutation | Tests actually detect faults | **test-engineer** | Class L, changed modules, in Verify |

## 2. From acceptance criterion to test

```python
@pytest.mark.ac("F001:AC-03.1")
async def test_unregistered_email_gets_same_confirmation_and_no_email(client, mailbox):
    # Given no account exists for bob@example.com
    # When a reset is requested for bob@example.com
    response = await client.post("/password-reset", data={"email": "bob@example.com"})
    # Then the same confirmation is shown
    assert response.status_code == 200
    assert "If an account exists for this email" in response.text
    # And no email is sent
    assert await mailbox.messages_to("bob@example.com") == []
```

Rules:
- One test per AC scenario at minimum; name it after the behavior; the Given/When/Then is visible as structure.
- Tag with the fully qualified AC (or NFR) ID so `sdd.py trace` can map it.
- Drive through **public interfaces only** (HTTP via ASGI client, the UI via Playwright, CLI, published events). Never import internal modules to assert state; observe effects the way a user or consumer would (a response, a page, a message in a captured mailbox, a record visible through an API).
- Assert the specific observable outcome from the AC — exact status, message key, state — not "no error".

## 3. Fail for the right reason

Before handing over a test task, run the new tests against the current branch and record the output in the handoff:

| Right reason (✅) | Wrong reason (❌ fix the test) |
|---|---|
| 404/405 for a route that doesn't exist yet | ImportError, fixture error, syntax error |
| Assertion mismatch on the expected outcome | Connection refused because the test DB isn't started |
| NotImplemented from a stub the plan created | Timeout from a `sleep` or bad wait |

A test that **passes** before implementation is either testing nothing or the behavior already exists — investigate.

## 4. Fixtures, data, determinism

- **Real infrastructure**: PostgreSQL via testcontainers (one container per session, a transaction or schema per test). Never SQLite as a stand-in.
- **Fakes only for what we don't own**, behind the same contract: an SMTP capture server (e.g. Mailpit) for email, a stub payment provider, a fake clock.
- Each test **creates its own data** through public interfaces or factories; no shared mutable fixtures; unique values (emails, IDs) per test.
- **Inject time and randomness** (clock, ID/token generator, seed). No `sleep`; wait on conditions with a deadline.
- Tests pass in any order and in parallel (`pytest -p no:randomly` must not be needed).

## 5. Contract, e2e, accessibility

- **Contract**: run schemathesis (OpenAPI) against the running app; add explicit examples for every documented error. Payload schemas (JSON Schema) are validated on produced messages.
- **E2E**: Playwright; select by role/label/text (accessible selectors), never CSS internals; one test per critical journey; trace and screenshot on failure.
- **Accessibility**: axe checks on every screen and state (empty, error, success); keyboard-only path for each journey.

## 6. NFR verification

For each NFR `verify:` line, implement the check and record the measurement:
- **Latency/throughput**: k6 or locust against an environment with realistic data volume; report p50/p95/p99 and error rate against the threshold.
- **Timing parity / side channels**: repeated measurements with a statistical comparison (median difference and a test such as Mann–Whitney), not single samples.
- **Resilience**: inject the dependency failure named in the design's failure-mode table (stop the container, add latency) and assert the specified behavior.
- **Availability/operability**: verify health endpoints, alerts firing on simulated symptoms, rollback procedure (with platform-engineer).
Thresholds are reviewed by reliability-engineer; you run and report.

## 7. Mutation testing (class L, Verify)

Run mutmut (Python) on the changed modules. The score is informational. **Surviving mutants in code that implements an AC are `major` findings** routed to the owner of the gap (a missing assertion → yourself; missing unit tests → engineer). Equivalent mutants are noted and ignored.

## 8. Flaky tests — zero tolerance

A test that fails intermittently **blocks Verify**. Re-run only to diagnose (collect failures, seeds, timing), never to get green. Typical causes: shared state, order dependence, real time, async waits, port collisions, test data collisions, a real race in the product. Fix the cause; if the cause is in production code, it's a bug routed to the engineer.

## 9. Testability review (Specify)

For each AC: observable outcome? concrete values? precondition achievable in a test? For each NFR: is `verify:` executable, with a threshold and an environment? Findings go to product-lead with a rewrite suggestion.

## 10. Verify phase

1. Run the full suite with JUnit output into `specs/<f>/evidence/` and run `sdd.py trace --phase verify --junit <report>`.
2. Execute every NFR verification; record measurements.
3. Class L: mutation testing (§7).
4. UI or public API: **exploratory testing** — 2–4 time-boxed charters ("Explore <area> with <resources> to discover <risk>"), driving the running app with Playwright; file findings.
5. Write the **evidence pack** `specs/<f>/evidence/README.md`: per AC → test(s), result, screenshot or request/response transcript; per NFR → measurement vs threshold; exploratory notes; known risks.
6. Write the verdict `reviews/verify-test-engineer-r<n>.md` in the findings schema: `approve` only if the suite is green, trace is clean, NFRs are met, no flaky tests, and no blocking findings.

## 11. Review checklist for tests (yours and others')

- [ ] Every AC in scope tagged and tested through public interfaces
- [ ] Failure-before-implementation recorded, for the right reason
- [ ] Real infrastructure; fakes only for external systems
- [ ] Deterministic, order-independent, own data
- [ ] Assertions are specific to the AC's observable outcome
- [ ] Unwanted-behavior and boundary ACs covered, not just happy paths
