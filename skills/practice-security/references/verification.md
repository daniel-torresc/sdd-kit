# Security review and verification (security-engineer)

## Review (designs and code)

Review against the design's Security section (the threats and mitigations) and the verification level, not general taste:
- every required mitigation present and verified;
- authorization on every object access; no privilege-escalation paths;
- injection paths, unsafe parsing, server-side requests, path traversal, open redirects;
- session, token, cryptography and secret handling;
- security events logged without sensitive data; errors not leaking internals;
- new dependencies approved; supply-chain checks present in CI.

## Verification (Verify)

| Check | What | Scope |
|---|---|---|
| Static analysis | Security-focused rules for the stack | Changed code (wired into CI by platform-engineer) |
| Dependency audit | Known vulnerabilities in the full dependency tree | Lockfiles |
| Secret scanning | Credentials in history | The feature branch |
| Authorization tests | Your own tests in `tests/security/`: another user's object, missing authentication, wrong role — for every object-level access path | The feature |
| Dynamic baseline scan | An automated passive/baseline scan of the running application | Local or staging only — never production or hosts we don't own |
| Threat checks | The tests named for each mitigation | Each threat in the Security section |

Results go into `reviews/verify-security-engineer-r<n>.md` and `evidence/security/`.

## Severity

| Severity | Examples |
|---|---|
| critical | Remote code execution, authentication bypass, mass data exposure, secrets in the repository or images |
| major | Object-level access flaw on one object type, stored cross-site scripting, no rate limit on authentication, a high-severity vulnerable dependency reachable from the feature |
| minor | A missing hardening header, a verbose error on a non-sensitive path, weak but non-exploitable configuration |
| nit | Hardening suggestions |

A `major` or `critical` finding needs an exploit scenario.
