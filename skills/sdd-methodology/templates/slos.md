---
artifact: slos
owner: reliability-engineer
status: draft
version: 1
upstream: []
---

# Service level objectives

<!-- One entry per user journey or service. Alert on error-budget burn rate, not raw thresholds. -->

### SLO-01: <journey>
sli: <good events / valid events, measured where users feel it>
target: <e.g. 99.5% over 28 days>
error-budget-policy: <what changes when the budget is exhausted>
alerting: <fast burn: 2% budget in 1h; slow burn: 10% in 3d>
source-nfrs: <F003:NFR-01, …>
dashboard: <link or path>
