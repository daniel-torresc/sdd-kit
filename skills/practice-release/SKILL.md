---
name: practice-release
description: How SDD releases software — trunk-based development with feature flags, semantic versioning and changelogs from Conventional Commits, rolling deploys with health checks and automatic rollback, canary only when the design requires it, migration ordering (expand/migrate/contract), rollback rehearsal, release.md, and the one-screen G3 package. Use when preparing a release, writing release.md or the G3 gate, or deploying.
---

# Practice: Release

## 1. Defaults

| Aspect | Default |
|---|---|
| Branching | Trunk-based: `main` is always releasable; features land behind **feature flags** when risky or incomplete |
| Versioning | Semantic versioning: breaking contract change → major, feature → minor, fix → patch |
| Changelog | Generated from Conventional Commits (`feat`, `fix`, `perf`, `!`/`BREAKING CHANGE`), edited for users |
| Deploy | **Rolling** with readiness checks; **automatic rollback** when health checks or error-rate thresholds fail during the bake window |
| Canary | Only when the design says so (high-risk change, large blast radius) — percentage steps with explicit success signals |

## 2. release.md

Write `specs/<f>/release.md` from the template:
- **Change summary** for users and operators; version bump and changelog entry.
- **Rollout plan**: environments in order (dev → staging → production), what "healthy" means at each step (readiness, error rate, latency vs NFR budgets), bake time, who/what decides to proceed.
- **Feature flags**: which, default state, how and when to remove them (a `DEBT-nn` if they linger).
- **Data migrations** in **expand → migrate → contract** order, each step backward compatible with the previous release; the contract step ships in a later release.
- **Rollback plan**: exact steps, expected time, data implications (what happens to rows written by the new version), and **rehearsal evidence**.
- **Monitoring**: dashboards and alerts to watch for 24 h; runbook links.

## 3. Rollback rehearsal

Before G3, in staging: deploy the new version, exercise it (smoke tests), roll back with the documented procedure, verify the old version works with any data the new one wrote, roll forward again. Record commands, timings and results in `release.md`. No rehearsal → not ready (unless the human explicitly accepts the risk at G3).

## 4. G3 package (one screen)

`gates/G3-production.md`:
- **Decision**: release `<feature>` as version `<x.y.z>` to production?
- **Evidence**: Verify verdict and evidence-pack link; CI status of the release commit; staging soak results; rollback rehearsal result.
- **Risk**: open `RISK-nn`, accepted exceptions, `DEBT-nn` going live, migration risk.
- **Options**: approve / approve with conditions (e.g. flag off by default) / hold.
- **Recommendation** (non-binding) and **what happens on approval**: merge to main, tag, protected production deploy (requires the human's reviewer approval in GitHub), watch window.

## 5. After approval

1. Merge `sdd/<F>-<slug>` to `main` (the human merges, or approves the merge).
2. Tag `v<x.y.z>`; publish release notes (external write — only after G3).
3. Trigger the production deploy workflow; the human approves the protected environment in GitHub.
4. Watch the bake window; on failure, automatic rollback — then report and open an incident if users were affected.
5. Record the outcome in `release.md` and the history.
