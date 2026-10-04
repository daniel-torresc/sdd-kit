---
name: stack-github-actions
description: GitHub Actions expertise for SDD — workflow structure, SHA-pinned actions, least-privilege permissions, caching, service containers for databases, artifacts, environments with protection rules, OIDC to clouds, reusable workflows, concurrency, and common security pitfalls. Use when writing or reviewing .github/workflows.
---

# Stack: GitHub Actions

> Verify action versions and inputs in current docs (context7) before use.

## Rules

- **Pin every third-party action by full commit SHA**, with the version as a comment: `uses: actions/checkout@<sha> # v4.x.y`. Renovate keeps them updated.
- **Least privilege**: top-level `permissions: {}` (or `contents: read`), then grant per job only what it needs (`id-token: write` for OIDC, `pull-requests: write` only where required).
- **Triggers**: `pull_request` and `push` on `main` and `sdd/**`; avoid `pull_request_target` unless you fully understand it (it runs with secrets on untrusted code).
- **Never interpolate untrusted input** (`${{ github.event.pull_request.title }}`, branch names) directly into `run:` — pass through `env:` and quote.
- **Concurrency**: `concurrency: { group: ${{ github.workflow }}-${{ github.ref }}, cancel-in-progress: true }` for CI; never cancel deploys mid-flight.
- **Caching**: `astral-sh/setup-uv` with cache enabled (keyed on `uv.lock`), `actions/setup-node` with lockfile cache, Docker layer cache via buildx.
- **Databases**: use `services:` with a pinned image and health check for integration tests.
- **Artifacts**: upload JUnit, coverage XML, SBOM, scan reports with a retention period.
- **Environments**: `environment: production` with required reviewers and deployment-branch restriction (`main`); secrets scoped to environments.
- **Cloud auth**: OIDC federation (`id-token: write`) instead of stored long-lived keys.
- **Reusable workflows** (`workflow_call`) for build/test/scan shared by CI and deploy.
- **Timeouts**: `timeout-minutes` on every job.

## Lint

`actionlint` on every change (catches expression errors, unknown inputs, shell issues via shellcheck).
