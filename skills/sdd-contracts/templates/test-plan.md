---
artifact: test-plan
feature: F000
owner: test-engineer
status: draft
version: 1
upstream: [requirements.md@1, design.md@1]
---

# Test plan: <feature name>

## Strategy
<!-- Levels (unit, integration, contract, e2e, property, load, security) and why each is needed here. -->

## AC → test mapping
| AC | Level | Test location | Notes |
|---|---|---|---|

## NFR verification
| NFR | Method | Tool | Threshold |
|---|---|---|---|

## Performance and resilience
<!-- Load profiles (arrival rate, mix, data volume, duration, pass criteria, environment), soak, and resilience experiments
     (failure injected, expected behavior, recovery). Profiles come from reliability-engineer's review. -->

## Evaluations (features with model calls)
<!-- Criteria and thresholds, dataset composition (typical, edge, adversarial, regression), graders, regression gate (ai-evals lens). -->

## Exploratory charters
<!-- 2–4 time-boxed charters: "Explore <area> with <resources> to discover <risk>". -->

## Mutation testing
<!-- Class L: modules in scope; equivalent mutants noted. -->

## Test data and environments

## Out of scope for testing
