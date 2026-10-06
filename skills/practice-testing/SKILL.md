---
name: practice-testing
description: How to approach and perform testing in SDD, independent of technology — testing by risk, the purpose of each test level, turning Given/When/Then acceptance criteria into executable specifications, proving tests fail for the right reason, test data and determinism, contract testing, end-to-end and accessibility verification, verifying non-functional requirements (performance, timing, resilience, operability), mutation testing, exploratory testing, the evidence pack, flaky-test policy, and testability review of requirements. Use when writing test plans or tests, reviewing testability, diagnosing failures, or running Verify.
---

# Practice: Testing

Tests are the executable form of the specification. Their job is to give evidence that the system does what the spec says, and to fail loudly when it stops doing so.

## 1. Test by risk

For each slice, ask what would hurt users most if it broke, and what is most likely to break. Spend effort there. Record the reasoning in `test-plan.md`.

| Level | What it proves | Owner | Use when |
|---|---|---|---|
| Unit | A unit of logic behaves | engineer | Pure logic, edge cases, fast feedback |
| **Acceptance** | An AC holds through public interfaces with real infrastructure | **test-engineer** | Every AC |
| **Contract** | The implementation matches the published contract | **test-engineer** | Every external or public interface |
| Property-based | Invariants hold across generated inputs | test-engineer or engineer | Parsers, validators, calculations, state machines |
| **End-to-end** | A user journey works in the real client | **test-engineer** | Critical journeys only: few and stable |
| **Accessibility** | The UI is usable with a keyboard and assistive technology, and meets WCAG 2.2 AA | **test-engineer** | Every screen and state of a UI |
| **Non-functional** | Performance, timing, resilience and operability measures | **test-engineer** (profiles from reliability-engineer) | Every NFR with an executable verification |
| Mutation | The tests actually detect faults | **test-engineer** | Class L, changed code, in Verify |

## 2. From acceptance criterion to test

Each AC scenario becomes at least one test that:
- is **named after the behavior** and makes the Given/When/Then visible in its structure;
- carries the AC's fully qualified ID (the tagging rule in the artifacts contract);
- drives the system **only through public interfaces**: requests, the UI, published messages, CLI. It observes effects the way a user or consumer would: a response, a page, a delivered message, a record visible through an interface. It never reaches into internal modules to inspect state;
- asserts the **specific observable outcome** the AC names (exact status, message, state), never just "no error".

## 3. Fail for the right reason

Before implementation exists, run the new tests and record their failure:

| Right reason | Wrong reason (fix the test) |
|---|---|
| The behavior is missing (not found, not implemented) | Import or compilation error, broken fixture |
| An assertion on the expected outcome fails | Infrastructure not started, wrong configuration |
| | Timeout caused by the test itself |

A test that passes before implementation is either testing nothing, or the behavior already exists. Investigate before handing over.

## 4. Data, isolation and determinism

- **Real infrastructure for what we own** (databases, queues). Use **contract-faithful fakes only for what we don't own** (email delivery, payment providers, third-party APIs).
- Each test **creates its own data** through public interfaces or factories, with unique values. No shared mutable fixtures.
- **Inject time, randomness and identifiers.** Never sleep; wait on conditions with a deadline.
- Tests pass in any order and in parallel.

## 5. Contracts, journeys and accessibility

- **Contract tests**: exercise every documented operation and error against the running system, and generate inputs from the contract where possible. Validate produced messages against their schemas.
- **End-to-end tests**: select elements the way users perceive them (role, label, text), never by internal structure. One test per critical journey. Capture diagnostics on failure.
- **Accessibility verification**:
  - automated checks on every screen and state (empty, error, success, …);
  - a keyboard-only run of each journey;
  - a screen-reader spot check of critical flows;
  - findings that block a journey for assistive-technology users are critical.

## 6. Non-functional verification

For each NFR's `verify:` line, implement the check and record the measurement against its threshold:
- **Performance**: load profiles from reliability-engineer, run against production-like data volume; report percentiles and error rate.
- **Timing side channels**: repeated measurements compared statistically, never single samples.
- **Resilience**: inject the failures named in the design's failure-mode table and assert the specified behavior and recovery.
- **Operability**: health checks, alerts firing on simulated symptoms, and the rollback procedure (with platform-engineer).

## 7. Mutation testing

For class L, mutate the changed code and check that the tests notice. The score is informational. **Surviving mutants in code that implements an AC are `major` findings**, routed to whoever owns the gap (a missing assertion goes to test-engineer; missing unit tests go to engineer). Equivalent mutants are noted and ignored.

## 8. Flaky tests: zero tolerance

An intermittently failing test **blocks Verify**. Re-run only to diagnose (collect failures, seeds, timing), never to get a green result. Common causes are shared state, order dependence, real time, unbounded waits, resource collisions, and genuine races in the product. Fix the cause. A race in the product is a bug routed to the engineer.

## 9. Testability review (Specify)

For each AC: is the outcome observable? Are the values concrete? Is the precondition achievable in a test? For each NFR: is `verify:` executable, with a threshold and an environment? Send findings to product-lead with a suggested rewrite.

## 10. Verify phase

1. Run the full suite with machine-readable results into `specs/<f>/evidence/`, and run `sdd.py trace --phase verify --junit <report>`.
2. Execute every NFR verification and record the measurements.
3. Class L: mutation testing (§7).
4. UI or public API: **exploratory testing**. Run 2–4 time-boxed charters ("Explore <area> with <resources> to discover <risk>") against the running system, and file findings.
5. Write the **evidence pack** `specs/<f>/evidence/README.md`:
   - per AC: the tests, the result, and a screenshot or request/response transcript;
   - per NFR: the measurement against its threshold;
   - accessibility results;
   - exploratory notes and known risks.
6. Write the verdict in `reviews/verify-test-engineer-r<n>.md`. Approve only if the suite is green, the trace is clean, NFRs are met, there are no flaky tests and no blocking findings remain.

## 11. Reviewing tests (yours and others')

- [ ] Every AC in scope tagged and tested through public interfaces
- [ ] Failure before implementation recorded, for the right reason
- [ ] Real infrastructure for what we own; fakes only at external boundaries
- [ ] Deterministic, order-independent, owns its data
- [ ] Assertions specific to the AC's observable outcome
- [ ] Unwanted-behavior, boundary and accessibility ACs covered, not just happy paths
