---
name: lens-api-compat
description: API compatibility lens for SDD consultants, independent of technology — for any interface others depend on (HTTP/RPC APIs, events and messages, schemas, files, SDKs, CLIs): identifying consumers, classifying changes as additive or breaking (including behavioral changes), designing for evolvability, versioning and deprecation policy, migration paths and guides, and verifying compatibility automatically. Use when a feature changes a public or externally consumed interface, or introduces one.
---

# Lens: API compatibility

An interface is a promise. Consumers built on yesterday's behavior break when it changes, often silently and often in systems we can't see. This lens keeps promises explicit and changes deliberate.

## 1. Know the consumers

List who depends on the interface: internal modules, other services, mobile or desktop clients you can't force-upgrade, partners, the public. The less control you have over consumers, the stricter the rules. Unknown consumers should be assumed to exist.

## 2. Classify every change

| Change | Classification |
|---|---|
| New optional output field, new operation, new optional input that old clients never send | Additive (usually safe) |
| Removing or renaming fields, operations or enum values; changing types or formats | **Breaking** |
| Making optional input required; tightening validation of inputs clients already send | **Breaking** |
| Changing status or error codes, error shapes, default values, ordering, pagination, or semantics | **Breaking** (behavioral) |
| Rejecting values that were previously ignored or accepted | **Breaking** for clients that send them |
| Adding a value to an enum consumers switch on | Potentially breaking: check consumer tolerance |
| Changing performance characteristics beyond documented limits (rate limits, timeouts, size limits) | Potentially breaking |

Behavioral changes are the most often missed. Compare behavior, not just shape.

## 3. Design for evolvability

- Consumers must tolerate unknown fields and unknown enum values. Document this as part of the contract.
- Never repurpose a field. Add a new one.
- Use explicit versions for contracts consumed outside the team.
- Make defaults explicit in the contract, so changing them is visibly a change.
- For events: include a schema version, and keep producers compatible with consumers that are still on older versions.

## 4. Versioning and deprecation

- Breaking changes need either a **new version** that runs alongside the old one, or a **deprecation window**:
  - announce the change with dates;
  - mark deprecated elements in the contract and in responses where the protocol allows;
  - measure remaining usage;
  - publish a migration guide;
  - remove only when usage is gone or the window ends.
- A breaking change to an internal interface is D2 with the architect. If external consumers are affected, it is D3.

## 5. Verify automatically

- Diff each contract against the last **released** version in CI. Breaking differences fail the build unless the version changed or a deprecation is recorded.
- Run consumer-driven contract tests where consumers are known.
- Run behavioral regression tests for documented semantics (ordering, defaults, error codes).
- When anything breaks, write a migration guide for consumers in the docs.

## Review checklist

- [ ] Consumers identified, including uncontrolled ones
- [ ] Every change classified, behavioral changes included
- [ ] Evolvability rules followed (tolerant readers, no repurposing, explicit defaults)
- [ ] Breaking changes versioned or deprecated with a window and a guide
- [ ] Automated contract diff and consumer tests in CI

Severity: an undeclared breaking change to external consumers → **critical**; a breaking change without a version or deprecation plan → **major**.
