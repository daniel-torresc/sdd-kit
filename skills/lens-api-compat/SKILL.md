---
name: lens-api-compat
description: API compatibility lens for SDD consultants — classifying contract changes as additive or breaking (HTTP/OpenAPI, events/AsyncAPI, schemas, CLIs, SDKs), consumer impact, versioning and deprecation policy, compatibility testing (contract diffs, consumer-driven contracts), and migration guides. Use when a feature changes a public or externally consumed interface.
---

# Lens: API compatibility

## Classify every change
| Change | Classification |
|---|---|
| New optional field in a response; new endpoint; new optional parameter that old clients never send | Additive (usually safe) |
| Removing/renaming fields, endpoints, enum values; changing types or formats; making optional input required; tighter validation of inputs clients already send; changed status/error codes or semantics | **Breaking** |
| Rejecting values that were previously ignored | **Breaking** for clients that send them |

## Policy
- Breaking changes require a **new version** (path/header/media-type per conventions) or a **deprecation window** (announce, `Deprecation`/`Sunset` headers, usage telemetry, migration guide) — decided as D2 with the architect, D3 if external consumers are affected.
- Event schemas: consumers tolerate unknown fields; never repurpose a field.

## Verify
- Automated **contract diff** against the previous released contract (e.g. oasdiff for OpenAPI) in CI; breaking diffs fail unless the version changed.
- Consumer-driven contract tests where consumers are known.
- Migration guide for consumers in the docs when anything breaks.

Severity: undeclared breaking change to an external consumer → **critical**; breaking change without deprecation plan → **major**.
