---
name: practice-release
description: How SDD gets a verified change to users safely, independent of technology — release readiness, versioning and changelogs, release types (feature, patch, hotfix, security fix), progressive delivery strategies (rolling, canary, blue-green, dark launch) and how to choose, feature-flag lifecycle, database and contract changes across releases, rollback design and rehearsal, verification and the watch window after release, communication, release.md, and the one-screen G3 package. Use when preparing, approving or executing a release.
---

# Practice: Release

A release is the moment risk meets users. The goal is a release that is **boring**: small, verified, observable, and reversible within minutes.

## 1. Readiness

A feature is ready to release when:
- Verify has passed (evidence pack, traceability clean, lens reviews approved);
- the artifact is built once and has already run in staging;
- migrations are ordered and rehearsed;
- the rollback has been rehearsed;
- monitoring and alerts for the change exist;
- the runbook is updated;
- the error budget allows it (an exhausted budget means hold or a D3);
- open risks are listed for the human.

## 2. Versioning and changelog

- **Semantic versioning** for anything with consumers: a breaking contract change bumps the major version, a feature the minor, a fix the patch.
- The changelog is generated from Conventional Commits, then edited for its readers: what changed for users and integrators, what they must do, and what was deprecated.
- Releases are tagged and their notes published after G3 (an external write the human approves in `decisions.md`).

## 3. Release types

| Type | Path | Notes |
|---|---|---|
| Feature release | Full flow through G3 | Default |
| Patch | Class S/T flow, G3 | Bug fix restoring specified behavior |
| Hotfix | Fast path: class T/S from the incident, minimal change plus regression test, review, G3 | Branch from the released version if main has moved; merge back immediately |
| Security fix | Like a hotfix, coordinated with security-engineer | Disclose only after the fix is out; external communication is the human's |

## 4. Choosing a delivery strategy

| Strategy | When | Health criteria |
|---|---|---|
| Rolling (default) | Most changes; stateless services with backward-compatible data | Readiness per instance; error rate and latency vs SLO during the roll |
| Canary | High-risk or large-blast-radius changes; when the design calls for it | Percentage steps (e.g. 1% → 10% → 50% → 100%) with an explicit success signal and bake time at each |
| Blue-green | Fast switch-back needed; changes hard to roll gradually | Full parallel environment; switch traffic and keep the old one warm through the watch window |
| Dark launch | Risky backends or new data paths | Ship off, exercise with shadow traffic or internal users, then enable |

**Automatic rollback** triggers on failed health checks or SLO-burn thresholds during the rollout, for every strategy.

## 5. Feature flags

- Use flags to **decouple deploy from release**: risky or incomplete behavior ships dark and is enabled deliberately.
- Every flag has an owner, a default state, a planned removal date and a debt entry. A flag that outlives its purpose is debt.
- Flags never replace authorization. Test both states of each flag in Verify.

## 6. Data and contracts across releases

- Migrations follow **expand → migrate → contract** across releases. Every release is compatible with the data of the previous one, so rollback is always possible.
- Contract changes follow the api-compat rules: additive within a version; breaking changes only with a new version or a deprecation window that has been communicated.

## 7. Rollback

Design the rollback before the rollout:
- the exact steps;
- the expected time;
- what happens to data written by the new version;
- who or what decides to trigger it.

**Rehearse it in staging**: deploy, exercise, roll back, verify the old version works with the new data, roll forward. Record the evidence in `release.md`. If rollback is impossible (a destructive migration), say so explicitly, and the human accepts that at G3.

## 8. After release

- **Watch window**: compare SLIs, error rates, latency and business signals against the pre-release baseline for a defined period (24 h by default).
- **Verification in production**: smoke checks of the critical journeys, and checks that the feature's metrics are flowing.
- **Close the release**: record the outcome in `release.md`, remove completed flags (as tasks), and hand the retro to the librarian.
- If users were harmed, open an incident.

## 9. Communication

Release notes for users and integrators: what changed, why it matters, what they need to do. Internal notes for operators: what to watch and how to roll back. Deprecations are announced with dates. Everything external is listed in `decisions.md` and needs the human's approval.

## 10. `release.md`

Write it from the template, covering:
- the change summary;
- version and changelog entry;
- the readiness checklist (§1);
- the strategy and its health criteria (§4);
- flags (§5);
- migration order (§6);
- the rollback plan and its rehearsal evidence (§7);
- monitoring for the watch window (§8);
- communication (§9).

## 11. G3 package (one screen)

The **G3 entry** in the feature's `decisions.md`:
- **Decision**: release `<feature>` as version `<x.y.z>` to production?
- **Evidence**: the Verify verdict and evidence pack, pipeline status of the release commit, staging soak, rollback rehearsal.
- **Risk**: open `RISK-nn`, accepted exceptions, debt going live, migration risk, error-budget status.
- **Options**: approve / approve with conditions (e.g. flag off by default, canary only) / hold.
- **Recommendation** (non-binding), and **what happens on approval**: merge, tag, protected production deploy (the human approves it in the deployment system), watch window.
