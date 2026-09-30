---
name: practice-requirements
description: How to write production-grade requirements for SDD — EARS patterns for functional requirements, Given/When/Then acceptance criteria that cover negative and edge cases, measurable NFRs from a quality-attribute checklist, forbidden vague words, and a self-review checklist. Use when writing or reviewing requirements.md, acceptance criteria, NFRs, or any statement of what a system shall do.
---

# Practice: Requirements

A requirement is a **testable statement of externally observable behavior** that a stakeholder needs. It says *what*, never *how*.

## 1. Functional requirements — EARS

Write every REQ in exactly one EARS pattern. The system name is the product or component as users know it (use the glossary term).

| Pattern | Template | Use for |
|---|---|---|
| Ubiquitous | The `<system>` shall `<response>`. | Always-true properties |
| Event-driven | **When** `<trigger>`, the `<system>` shall `<response>`. | Reactions to events or user actions |
| State-driven | **While** `<state>`, the `<system>` shall `<response>`. | Behavior that holds during a mode |
| Unwanted behavior | **If** `<condition>`, **then** the `<system>` shall `<response>`. | Errors, abuse, failures, invalid input |
| Optional feature | **Where** `<feature is enabled>`, the `<system>` shall `<response>`. | Configurable or tiered capabilities |
| Complex | **While** `<state>`, **when** `<trigger>`, the `<system>` shall `<response>`. | Combination (use sparingly) |

Rules:
- **One `shall` per REQ.** Two behaviors → two REQs (atomic).
- **The response is observable** from outside: a UI state, an API response, a stored record visible through an interface, a message sent.
- **Name the actor or trigger precisely.** "When a signed-in customer submits…", not "When the user acts…".
- **No design words:** database, table, cache, queue, microservice, endpoint names, framework names — unless the interface *is* the requirement (a public API contract the customer needs).

## 2. Acceptance criteria — Given/When/Then

Each `AC-nn.m` makes one scenario of `REQ-nn` concrete and becomes at least one automated test.

```markdown
#### AC-02.3: Expired reset link is rejected
- **Given** a password-reset link issued more than 15 minutes ago
- **When** the customer opens it
- **Then** the reset form is not shown
- **And** the customer sees "This link has expired" with an option to request a new one
```

Coverage per REQ — consider each; include every one that applies:
1. **Happy path** — the main success scenario.
2. **Unwanted behavior** — invalid input, missing permission, conflict/duplicate, dependency failure, timeout. **Every REQ needs at least one**, or a one-line reason why none applies.
3. **Boundaries** — zero, one, max, max+1, empty, very long, unicode, time zones, concurrency (two at once).
4. **State** — first use, repeated use, after cancellation, after partial failure.

Rules:
- **Then** is observable and specific (exact message key, status, state) — not "works correctly".
- Use concrete example values (`15 minutes`, `3 attempts`), not placeholders.
- Do not script the UI click-by-click; describe intent-level actions.

## 3. Non-functional requirements

NFRs are where production systems fail. Walk this checklist for every M/L feature and write an NFR — or record "not applicable: <reason>" in `requirements.md` — for each attribute:

| Attribute | Typical measurable form |
|---|---|
| Performance | p95/p99 latency under stated load; throughput; time to first render |
| Capacity / scale | Data volume, concurrent users, growth horizon |
| Availability | Monthly uptime target; planned-maintenance policy |
| Resilience | Behavior when dependency X is down; recovery time (RTO) and data loss (RPO) |
| Security | AuthN/AuthZ rules; rate limits; data classification handling |
| Privacy | Personal data collected, purpose, retention, deletion, consent, residency |
| Accessibility | WCAG 2.2 AA (default for any UI) |
| Localization | Languages, formats (dates, currency), time zones |
| Auditability | Which actions are logged, for how long, who can read them |
| Observability | What operators must be able to see and alert on |
| Compatibility | Browsers/devices; API versioning and backward-compatibility window |
| Maintainability | Only when stakeholder-visible (e.g. "configurable without deploy") |
| Cost | Budget ceilings when they constrain the design |

Every NFR has **a number and a `verify:` line**:

```markdown
### NFR-01: Checkout latency
When a customer submits checkout, the system shall respond within 800 ms at p95 under 50 requests per second.
verify: k6 load test in CI against staging, p95 < 800 ms @ 50 rps for 10 min
```

If you don't know the right number, choose a defensible default, mark it `ASM-nn`, and let G1 confirm it.

## 4. Forbidden words

These words hide a missing requirement. When you write one, replace it with the measurable or observable behavior it stands for:

fast · quick · slow · efficient · scalable · robust · reliable · secure · safe · user-friendly · intuitive · easy · simple · flexible · modern · seamless · appropriate · adequate · reasonable · as needed · if necessary · etc. · and/or · support (as a verb without an object behavior) · handle · manage · process (as a vague verb) · should · may · might · could

## 5. Scope and priority

- Tag each REQ with priority on its own line: `priority: must | should | could`. `won't` items go to *Out of scope*.
- `must` = the release is worthless without it. If more than ~60% are `must`, re-examine.
- Out of scope is explicit and mirrors brief non-goals.

## 6. Self-review checklist (run before returning)

- [ ] `sdd.py trace --phase specify` is clean
- [ ] Every REQ: one EARS pattern, one `shall`, observable response, no design words, glossary terms
- [ ] Every REQ has ≥1 unwanted-behavior AC or a stated reason
- [ ] Boundaries considered for every input
- [ ] NFR checklist walked; each applicable attribute has a number and `verify:`
- [ ] No forbidden words
- [ ] Every unverified number or fact is an `ASM-nn`
- [ ] Every `Q-nn` has a default
- [ ] Every REQ traces to the brief's problem or a success metric; nothing traces to nothing

## 7. Worked example

Bad:
> The system should allow users to reset their password quickly and securely.

Good:
```markdown
### REQ-02: Request password reset
When a customer submits a password-reset request with a registered email, the system shall send a single-use reset link to that email.
priority: must

#### AC-02.1: Link is sent
- **Given** a customer account registered with ana@example.com
- **When** a reset is requested for ana@example.com
- **Then** one email with a reset link is sent to ana@example.com within 60 seconds

#### AC-02.2: Unregistered email reveals nothing
- **Given** no account exists for bob@example.com
- **When** a reset is requested for bob@example.com
- **Then** the same confirmation message as AC-02.1 is shown
- **And** no email is sent

### REQ-03: Reject expired or used links
If a reset link is older than 15 minutes or has already been used, then the system shall refuse the reset and offer to send a new link.
priority: must
```
