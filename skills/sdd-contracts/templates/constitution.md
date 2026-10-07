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
<!-- Technologies the human fixes as constraints are recorded in .sdd/stack.yaml with `fixed: true`.
     There are no other defaults: every other choice is derived from context (practice-tech-selection). -->
See `.sdd/stack.yaml`.

## Definition of Done (project additions)
<!-- The methodology's definition of done is the workflow exit checks (sdd-contracts). Add only what this project requires on top. -->
- [ ] <project-specific item>
