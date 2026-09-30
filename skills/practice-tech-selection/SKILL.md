---
name: practice-tech-selection
description: How to choose technologies in SDD and present foundational choices to the human — the baseline stack every option must beat, evaluation criteria (fit, maturity, ecosystem, operational cost, lock-in, license, security record, hiring), innovation tokens, frontend rendering-model selection, and how to build a fair G2 options package. Use when choosing a language, framework, datastore, hosting, identity provider, frontend approach or any significant library, and when preparing or reviewing a G2 decision package.
---

# Practice: Technology selection

The human wants **the best technology for each application**, not a house stack. The baseline below is a **comparison point**: every G2 package includes it as Option A, and any other option must beat it on the actual requirements.

## 1. Baseline stack (option A to beat)

> Proposed baseline — the human may adjust it in `.sdd/constitution.md` (Technology baseline). Always verify current stable versions in live documentation (context7) before recommending.

| Layer | Baseline | Why it is the baseline |
|---|---|---|
| Backend language | Python (latest stable CPython supported by the chosen libraries) | Fixed by the human |
| HTTP API framework | FastAPI + Pydantic v2 | Typed contracts, generated OpenAPI, async, large ecosystem |
| Persistence | PostgreSQL + SQLAlchemy 2.x + Alembic | Transactions, constraints, JSON, full-text, queues — covers most needs with one system |
| Background work | PostgreSQL-backed job queue; no broker | One fewer system to run; add a broker only when volume requires |
| Cache | None | Add only when an NFR budget requires it |
| Architecture | Modular monolith, one deployable | Simplest thing that scales far |
| Packaging and tooling | uv, ruff (lint + format), pyright strict, pytest (+ hypothesis) | Fast, standard, strict |
| Observability | Structured JSON logs + OpenTelemetry (traces, metrics) | Vendor-neutral |
| Runtime | OCI container on a managed container platform | Portable; no servers to patch |
| CI | GitHub Actions | Default forge integration |
| Infrastructure as code | OpenTofu/Terraform once any cloud resource exists | Reviewable, reproducible |
| Identity | Managed OIDC provider vs. in-app auth library | **No default — always G2** (security and cost trade-off) |
| Hosting provider | — | **No default — always G2** (cost, region, data residency) |
| Frontend | — | **No default — always analyzed per application** (§4) |

## 2. Evaluation criteria

Score each option against **the feature's actual REQs/NFRs first**, then these criteria. Use evidence (docs, benchmarks, release history), not reputation.

| Criterion | Questions |
|---|---|
| Fit | Which REQs/NFRs does it meet natively, with effort, or not at all? |
| Maturity | Years in production use, release cadence, breaking-change history, 1.0+? |
| Ecosystem | Libraries, integrations, docs quality, community answers? |
| Operational cost | What must we run, patch, back up, monitor? Money per month at expected scale? |
| Lock-in and reversal cost | Proprietary APIs? Data export? Cost to migrate away? |
| License | Permissive (MIT/Apache/BSD) vs copyleft vs source-available — copyleft/unknown is D3 |
| Security record | CVE history, response time, supply-chain posture (signed releases, maintainers) |
| Team and hiring | Skills available to build and maintain it (agents *and* humans who inherit it) |
| Longevity | Backing organization, bus factor, funding |

## 3. Innovation tokens

Each project has **3 innovation tokens**. Choosing a technology that is new to the project's baseline, immature, or niche spends one. Spending a token requires stating what the novelty buys that the baseline cannot. Out of tokens → choose boring.

## 4. Frontend selection

Decide the **rendering model first**, then the framework:

| Situation | Rendering model | Candidate families |
|---|---|---|
| Internal tools, CRUD, forms, low interactivity | Server-rendered HTML with progressive enhancement | Backend templates + HTMX/Alpine |
| Rich, stateful interaction behind login (editors, dashboards) | Single-page app | React or Vue or Svelte + Vite + TypeScript |
| Public, content-heavy, SEO or first-load critical | SSR/SSG meta-framework | Next.js, Nuxt, SvelteKit, Astro |
| Offline, device features | PWA or native/cross-platform | PWA; React Native / Flutter only with a G2 |

Always also consider: accessibility support of the component ecosystem, design-system availability, bundle and performance budget, how the frontend consumes the API contract (generated typed client from OpenAPI), and testing (Playwright for e2e).

## 5. Building a G2 package

Write `gates/G2-<slug>.md` (feature) or `.sdd/gates/G2-<slug>.md` (project) from the gate template.

1. **Decision in one sentence**, and why it is a one-way door.
2. **Options**: the baseline (Option A) + every *viable* alternative (typically 2–4 total). Exclude non-viable ones in a single line each with the reason.
3. **Per option, symmetric depth**: pros, cons, fit against the named REQ/NFR IDs, reversal cost, operational cost (with a monthly estimate at expected scale and its source), innovation tokens spent, license.
4. **Comparison matrix**: criteria × options, with short evidence per cell.
5. **Recommendation — non-binding**, in its own section; option descriptions must read the same with or without it.
6. **What is blocked** until decided, and what proceeds.
7. Send it to the **challenger fairness review** before the hub presents it. After the human decides, write the ADR with `decided-by: human` and the human's reasons.

## 5a. Decision brief — when there is more than one G2

The human must be able to decide from **one page**; the packages are the evidence behind it. Whenever two or more G2 packages are pending together, write `G2-brief.md` next to them:

1. **Questions first** — the few assumptions that flip recommendations (e.g. "does EU residency allow US-owned providers in EU regions?"). Answering these first may remove options.
2. **Decision order** — which decisions constrain which (e.g. hosting → identity → payments), and which can be deferred without blocking anything.
3. **Coherent bundles** — 2–3 complete stacks that fit together (e.g. "Lean: FastAPI + server-rendered/htmx + PostgreSQL shared schema + in-app auth"), each with total monthly cost estimate, innovation tokens spent, reversal risk, and who it suits. The baseline bundle is always one of them. Mixing is allowed; say which combinations do *not* fit.
4. **One line per decision** — options, the non-binding lean, a link to the full package.
5. **How to answer** — e.g. "reply with a bundle name plus any overrides, and answers to the questions".

Keep it to one screen. The challenger reviews it for fairness together with the packages.

## 6. Smaller choices (D1)

A library inside the chosen stack: check fit, maintenance (release in the last 12 months, open-issue health), license, and known vulnerabilities; prefer the standard library or an already-used dependency; log the choice in `log.md`. A new **runtime** dependency is D2 — security-engineer confirms license, CVEs and maintenance.
