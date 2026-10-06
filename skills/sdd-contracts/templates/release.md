---
artifact: release
feature: F000
owner: platform-engineer
status: draft
version: 1
upstream: [design.md@1, tasks.md@1]
---

# Release: <feature name>

## Change summary
## Version and changelog entry
## Readiness checklist
<!-- practice-release §1 -->
## Delivery strategy and health criteria
<!-- rolling | canary | blue-green | dark launch, with success signals and automatic rollback triggers -->
## Feature flags
<!-- owner, default state, removal date -->
## Rollout plan
<!-- Environments, order, feature flags, canary/percentage steps, success signals per step. -->
## Data migrations
<!-- Forward steps, backward compatibility window, verification. -->
## Rollback plan
<!-- Exact steps, time to roll back, data implications. Evidence it was exercised. -->
## Monitoring
<!-- Dashboards, alerts, what "healthy" looks like for 24h after release. -->
## Runbook updates
## Communication
<!-- release notes (external, via sync outbox), operator notes, deprecations -->
## Outcome
<!-- filled after the watch window -->
