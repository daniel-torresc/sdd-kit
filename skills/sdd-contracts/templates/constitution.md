# Project Constitution

> Owned by the human. Changes are D3. Every agent reads this before acting.

## Purpose
<!-- One paragraph: what this product is for and for whom. -->

## Principles
<!-- Ordered: when two principles conflict, the higher one wins. -->
1. Correctness and data integrity over speed of delivery.
2. Security and privacy by design.
3. Simplicity: the simplest design that meets the REQs and NFRs.
4. Operability: every production path is observable and reversible.
5. Tests are specifications: every acceptance criterion has an automated test.

## Non-negotiables
- No secrets in the repository.
- No production change without a tested rollback path.
- No dependency with an unknown or copyleft license without a D3 decision.
- No PII in logs.

## Technology constraints
<!-- Technologies fixed by the human (not defaults — constraints every decision must respect),
     and technologies decided at G2, each with its ADR. There are no other defaults: choices are derived from context. -->
- Fixed by the human: <e.g. backend language>
- Decided (G2): <technology — ADR-NNNN>

## Definition of Done (feature)
- [ ] `sdd.py trace --phase verify` is clean
- [ ] Lint, formatter, type-checker and all tests green in CI
- [ ] All active lens reviews approve; no open blocking findings
- [ ] Every deferred finding is a RISK with an accepted gate
- [ ] Observability in place for every new external interface (logs, metrics, traces)
- [ ] User-facing and operational docs updated (README, runbook, API docs)
- [ ] Release plan with rollback path
