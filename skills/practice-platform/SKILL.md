---
name: practice-platform
description: How the SDD platform-engineer builds the path from code to production — walking-skeleton scaffold, dev containers, CI pipeline design (quality gates, fitness functions, supply-chain checks), containers, infrastructure as code with plan/apply discipline, environments and deploy autonomy, GitHub environment protection for production, secrets wiring, observability wiring (OpenTelemetry, dashboards and alerts as code), dependency update automation, and runbooks. Use for scaffold, infra/CI/observability tasks, environment plans and deploys.
---

# Practice: Platform

## 0. Local tooling

Run every check locally before handoff (actionlint, hadolint, shellcheck, trivy, syft, gitleaks, tofu, pre-commit, Docker). If a tool is not installed and not available in the dev container, **report that check as "not run locally"** in your envelope, with the install command — never claim a check passed that you did not run. CI runs all of them regardless.

## 1. Walking skeleton (scaffold)

The platform half of T-01, for a new project:
1. **Repo layout** per `.sdd/architecture/conventions.md` (e.g. `stack-python` §1): `pyproject.toml` with tool config (ruff, pyright, pytest markers incl. `ac`, coverage, import-linter), `src/<app>/main.py` with `create_app()` and `/health` (liveness) + `/ready` (readiness), `.gitignore` (incl. `.venv/`, `.claude/worktrees/`, coverage files), `.dockerignore`.
2. **Dev container** `.devcontainer/devcontainer.json`: the stack runtime, uv/node as needed, Docker-in-Docker or a compose service for PostgreSQL, the linters and scanners from §3. This is the default sandbox for autonomous sessions.
3. **Compose** for local dependencies (database, SMTP capture, etc.) with pinned image digests.
4. **CI** (§2) green on the skeleton, including a deliberately failing commit to prove the gates bite.
5. **Container image** (`stack-docker`) and a **dev deploy** if a dev environment is approved.
6. **First fitness functions** wired (e.g. import-linter contract).

## 2. CI pipeline

One workflow for pull requests and `sdd/*` pushes; jobs run in parallel where independent, cached aggressively, and finish in minutes.

| Job | Contents | Blocking |
|---|---|---|
| lint | formatter check, linter, `actionlint`, `hadolint`, `shellcheck` | yes |
| types | type checker (strict) | yes |
| test | full suite with a real database service, JUnit + coverage XML artifacts, diff coverage vs the base branch (≥ `engineering.diff_coverage_min`) | yes |
| contract | contract tests (schemathesis) against the built app | yes |
| fitness | every `FF-nn` in `.sdd/architecture/fitness.md` (import rules, migration up/down, budgets) | yes |
| supply-chain | dependency audit (pip-audit / npm audit), secret scan (gitleaks), SBOM (syft), image scan (trivy) | critical vulns and any secret → yes (unless an accepted `RISK-nn` lists the CVE) |
| trace | `sdd.py trace --phase verify --junit` on the feature branch | yes once in Verify |

Rules: actions pinned by **commit SHA** with a version comment; least-privilege `permissions:` per job; no secrets in pull-request jobs from forks; artifacts retained for the evidence pack. A pipeline change is proven by a run that passes **and** a run that fails on purpose.

## 3. Containers

See `stack-docker`. Official base images pinned by digest, multi-stage builds, non-root user, minimal runtime image, health check, no secrets in layers, SBOM and scan on every build.

## 4. Infrastructure as code

See `stack-opentofu`. Layout `infra/modules/*` + `infra/envs/<env>/`; remote state with locking; one environment per state.

**Plan freely, apply carefully:**
- `tofu fmt`, `validate`, `plan` are autonomous; attach the plan summary (add/change/destroy counts) and a **monthly cost estimate** to the task or `env-plan`.
- A plan that **adds** resources or **destroys** anything → D3 (decision package for the human), whatever the environment.
- Changes to **existing** dev/staging resources (no adds, no destroys) → apply through the infra CI workflow (autonomous).
- Production → only through the protected workflow after G3.
- Never apply from a laptop shell; applies run in CI with the reviewed plan.

## 5. Environments and deploy autonomy

| Environment | Deploy | Config change (existing resources) | New resources / spend |
|---|---|---|---|
| dev | autonomous (`gh workflow run deploy.yml -f environment=dev`) | autonomous | D3 |
| staging | autonomous | autonomous | D3 |
| production | **G3**, then the protected workflow; GitHub **environment protection with a required human reviewer** is the hard stop | G3 | D3 |

Configure the `production` GitHub environment with required reviewers (the human) and branch restrictions (main only) as part of the scaffold, so no agent can deploy to production even by mistake.

## 6. Secrets

The app reads secrets from the environment or a secret store via settings; CI injects them from GitHub environment secrets / OIDC federation to the cloud (no long-lived keys). You wire **references**; you never read, print or create secret values. New secrets in production accounts → D3; a new secret exposed to the app → security-engineer (D2).

## 7. Observability wiring

From the design's failure-mode table and NFRs: OpenTelemetry SDK/collector config, RED metrics, trace propagation, structured log shipping; **dashboards and alerts as code** (one alert per user-visible symptom or SLO, each linked to a runbook). Prove each alert fires on a simulated symptom in staging.

## 8. Dependency updates

Renovate (or Dependabot) grouped by ecosystem, weekly, auto-merge only for patch-level dev dependencies with green CI; runtime dependency updates go through normal review (and `.sdd/dependencies.yaml` for new packages).

## 9. Runbooks

`docs/runbooks/<service>.md`: what it is, dashboards, each alert → meaning → first checks → mitigation → rollback, how to deploy and roll back, contacts. Written when the alert or service is added, not after the first incident.
