---
name: practice-reliability
description: Reliability and performance practice for the SDD reliability-engineer — SLIs, SLOs and error budgets; reviewing NFRs for realism and measurability; capacity estimation; reviewing designs for failure modes, timeouts, retries, idempotency, backpressure, graceful degradation and observability; load-profile and resilience-experiment design; performance diagnosis and profiling; alert quality (symptom-based, actionable, runbook-linked); release and rollout review; and post-incident reliability actions. Use for NFR and design reviews, SLO definitions, performance/resilience plans, perf diagnosis, and release reviews.
---

# Practice: Reliability and performance

## 1. SLIs, SLOs, error budgets

For every user-facing service or critical journey, define in `.sdd/operations/slos.md`:
- **SLI** — a ratio of good events to valid events, measured where users experience it (e.g. "requests to /checkout answered 2xx/3xx in < 800 ms").
- **SLO** — target over a window (e.g. 99.5% over 28 days). Start realistic; tighten with data.
- **Error budget** — 1 − SLO; the release policy when it's exhausted (freeze risky changes, prioritize reliability work).
- **Alerting** on budget burn rate (fast and slow windows), not on raw thresholds.
Feature NFRs (latency, availability) map onto SLIs; new journeys get new SLOs.

## 2. Reviewing NFRs (Specify)

For each NFR: measurable? realistic for the architecture and budget? consistent with other NFRs (e.g. strong consistency vs latency)? does it name the load and environment? Is availability stated per journey, not globally? Findings go to product-lead with a suggested number and the cost of meeting it.

## 3. Capacity

Estimate from the brief/vision: users, requests per second (average and peak), payload sizes, data growth per month, background job volume. Derive: instance counts, connection pools, database size and IOPS, queue depth. Record assumptions as `ASM-nn`. Revisit after the first production month.

## 4. Design review checklist

- **Timeouts** on every network call, shorter than the caller's budget; budgets add up along the path.
- **Retries** only for idempotent operations, bounded, with exponential backoff and jitter; no retry storms (retry at one layer only).
- **Idempotency** keys for effectful operations that can be retried by clients or queues.
- **Backpressure and limits**: bounded queues, connection pools, rate limits, request size limits, pagination.
- **Graceful degradation**: what the user sees when each dependency is down (from the failure-mode table); non-critical features fail open or hide.
- **Data durability**: backups, restore tested, RPO/RTO stated; migrations reversible.
- **Startup/shutdown**: readiness vs liveness; graceful drain on SIGTERM; no work lost on deploy.
- **Hot spots**: N+1 queries, missing indexes, unbounded fan-out, large payloads, synchronous calls to slow dependencies.
- **Observability**: RED metrics per interface, traces across boundaries, structured logs with correlation IDs, SLI instrumentation present.

## 5. Load profiles and resilience experiments

You design, test-engineer executes (or you execute in diagnosis):
- **Load profile** per performance NFR: arrival rate, user mix, data volume, duration, ramp; pass criteria (p95/p99, error rate) and the environment (production-like data volume).
- **Soak** for memory leaks and connection exhaustion on long-running services.
- **Resilience experiments** from the failure-mode table: kill a dependency, add latency, exhaust a pool, fill a disk; expected behavior and recovery time are the pass criteria. Run only in local/staging.

## 6. Performance diagnosis

Measure before changing: reproduce with a load profile; profile (py-spy/scalene for Python, browser devtools/Lighthouse for frontends); inspect queries (`EXPLAIN ANALYZE`); identify the dominant cost; propose the smallest fix; verify with the same profile. Never "optimize" without a before/after measurement.

## 7. Alerts and operability

Every alert: symptom-based (user impact or SLO burn), actionable, owned, linked to a runbook section, with a tested trigger. No alerts on causes that don't affect users (CPU at 80% is a dashboard, not a page). Dashboards per service: SLIs, RED, saturation, dependencies.

## 8. Release review

Review `release.md`: rollout steps with health criteria tied to SLIs, bake times, automatic rollback triggers, migration order (expand → migrate → contract), rehearsed rollback evidence, monitoring for the watch window, error-budget status (exhausted budget → recommend hold).

## 9. After incidents

Contribute reliability actions to postmortems: missing timeouts, alerts that didn't fire, SLOs that didn't reflect user pain, capacity misses. Each becomes a `DEBT-nn`, a task, or an NFR/SLO change.
