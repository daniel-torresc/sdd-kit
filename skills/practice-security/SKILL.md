---
name: practice-security
description: Deep security practice for the SDD security-engineer — data classification, STRIDE threat modeling per trust boundary, security requirements by verification level (OWASP ASVS L1/L2), authentication/authorization/session design, cryptography defaults, secrets management, dependency and supply-chain vetting (license, CVEs, maintenance, provenance), security review of designs and code, security testing (SAST, dependency audit, secret scanning, DAST baseline, authorization tests), severity rating, and risk-acceptance packages. Use for threat models, security reviews, dependency approvals, security verification, and security exceptions. Builds on practice-security-basics.
---

# Practice: Security

`practice-security-basics` is the floor every engineer applies. This skill is the security-engineer's depth on top of it.

## 1. Verification level

| Feature class / data | Target |
|---|---|
| M without personal or financial data | OWASP ASVS **Level 1** controls for the touched areas |
| L, or any feature handling authentication, personal, financial or health data | ASVS **Level 2** for the touched areas |
| Regulated data (health, payments card data) | Level 2 + the regulation's specific controls → flag for D3 legal review |

Record the target in the threat model.

## 2. Data classification

For every data element the feature stores, processes or transmits: `public`, `internal`, `personal`, `sensitive` (credentials, tokens, financial, health, government IDs). Classification drives encryption, retention, logging (never log `personal`/`sensitive` values), access control and the threat model's assets.

## 3. Threat modeling (Design phase)

Write `specs/<f>/threat-model.md` from the template, **in parallel with the architect's design** (read the draft `design.md` and contracts):
1. **Assets** with classification.
2. **Trust boundaries and entry points** — every external `IF-nn` must appear (users, other services, admin paths, background jobs consuming external data, file uploads, webhooks).
3. **Threats per entry point with STRIDE**: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. Add abuse cases from the requirements' unwanted behaviors (enumeration, brute force, replay, mass assignment, IDOR, SSRF, injection).
4. For each `THR-nn`: likelihood, impact, **mitigation** (a control in the design, a REQ/NFR, or a test), **verified-by** (a test ID, a review check, or a CI tool).
5. **Residual risks** → `RISK-nn` entries; high residual risk → D3 risk acceptance.
Mitigations that need design changes become findings to the architect; ones that need requirements become findings to product-lead.

## 4. Design patterns and defaults

- **Authentication**: prefer a vetted library or provider over hand-rolled flows; password hashing argon2id; MFA-ready design; session tokens server-side or short-lived signed tokens with rotation; logout and password change invalidate sessions.
- **Authorization**: deny by default; object-level checks in the service layer; roles/permissions explicit in the design; admin paths separated and audited.
- **Cryptography**: platform/library primitives only (no custom crypto); TLS everywhere; AES-GCM or libsodium for data at rest when application-level encryption is needed; keys in a KMS/secret store with rotation.
- **Secrets**: secret store or platform secrets, injected at runtime; no secrets in repo, images, logs or CI output; rotation plan for each secret.
- **Input/Output**: schema validation at boundaries; output encoding by context; safe parsers; SSRF allow-lists.
- **Auditability**: security-relevant events (auth success/failure, permission changes, admin actions, data export) logged with actor, action, target, result — no sensitive values.
- **Abuse resistance**: rate limits and quotas on authentication and expensive endpoints; uniform responses where enumeration matters.

## 5. Dependency and supply-chain vetting (D2 approvals)

For each requested runtime dependency, check and record in `.sdd/dependencies.yaml`:

| Check | Pass condition |
|---|---|
| License | Permissive (MIT, Apache-2.0, BSD, ISC, PSF, MPL-2.0 file-level) — copyleft (GPL/AGPL/LGPL) or unknown → D3 |
| Vulnerabilities | No unfixed critical/high in the requested version (OSV, pip-audit, npm audit) |
| Maintenance | Release within ~12 months, responsive issue tracker, >1 active maintainer for anything security-critical |
| Provenance | Published by the expected org; no typosquat; signed releases/provenance where available |
| Necessity | Not trivially replaceable by the standard library or an already-approved package |

Decision: `approved` (with version range), `rejected` (with reason and alternative), or D3 (license/legal).

## 6. Security review (designs and code)

Review against the threat model and ASVS target, not general taste:
- every `THR-nn` mitigation present and verified;
- authorization on every object access; no IDOR; no privilege escalation paths;
- injection sinks, deserialization, SSRF, path traversal, open redirects;
- session/token handling, crypto use, secrets handling;
- logging of security events without sensitive data; error responses not leaking internals;
- new dependencies approved; supply-chain checks present in CI.
Findings use the schema; severity by §8.

## 7. Security testing (Verify)

| Test | Tool | Scope |
|---|---|---|
| SAST | semgrep (rulesets for the stack), ruff `S` / bandit | changed code; CI-wired by platform-engineer |
| Dependency audit | pip-audit / npm audit / osv-scanner | full lockfile |
| Secret scan | gitleaks | full history of the feature branch |
| Authorization tests | your own tests in `tests/security/` (pytest) | every object-level access path in the feature: other user's object, missing auth, wrong role |
| DAST baseline | OWASP ZAP baseline scan (Docker) | local or staging deployment only — never production, never third-party hosts |
| Threat checks | tests named in `verified-by` | each `THR-nn` |

## 8. Severity

| Severity | Examples |
|---|---|
| critical | Remote code execution, auth bypass, mass data exposure, secrets in repo/image |
| major | IDOR on a single object type, stored XSS, missing rate limit on authentication, vulnerable dependency (high) reachable from the feature |
| minor | Missing security header, verbose error in non-sensitive path, weak but non-exploitable configuration |
| nit | Hardening suggestions |

## 9. Risk acceptance (D3)

When a critical/major issue is deferred or a control is consciously omitted, write a decision package `specs/<f>/gates/risk-<RISK-nn>.md` (gate template): the risk, exploit scenario, likelihood/impact, options (fix now / mitigate partially / accept with expiry), recommendation, and an **expiry date** for any acceptance.
