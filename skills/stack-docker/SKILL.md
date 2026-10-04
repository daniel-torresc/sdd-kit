---
name: stack-docker
description: Container expertise for SDD — production Dockerfiles (official base images pinned by digest, multi-stage builds, non-root, minimal runtime, health checks, no secrets in layers), Python/uv and Node patterns, .dockerignore, compose for local dependencies, image scanning (trivy) and SBOMs (syft), and hadolint. Use when writing or reviewing Dockerfiles or compose files.
---

# Stack: Docker

> Verify base image tags/digests and tool flags in current docs before use.

## Dockerfile rules

- Official or verified base images, **pinned by digest** (`python:3.x-slim@sha256:…`); update via Renovate.
- **Multi-stage**: a builder stage installs dependencies and builds; the runtime stage copies only what runs.
- **Non-root** runtime user with a fixed UID; read-only filesystem where possible.
- **No secrets** in build args, layers or the image; use BuildKit secret mounts for build-time credentials.
- `HEALTHCHECK` (or platform health probes) hitting the readiness endpoint.
- Explicit `WORKDIR`, `EXPOSE`, exec-form `CMD`/`ENTRYPOINT`; handle SIGTERM for graceful shutdown.
- Order layers for cache hits: lockfile + dependency install before copying source.
- `.dockerignore` excludes `.git`, `.venv`, `node_modules`, tests artifacts, `.claude/`, local env files.

## Python with uv (pattern)

Builder: copy `pyproject.toml` + `uv.lock`, `uv sync --frozen --no-dev --no-install-project`, then copy source and `uv sync --frozen --no-dev`. Runtime: copy the `.venv` and source, put `.venv/bin` on `PATH`, run the ASGI server (e.g. uvicorn/gunicorn) with access logs configured per the conventions (no query strings with personal data).

## Compose (local only)

Local dependencies (PostgreSQL, SMTP capture, etc.) with pinned images, health checks, named volumes, no published ports beyond what's needed. Never used for production.

## Checks

`hadolint` (lint), `trivy image` (critical vulns block unless an accepted RISK), `syft` (SBOM artifact).
