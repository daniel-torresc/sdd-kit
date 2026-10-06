# Threat modeling (security-engineer)

## Verification level

| Feature class / data | Target |
|---|---|
| M without personal or financial data | OWASP ASVS Level 1 controls for the touched areas |
| L, or any feature handling authentication, personal, financial or health data | ASVS Level 2 for the touched areas |
| Regulated data (health, card data, …) | Level 2 + the regulation's controls → flag for D3 legal review |

Record the target in the threat model.

## Data classification

For every data element stored, processed or transmitted: `public`, `internal`, `personal`, `sensitive` (credentials, tokens, financial, health, government IDs). Classification drives encryption, retention, logging, access control and the assets of the model. Personal data also triggers the privacy lens.

## Building the model

Write `specs/<f>/threat-model.md` from the template, in parallel with the architect's design (read the draft design and contracts):
1. **Assets** with classification.
2. **Trust boundaries and entry points** — every external `IF-nn` appears: users, other services, admin paths, jobs consuming external data, file uploads, webhooks, model inputs.
3. **Threats per entry point with STRIDE** (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege), plus abuse cases from the requirements' unwanted behaviors (enumeration, brute force, replay, mass assignment, object-level access, server-side requests, injection).
4. For each `THR-nn`: likelihood, impact, **mitigation** (a design control, a REQ/NFR, or a test) and **verified-by** (test ID, review check, or automated tool).
5. **Residual risks** → `RISK-nn`; high residual risk → risk acceptance (D3).

Mitigations needing design changes become findings to the architect; ones needing requirements, to product-lead.

## Design-level patterns

- Authentication: vetted libraries or providers; modern password hashing; second-factor-ready; short-lived, rotating session credentials; invalidation on logout and credential change.
- Authorization: deny by default; object-level checks in the service layer; explicit roles and permissions in the design; separated, audited admin paths.
- Cryptography: platform primitives only; encryption in transit everywhere; application-level encryption at rest only where the classification needs it; keys in a managed store with rotation.
- Secrets: managed store or platform injection; rotation plan per secret; least privilege for each consumer.
- Auditability: security events logged with actor, action, target, result.
- Abuse resistance: rate limits and quotas on authentication and expensive operations; uniform responses where enumeration matters.
