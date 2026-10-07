# Dependency vetting (security-engineer, D2)

For each runtime dependency listed in the design (or requested during Build), check and record the result in your review:

| Check | Pass condition |
|---|---|
| License | Permissive (MIT, Apache-2.0, BSD, ISC, file-level MPL-2.0, …) — copyleft or unknown → D3 |
| Vulnerabilities | No unfixed critical/high advisories affecting the requested version (public advisory databases) |
| Maintenance | A release within ~12 months, responsive maintainers, more than one active maintainer for security-critical code |
| Provenance | Published by the expected owner; not a typosquat; signed releases or provenance attestations where the ecosystem offers them |
| Necessity | Not trivially replaceable by the standard library or an already approved dependency |
| Footprint | Transitive dependencies reasonable; no install-time scripts doing unexpected things |

Decision per dependency: `approved` (with a version range), `rejected` (with the reason and an alternative), or D3 (license or legal, as a decision entry for the human). code-reviewer checks dependency diffs against your approvals.
