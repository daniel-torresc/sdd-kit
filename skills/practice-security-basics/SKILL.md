---
name: practice-security-basics
description: Baseline secure-coding rules every SDD engineer and code reviewer applies to all code — input validation, output encoding, authentication and session handling, authorization on every object access, secrets handling, cryptography defaults, safe deserialization and file handling, SSRF and injection prevention, logging without sensitive data, dependency hygiene, and security-relevant error handling. Use when writing or reviewing any code; security-engineer builds deeper threat-specific analysis on top of it.
---

# Practice: Security basics

These rules apply to **all** code, whatever the feature. They are not a substitute for the threat model; they are the floor.

## 1. Input

- Validate **every** input at the boundary (HTTP, CLI, events, files, environment) against an explicit schema: type, length, range, format, allowed values. Reject; don't sanitize-and-continue.
- Bound sizes: request bodies, uploads, list lengths, pagination limits, string lengths.
- Treat everything from outside the process as untrusted, including headers (`X-Forwarded-For` only from trusted proxies), cookies and data from other services.

## 2. Output and injection

- **SQL**: bound parameters / ORM only. Never build SQL with string formatting.
- **HTML**: auto-escaping templates; no `|safe`/`dangerouslySetInnerHTML` on user data; set a Content-Security-Policy.
- **Shell**: no `shell=True`; pass argument lists; never interpolate user input into commands.
- **Paths**: resolve and verify user-influenced paths stay inside the intended directory.
- **Redirects**: allow-list destinations; no open redirects from user input.
- **URLs fetched server-side** (webhooks, previews, imports): allow-list hosts or block private/link-local ranges (SSRF).

## 3. Authentication and sessions

- Passwords: argon2id (or the ADR's choice) with parameters from the design; never log, return or store them in plaintext; compare secrets with constant-time functions (`hmac.compare_digest`).
- Session tokens and reset/verification tokens: generated with a CSPRNG (`secrets`), ≥128 bits of entropy, stored hashed, single-use where the spec says so, with expiry.
- Cookies: `Secure`, `HttpOnly`, `SameSite=Lax` (or `Strict`); CSRF protection on state-changing form posts.
- Rate-limit authentication-adjacent endpoints as the requirements specify; never reveal whether an account exists unless the spec allows it.

## 4. Authorization

- Check authorization on **every** request that reads or changes an object — by ownership or role, not just "is logged in" (broken object-level authorization is the most common API flaw).
- Deny by default; authorization lives in the service layer, not only in the UI.

## 5. Secrets and configuration

- No secrets in code, tests, fixtures, logs, error messages or commits. Read them from the environment/secret store via settings; fail at startup if required secrets are missing.
- Test secrets are obviously fake and scoped to tests.

## 6. Data protection and logging

- Log opaque identifiers, never personal data, credentials, tokens or full request bodies.
- Error responses carry stable codes and generic messages; details go to logs (without sensitive data).
- Apply the data classification and retention rules from the design.

## 7. Deserialization and files

- No `pickle`, `yaml.load` (use `safe_load`), or `eval` on untrusted data.
- Uploaded files: validate type by content, cap size, store outside the web root with generated names, never execute.

## 8. Dependencies

- Only approved runtime dependencies (`.sdd/dependencies.yaml`); pinned via the lockfile.
- Run the audit tool (`pip-audit`, `npm audit`) when dependencies change; known-vulnerable versions are blocking.

## 9. Review quick-check

- [ ] Every new input validated and bounded
- [ ] No injection sinks with untrusted data (SQL, HTML, shell, paths, URLs)
- [ ] Authorization checked per object, deny by default
- [ ] Tokens/passwords handled per §3
- [ ] No secrets or PII in code, logs or errors
- [ ] No unsafe deserialization; uploads constrained
- [ ] Dependencies approved and audited
