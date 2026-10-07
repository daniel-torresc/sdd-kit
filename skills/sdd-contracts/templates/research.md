---
artifact: research
id: Q-00
kind: question            # question | technology-options | technology-reference | codebase-investigation | spike | domain
feature: F000
owner: researcher         # or cartographer (codebase-investigation), architect (spike)
status: done              # in-progress | done | superseded
version: 1
asked-by: <agent>
---

# Research: <what was investigated>

## Why
<!-- The question in one sentence, the decision it informs, who decides, and what "answered" means. -->

## How
<!-- Approach: sources consulted, code examined, experiment run (for a spike: what was built, how it was measured, time box). -->

## Findings
<!-- Each finding with its confidence (high | medium | low). Facts cited; inferences labeled. -->

### 1. <finding>
confidence: high

## Options (if a choice is being informed)
<!-- For technology choices: criteria from context, the reference option, every viable option with symmetric depth,
     one-line exclusions (practice-tech-selection). -->

| Option | Fit (REQ/NFR) | Evidence | Cost | Reversal cost | Risks |
|---|---|---|---|---|---|

## Conclusion
<!-- The answer in 3–5 lines, with overall confidence. A recommendation, if asked for, clearly marked as such. -->

## Decision taken
<!-- Filled once decided: what was decided, by whom, where it is recorded (decisions.md, ADR, stack.yaml). -->

## Open questions
<!-- What could not be established, and how it could be. -->

## Sources
| # | Source | Type (primary / secondary / tertiary / code) | Retrieved |
|---|---|---|---|
