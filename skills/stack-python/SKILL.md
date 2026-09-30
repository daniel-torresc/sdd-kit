---
name: stack-python
description: Python backend expertise for SDD — project layout for a modular monolith, uv packaging, typing with pyright strict, FastAPI and Pydantic v2 service design, SQLAlchemy 2.x and Alembic persistence and migrations, pytest testing patterns (acceptance-criterion markers, hypothesis, testcontainers, contract tests), error handling, configuration, logging and observability, security and performance pitfalls. Use when designing, implementing, testing or reviewing Python backend code.
---

# Stack: Python backend

> Versions move. Before relying on a specific API, confirm it in current docs (context7) and pin versions in `pyproject.toml` / `uv.lock`.

## 1. Project layout (modular monolith)

```
pyproject.toml            # single source of config: deps, ruff, pyright, pytest, import-linter
uv.lock
src/<app>/
  __init__.py
  main.py                 # app factory: create_app(); wiring only
  config.py               # settings (pydantic-settings), read once at startup
  <module>/               # one package per business module (bounded context)
    api.py                # the module's PUBLIC interface — other modules import only this
    routes.py             # HTTP layer (FastAPI router): parse, validate, call service, map errors
    service.py            # use cases; transaction boundaries live here
    models.py             # SQLAlchemy ORM models (owned by this module)
    schemas.py            # Pydantic request/response models (the contract)
    repository.py         # data access, if queries are non-trivial
    errors.py             # domain exceptions
  shared/                 # small, stable utilities only (clock, ids, logging) — no business logic
migrations/               # Alembic
tests/
  unit/  integration/  contract/  e2e/
```

- `src/` layout; the app is an installable package.
- Other modules import `<module>.api` only — enforce with **import-linter** contracts (fitness function).
- No circular imports; no business logic in `routes.py` or `models.py`.

## 2. Tooling

| Purpose | Tool | Rule |
|---|---|---|
| Env, deps, lock, run | uv | `uv sync`, `uv run`, `uv add`; commit `uv.lock` |
| Lint + format | ruff | `ruff check` + `ruff format`; enable at least E, F, I, B, UP, S (bandit), SIM, RUF |
| Types | pyright (strict) | No `Any` leaks at module boundaries; `# pyright: ignore[...]` needs a reason |
| Tests | pytest | `--strict-markers`; register the `ac` marker |
| Property tests | hypothesis | Parsers, validators, invariants |
| Real dependencies in tests | testcontainers | Real PostgreSQL in integration tests — no SQLite stand-in |
| API contract tests | schemathesis | Against the OpenAPI contract |
| Architecture rules | import-linter | Module boundaries |
| Dependency audit | pip-audit | In CI |

## 3. FastAPI and Pydantic v2

- **App factory** (`create_app()`), no import-time side effects; dependencies via `Depends`.
- **Schemas are the contract**: separate request and response models; never return ORM objects directly; `model_config = ConfigDict(extra="forbid")` on inputs.
- **Validation at the edge**: constrained types (`EmailStr`, `Annotated[str, StringConstraints(...)]`), explicit limits on lengths and list sizes.
- **Errors**: domain exceptions in `errors.py`, mapped centrally to RFC 9457 problem details with stable `type`/`code`; never leak stack traces or SQL.
- **Async discipline**: async endpoints must not call blocking I/O; use async drivers (asyncpg / psycopg async) or run sync work in a threadpool. Pick one model per app.
- **Timeouts** on every outbound call (httpx with explicit `Timeout`); retries only for idempotent calls, with backoff and jitter.
- **Idempotency keys** on effectful POSTs that clients may retry.
- Generate and commit the OpenAPI document; diff it in CI against `contracts/`.

## 4. Persistence: SQLAlchemy 2.x and Alembic

- 2.0-style APIs (`select()`, `Mapped[...]`, `mapped_column`); typed models.
- **Session per request/use case**; the service layer owns the transaction (`async with session.begin():`).
- Invariants as **database constraints** (unique, FK, check); handle `IntegrityError` → domain error.
- Concurrency: `SELECT … FOR UPDATE` or optimistic version columns for read-modify-write; unique constraints for "at most one".
- Avoid N+1: explicit `selectinload`/`joinedload`; review query counts in tests for hot paths.
- **Migrations**: Alembic autogenerate is a draft — review every one. Expand → migrate → contract; each migration backward compatible with the previous release; test upgrade *and* downgrade in CI.
- Timestamps `timestamptz` in UTC; money as integer minor units.

## 5. Configuration, logging, observability

- Settings via pydantic-settings from environment; validate at startup; secrets never in code, logs or error messages.
- Structured JSON logs (structlog or stdlib logging with a JSON formatter), correlation/trace ID on every line, **no PII** (log opaque IDs).
- OpenTelemetry instrumentation for FastAPI, SQLAlchemy, httpx; RED metrics per route.
- Health endpoints: liveness (process up) and readiness (dependencies reachable) are different.

## 6. Testing patterns

- Every acceptance test carries its AC: `@pytest.mark.ac("F003:AC-02.1")`.
- Test pyramid: many unit tests on services and pure logic; integration tests with real PostgreSQL (testcontainers) and the real app via `httpx.AsyncClient`/`ASGITransport`; contract tests with schemathesis; a few e2e.
- Deterministic time and randomness: inject a clock and ID generator; no `sleep` in tests.
- Fixtures build state through public interfaces or factories; each test owns its data (transaction rollback or unique data).
- `pytest --junitxml=report.xml` so `sdd.py trace --junit` can check results.

## 7. Security pitfalls

SQL built by string formatting (use bound parameters) · `pickle`/`yaml.load` on untrusted data (use `yaml.safe_load`) · `subprocess` with `shell=True` · missing authorization checks on object access (check ownership, not just authentication) · timing-unsafe comparisons of secrets (`hmac.compare_digest`) · weak password hashing (use argon2id) · secrets from `random` (use `secrets`) · unbounded request bodies/uploads · SSRF via user-provided URLs · verbose errors in production · dependency confusion (pin and hash via `uv.lock`).

## 8. Performance pitfalls

Blocking calls in async code · N+1 queries · missing indexes on filter/join columns (check `EXPLAIN`) · unbounded queries without pagination · large JSON serialization in hot paths · connection pool too small or per-request engines · doing slow work (email, external APIs) inline instead of enqueuing.
