---
name: practice-security
description: Security principles for everyone who designs, builds, reviews or operates software in SDD, independent of technology — trust boundaries and untrusted input, injection, authentication and sessions, authorization on every object, secrets, cryptography, sensitive data and logging, safe parsing and files, server-side requests, abuse resistance, dependencies and supply chain, and failing securely — plus, in references/, the security-engineer's procedures (data classification and verification levels, threat modeling, dependency vetting, security verification, risk acceptance). Use when writing, reviewing or designing anything that handles input, identity, data or dependencies.
---

# Practice: Security

This file holds the **principles** every engineer, reviewer and platform engineer applies. The **procedures** the security-engineer runs are in `references/` and loaded on demand:

| Reference | Used for |
|---|---|
| [references/threat-modeling.md](references/threat-modeling.md) | Data classification, verification level, STRIDE threat analysis delivered as review findings, design-level security patterns |
| [references/dependency-vetting.md](references/dependency-vetting.md) | Approving or rejecting runtime dependencies |
| [references/verification.md](references/verification.md) | Security review and security testing in Verify; severity |
| [references/risk-acceptance.md](references/risk-acceptance.md) | Packages for consciously accepting security risk |

## Principles

**1. Know your trust boundaries.** Everything that crosses into the process from outside is untrusted: requests, headers, cookies, files, messages, environment, data from other services, even your own database if others can write to it. Validate at the boundary against an explicit schema (type, length, range, format, allowed values) and reject rather than "clean and continue". Bound every size: bodies, uploads, list lengths, page sizes.

**2. Keep data and instructions apart.** Injection happens whenever untrusted data reaches an interpreter as code: query languages, markup, shells, file paths, URLs, templates, and model prompts. Use the parameterized or structured form of every interpreter, encode output for its context, never build commands by concatenation, keep resolved paths inside their intended root, and allow-list redirect targets.

**3. Authenticate with vetted mechanisms.**
- Never invent authentication or cryptography.
- Store passwords only with a modern, slow, salted password-hashing algorithm.
- Tokens come from a cryptographically secure generator, carry enough entropy, are stored hashed, expire, and are single-use where the spec says so.
- Compare secrets in constant time.
- Sessions are invalidated on logout and on credential change.
- Cookies are restricted (secure, not script-readable, same-site), and state-changing requests are protected against cross-site forgery.

**4. Authorize every access to every object.** "Logged in" is not authorization. Check, in the service layer, that this actor may perform this action on this specific object. Deny by default. Missing object-level authorization is the most common serious flaw.

**5. Treat secrets as radioactive.**
- No secrets in code, tests, fixtures, images, logs, error messages or commits.
- They come from a secret store or platform injection at runtime.
- Startup fails if a required secret is missing.
- Each secret has an owner and a rotation path.

**6. Protect sensitive data.** Know the classification of what you handle. Log opaque identifiers, never personal data, credentials, tokens or full payloads. Error responses carry stable codes and generic messages, and details go to logs (still without sensitive data). Apply the retention and deletion rules from the design.

**7. Parse safely.** Never deserialize untrusted data into executable structures or use evaluation functions on it. Validate uploaded files by content, cap their size, store them outside served paths with generated names, and never execute them.

**8. Be careful with server-side requests.** When the system fetches a URL influenced by users (webhooks, previews, imports), allow-list destinations or block private and internal address ranges.

**9. Resist abuse.**
- Rate-limit and add quotas to authentication-adjacent and expensive operations.
- Respond uniformly where differences would reveal whether an account or object exists.
- Make effectful operations idempotent so retries can't be abused.

**10. Trust dependencies only after vetting.** Use only approved runtime dependencies, pinned through lockfiles. Audit them when they change, and treat known-vulnerable versions as defects. The supply chain is attack surface.

**11. Fail securely and leave a trail.** On error, deny rather than allow. Log security-relevant events (authentication outcomes, permission changes, administrative actions, data exports) with actor, action, target and result, without sensitive values.

## Quick check (writing or reviewing code)

- [ ] Every new input validated and bounded at the boundary
- [ ] No untrusted data reaching an interpreter as code
- [ ] Authorization checked per object, deny by default
- [ ] Tokens, passwords and sessions handled per principle 3
- [ ] No secrets or sensitive data in code, logs or errors
- [ ] No unsafe parsing; uploads constrained; server-side requests restricted
- [ ] Dependencies approved and audited
