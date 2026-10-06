---
artifact: review
feature: F000
owner: <reviewer-agent>
status: draft
version: 1
upstream: [<target>.md@<n>]
---

```yaml
review:
  target: <artifact>@<version>
  reviewer: <agent>
  round: 1
  verdict: approve   # approve | approve-with-comments | changes-required | blocked
findings:
  - id: R1-01
    severity: minor  # critical | major | minor | nit | suggestion
    blocking: false
    category: <area/sub-area>
    location: "<file>#<ID> or <path>:<line>"
    refs: []
    claim: ""
    evidence: ""
    recommendation: ""
    confidence: high # high | medium | low
    route_to: <owner-agent>
    resolution:      # fixed | rejected | deferred  (author fills in)
    rationale:
```

## Notes
<!-- Optional: overall assessment, strengths worth keeping. -->
