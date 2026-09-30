# Contract 2 — Communication

Agents never talk to each other directly. They communicate through artifacts, and the hub routes work. Every agent returns exactly one message: the return envelope.

## A. Return envelope

Your final message to the hub is this YAML block and nothing else. Use exactly these keys — no additions. Paths are relative to the project root and carry `@version`:

```yaml
status: done            # done | needs-input | blocked | failed
artifacts:              # everything you created or changed, with version
  - specs/003-user-signup/design.md@3
  - docs/adr/ADR-0007-session-storage.md@1
summary: |              # ≤10 lines. Detail lives in the artifacts.
  ...
decisions:              # D1 decisions you made (also appended to log.md)
  - "Chose argon2id over bcrypt (ADR-0007)"
assumptions: [ASM-04]   # gaps filled with a documented default
open_questions:         # each with a recommended default
  - "Q-02: Allow social login? default: no (out of scope per brief)"
escalations:            # D2/D3 items needing someone else; always this shape
  - class: D2           # D2 | D3
    route_to: security-engineer   # an agent, or "hub" for D3
    item: "Approve new runtime dependency argon2-cffi (ASM-32)"
    blocks: [T-01]      # what cannot proceed until it is resolved; [] if nothing
next: "review panel: challenger, security-engineer"
```

- `needs-input` — you cannot proceed without a D2/D3 answer; list it under `escalations`, or under `intent_questions` for pre-draft intent questions:
  ```yaml
  intent_questions:        # max 3; only when interpretations differ materially
    - id: Q-01
      question: "Who is the primary user: admins or end customers?"
      why: "Changes the problem, flows and success metric"
      options: ["admins", "end customers", "both"]
      default: "end customers"
  ```
- `blocked` — an upstream artifact is wrong or stale; file a finding routed to its owner.
- `failed` — you could not complete the task; explain why in `summary`.

## B. Reviews

Review file: `specs/<feature>/reviews/<phase>-<agent>-r<n>.md`, started from `templates/review.md`.

```yaml
review:
  target: design.md@3
  reviewer: security-engineer
  round: 1
  verdict: changes-required   # approve | approve-with-comments | changes-required | blocked
findings:
  - id: R1-03
    severity: major           # critical | major | minor | nit | suggestion
    blocking: true
    category: security/authz
    location: "design.md#IF-02"      # or src/app/auth.py:42
    refs: [REQ-04, THR-02]
    claim: "Password reset token has no expiry"
    evidence: "IF-02 defines the token but no TTL; NFR-03 requires…"
    recommendation: "15-min TTL, single use, invalidate on password change"
    confidence: high          # high | medium | low
    route_to: architect       # owner of the fix; "hub" for D3 flags
    escalation:               # optional: D3 when the finding needs a human decision
    resolution:               # filled in by the author
    rationale:
```

### Reviewer rules

1. `critical` and `major` block by default; `minor` and `nit` never block.
2. A `major`/`critical` finding without concrete `evidence` is downgraded to `minor`.
3. Anything that expands scope is a `suggestion`, never blocking, and routes to product-lead.
4. Review the artifact against its upstream artifacts and the constitution — not against your personal preferences.
5. `verdict` follows the findings: any open blocking finding → `changes-required`; the artifact cannot be evaluated (e.g. stale upstream) → `blocked`.
6. In round n>1, re-check previous findings first, then look only for regressions introduced by the revision. Do not raise new non-regression findings after round 1 unless critical.
7. **Findings budget:** no cap on critical and major; at most 10 minor + nit per review, round 1 only. Further polish goes in the review notes, not as findings.
8. **Stay in your lane.** An issue in another reviewer's territory gets one `minor` pointer (`category: pointer/<lens>`, `route_to: <that agent>`), not a full finding.
9. **Settled decisions** (approved gates, accepted ADRs, human decisions) are challenged only with new evidence, as a D3 flag.

### Author rules

1. Answer every finding in the review file: `resolution: fixed | rejected | deferred` plus `rationale`.
2. `rejected` blocking findings go back to the same reviewer next round.
3. `deferred` findings become `RISK-nn`. Deferring a critical/major finding requires a risk-acceptance gate (D3).
4. Bump the artifact `version` after revising.

### Disagreement → arbitration

If a blocking finding is still disputed after the reviewer re-checks it, the hub routes it to an arbiter by category:

| Category | Arbiter |
|---|---|
| Scope, value, user impact | product-lead |
| Architecture, design, NFR trade-off | architect |
| Engineering practice, process, task split | tech-lead |

If the arbiter is a party to the dispute, or the question is a value or risk judgment, it goes to the human (D3).

## C. Change requests

Any agent that finds a defect in an artifact it does not own files a finding in `reviews/cr-<agent>-<n>.md` with `route_to: <owner>` and returns `status: blocked` if it cannot continue. The owner revises and bumps the version; downstream artifacts become stale automatically.
