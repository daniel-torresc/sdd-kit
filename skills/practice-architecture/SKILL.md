---
name: practice-architecture
description: How to design production systems in SDD — turning NFRs into quality-attribute scenarios and budgets, component and interface design, API design rules (errors, idempotency, pagination, versioning), data modeling, failure-mode analysis, observability by design, the simplest-structure principle, fitness functions, ADR writing, spikes, and a design self-review. Use when writing or reviewing design.md, ADRs, contracts, project architecture docs, or answering feasibility questions.
---

# Practice: Architecture

## 1. Method

1. **Read everything upstream**: requirements (REQ/NFR/AC), ux, the constitution, `.sdd/architecture/*`, existing ADRs, and — for existing code — the actual structure (cite it).
2. **Turn NFRs into quality-attribute scenarios** (§2) and allocate budgets.
3. **Find the one-way doors** first (§8). Anything needing G2 is raised before detailed design.
4. **Sketch the simplest design** that meets every REQ and scenario. Then steelman one real alternative and keep the better.
5. **Detail** components, interfaces, data, failure modes, observability (§3–§6).
6. **Record decisions** as ADRs (§9); write contracts for external/public interfaces (§4).
7. **Define fitness functions** for new structural rules (§7).
8. **Self-review** (§11) and run `sdd.py trace --phase design`.

## 2. Quality-attribute scenarios and budgets

Rewrite each NFR as: **source → stimulus → artifact → environment → response → measure**.

> *100 concurrent customers* (source) *submit reset requests* (stimulus) *to the reset endpoint* (artifact) *under normal operation* (environment); *the service responds* (response) *within 300 ms p95* (measure).

Then **budget** the measure across the path (edge 20 ms, app 60 ms, DB 40 ms, email enqueue 10 ms, margin). The budgets table in `design.md` shows where each NFR is spent and how it is verified. A budget that does not add up is a design defect, not a test problem.

## 3. Components

- One **responsibility** per component, stated in one sentence; it **owns** its data (no other component writes its tables).
- Dependencies point toward stable, abstract modules; no cycles.
- **Start from the simplest structure that meets the requirements**: one deployable with clear module boundaries (each module exposes an explicit public interface; others depend only on it), enforced by fitness functions. Distribution (separately deployed services, message brokers, additional datastores) must be justified in an ADR by a specific NFR or constraint: independent scaling, isolation of a failure domain, a different compliance boundary, or a different release cadence owned by a different team.
- Asynchronous work only where an NFR or failure mode needs it (slow or unreliable dependency, bursty load). Prefer the simplest mechanism the existing infrastructure already provides until volume demands more.

## 4. Interfaces and API design

Every `IF-nn` specifies: operation/signature or schema, auth, inputs with validation, outputs, **errors**, idempotency, rate limits, versioning, and which REQ/NFR it serves.

Rules:
- **Errors** are part of the contract: stable machine-readable codes (e.g. RFC 9457 problem details for HTTP), no internal details leaked.
- **Idempotency** for any operation that creates effects and may be retried (idempotency keys or natural keys).
- **Pagination** for any list that can grow (cursor-based by default).
- **Time** in UTC ISO-8601; money as integer minor units plus currency; IDs opaque.
- **Versioning**: additive changes only within a version; breaking changes need a new version and a deprecation window (D2 with api-compat).
- **Contracts**: external and public interfaces **must** have a machine-readable contract in `specs/<f>/contracts/` (OpenAPI 3.1 for HTTP, AsyncAPI for events, JSON Schema for payloads/files). Internal interfaces may. The contract is the source of truth: engineers implement it, test-engineer tests against it.

## 5. Data

- Entities, relationships, **invariants** (what must always be true), **ownership** (which component writes), **retention** and deletion (privacy), **classification** (public / internal / personal / sensitive).
- Every schema change has a **migration plan**: expand → migrate → contract; backward compatible with the previous release so rollback works.
- Concurrency: identify every read-modify-write; choose constraints, transactions, or optimistic locking explicitly.
- Prefer database constraints (unique, foreign key, check) over application checks for invariants.

## 6. Failure modes and observability

For every external dependency and every stateful operation, fill the table:

| Failure | Detection | Behavior (what the user/system sees) | Recovery |
|---|---|---|---|

Standard defenses: timeouts on every network call, bounded retries with backoff and jitter only for idempotent operations, circuit breaking or fallback for non-critical dependencies, bulkheads for resource isolation, graceful degradation defined per REQ.

**Observability by design**, per interface: structured logs (with correlation ID, no PII), RED metrics (rate, errors, duration), traces propagated across boundaries (vendor-neutral instrumentation), and the alerts that would page someone — each alert tied to a user-visible symptom or an SLO.

## 6a. Testability seams

Acceptance tests drive the system only through public interfaces, so the design must make every AC **observable and controllable from outside**. Specify these seams in `design.md`:
- **Time**: one injected clock is the only source of time for all logic (no `now()` in SQL or scattered `datetime.now()`).
- **Randomness and IDs**: injected generators (tokens, IDs) so tests can be deterministic.
- **Background work**: a way to drain queues on demand in tests (e.g. `worker.run_until_idle()`), so "eventually" becomes testable.
- **Observable state**: every AC outcome visible through an interface (a page, an API response, a captured message) — e.g. a page that shows whether a session is active.
- **External systems**: every outbound dependency behind a port with a contract-faithful fake (SMTP capture, payment stub).
- **Operability**: metrics and structured logs readable in tests, so NFR and "no PII in logs" checks don't reach into internals.

## 7. Fitness functions

Architecture rules that are automated and run in CI, recorded in `.sdd/architecture/fitness.md` as `FF-nn`:
- **Dependency rules** — module A may not depend on module B (enforced by the stack's dependency-rule tooling).
- **Contract conformance** — the implementation matches `contracts/` (contract tests generated from the contract; generated clients compile).
- **Performance budgets** — load test thresholds from the NFR `verify:` lines.
- **Migration safety** — migrations apply and roll back on a copy of the schema.
You define them; platform-engineer wires them into CI.

## 8. One-way doors (→ G2)

A decision is a one-way door when reversing it requires a rewrite, a data migration of production data, a vendor migration, or breaks external consumers. Typical: language/framework for a new codebase, primary datastore, hosting platform, identity provider, public API style, multi-tenancy model, event-sourcing vs. state storage. **Raise G2 before detailed design** using `practice-tech-selection`. Everything else: decide, log (D1), move on.

## 9. ADRs

One decision per ADR, in `docs/adr/ADR-NNNN-<slug>.md` from the template. Context names the forces (REQ/NFR IDs); options are real; consequences include the downsides and follow-up work. `decided-by: human` for G2 outcomes. Never edit an accepted ADR's decision — supersede it with a new ADR.

## 10. Spikes

When feasibility is uncertain and cheap to test, run a spike instead of assuming:
- Folder `.sdd/spikes/SPK-nn-<slug>/` with a `README.md` from the spike template: question, time box, method, result, decision it informs.
- Throwaway: never imported by product code, never copied without review.
- Record the result in the design or ADR that depended on it.

## 11. Design self-review

- [ ] Every REQ/NFR mapped to a component or interface (`trace --phase design` clean)
- [ ] Every NFR has a scenario, a budget that adds up, and a verification method
- [ ] Simplest design that works; one real alternative steelmanned and recorded
- [ ] One-way doors identified; G2 raised or explicitly avoided
- [ ] Every interface: errors, idempotency, auth, validation, versioning; contracts for external/public ones
- [ ] Data: invariants, ownership, retention, classification, migration plan, concurrency
- [ ] Failure-mode table covers every external dependency and stateful operation
- [ ] Observability and alerts specified per interface
- [ ] Testability seams specified: clock, randomness, queue drain, observable outcomes, external fakes, readable metrics/logs
- [ ] New structural rules captured as fitness functions
- [ ] ADR for every D1+ architectural choice; capability claims verified in current docs
- [ ] New runtime dependencies listed for security-engineer's dependency-review
- [ ] `.sdd/architecture/*` updates listed (applied when the feature ships)
