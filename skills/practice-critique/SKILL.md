---
name: practice-critique
description: How to critically review SDD specifications and designs — adversarial techniques (two-engineers test, pre-mortem, inversion, boundary interrogation, assumption stress test, steelman-then-attack, simplest-thing, reversibility), a calibrated severity rubric, finding categories, a findings budget, and a checklist per artifact type (product context, brief, requirements, ux, design, ADR, G2 entries, tasks). Use when reviewing any spec or design artifact, giving a second opinion on a decision, or checking a decision package for bias.
---

# Practice: Critique

A review exists to **change the outcome**: catch what would cause the wrong thing to be built, rework, or harm — and confirm quickly when the work is sound.

## 1. Procedure

1. **Read upstream first** (brief → requirements → ux → design), the constitution, `.sdd/product.md`, `.sdd/architecture.md` and relevant ADRs. You judge the target *against these*, not against your taste.
2. **Read the target twice**: once as its intended reader (can I build/decide from this?), once as an adversary.
3. **Run the mechanical check** (`sdd.py trace` / `stale`) so you never spend a finding on something the script catches.
4. **Apply the techniques** (§2) and the **artifact checklist** (§6).
5. **Write findings** (§3–§5), then the **notes**: pre-mortem, assumption ranking, strengths to keep.
6. **Set the verdict** from the findings.

## 2. Techniques

| Technique | Question | Typical catch |
|---|---|---|
| Two-engineers test | Would two competent engineers build the same thing from this sentence? | Ambiguity, undefined terms, missing values |
| Pre-mortem | It is 6 months later and this failed. What are the 3 most plausible reasons? | Wrong problem, unmet NFR, adoption failure, ops blind spot |
| Inversion / misuse walk | At each step, what does a careless user, a hostile actor, a failing dependency do? | Missing unwanted-behavior cases |
| Boundary interrogation | Zero, one, many, max, max+1, concurrent, reordered, retried, partially failed, time zones? | Edge cases, race conditions |
| Assumption stress test | For each ASM: if false, what breaks, and how expensive is it to discover late? | Load-bearing assumptions that deserve human attention |
| Consistency matrix | Do terms, numbers and rules agree with glossary, constitution, ADRs, upstream, and within the artifact? | Contradictions, drift |
| Traceability to intent | Does every item serve the brief? Is the brief's goal fully achieved by the items? | Gold-plating; under-scoping |
| Steelman, then attack | What is the strongest alternative? Does the chosen option beat it on the REQs/NFRs? | Unconsidered alternatives, weak rationale |
| Simplest-thing test | Could fewer moving parts meet the same REQs and NFRs? | Over-engineering, speculative generality |
| Reversibility check | Which choices are expensive to undo? Are they identified, justified, and gated (G2)? | Hidden one-way doors |

## 3. Severity rubric

| Severity | Definition | Blocks? |
|---|---|---|
| `critical` | We would build the wrong thing, or cause irreversible harm (data loss, legal exposure, security breach, unrecoverable design) | yes |
| `major` | Likely defect, significant rework, or an NFR/REQ that cannot be met as written | yes |
| `minor` | Local fix; would be caught later at low cost | no |
| `nit` | Wording, formatting | no |
| `suggestion` | Anything that expands scope or is a preference; routed to the owner (scope → product-lead) | never |

Calibrate: if you would not bet that fixing it changes the outcome, it is not `major`.

## 4. Writing findings

Every finding has:
- **location** anchored to an ID (`requirements.md#AC-02.4`) or a quoted line;
- **claim** — one sentence;
- **evidence** — the quoted text *and* the conflicting source or the concrete scenario that breaks it;
- **recommendation** — concrete ("add an AC for a second request within 60 s: second link invalidates the first"), never "clarify";
- **route_to** — the artifact owner.

Bad: `claim: "Rate limiting is unclear"`.
Good: `claim: "REQ-08 limits requests per email but not per IP, so one attacker can trigger emails to many addresses"`, `evidence: "REQ-08: 'at most 3 requests per email per hour'; brief goal is to prevent abuse (C-02); no per-source limit anywhere"`, `recommendation: "Add a per-source limit REQ, or record an ASM that edge rate limiting covers it and route to security-engineer"`.

### Special finding types

- **Pointer** — an issue in another lens's territory: one `minor`, `category: pointer/<lens>`, `route_to: <lens agent>`, one-line claim. No deep analysis.
- **D3 flag** — the artifact exposes a human-level issue (intent conflict, legal, scope beyond brief, settled decision invalidated by new evidence): `escalation: D3`, `route_to: hub`.

### Findings budget

- No cap on `critical` and `major`.
- At most **10** `minor` + `nit` per review, **round 1 only**, highest-value first. Anything beyond goes into a single "Further polish" bullet list in the notes, not as findings.

## 5. Notes section (mandatory, even when approving)

```markdown
## Pre-mortem
1. <most plausible failure> — <which finding addresses it, or "accepted risk">
2. …
3. …

## Assumptions ranked by risk
| Rank | ASM | If false | Cost to discover late | Recommend human attention |
|---|---|---|---|---|

## Strengths to keep
- <what is good and must survive revision>

## Further polish (not findings)
- …
```

The assumption ranking is used by the preparing agent to order the G1 assumptions table.

## 6. Checklists per artifact

**Vision / personas / glossary**
- Problem and audience specific enough to say no to things?
- Principles are real trade-offs (each rules something out)?
- Personas grounded in evidence or marked ASM; no persona without a distinct job?
- Glossary terms unambiguous; no synonyms left competing?

**Brief**
- Problem free of solution words; requested solutions kept as constraints?
- Users/personas and jobs named; other affected parties (ops, support, admins) considered?
- Evidence or ASM for every claim; no invented facts?
- Primary metric measurable with baseline → target; guardrails present?
- First slice truly minimal *and* sufficient to achieve the goal?
- Non-goals explicit; constraints complete; impact check done (data, contracts, billing, legal, ops)?

**Requirements**
- Two-engineers test on every REQ and AC.
- Every REQ traces to the brief; every brief goal is covered by REQs.
- Unwanted behaviors: invalid input, permission, conflict, dependency failure, timeout, abuse, concurrency, retries.
- NFR checklist walked; numbers are plausible and mutually consistent (e.g. latency vs. timing-equalization vs. retry windows).
- No contradictions between REQs, ACs, NFRs, constraints; glossary terms used.
- Priorities sane (≤ ~60% must, or justified).
- ASMs: which are load-bearing?

**UX**
- Every flow maps to REQs; no flow invents capability.
- All states: empty, loading, partial, error, success, permission-denied, offline.
- Error copy is actionable; destructive actions are confirmable/undoable.
- Accessibility considered (keyboard, focus, contrast, labels).

**Design**
- Every REQ/NFR mapped to a component; NFR budgets add up.
- Simplest-thing and steelman tests passed; alternatives recorded.
- Failure modes: detection, behavior, recovery for each external dependency.
- Data model: invariants, ownership, migrations, retention.
- Coupling: hidden shared state, chatty interfaces, circular dependencies.
- One-way doors identified; ADRs exist; G2 raised where required.
- Observability and rollback designed, not deferred.
- Claims about libraries/platforms verified against current official documentation.

**ADR**
- Context states the forces; options are real alternatives; consequences include the downsides.

**G2 entries and their research notes (fairness review)**
- All viable options present? Name any credible option missing.
- Pros and cons symmetric in depth and honesty for each option (no strawmen).
- Fit matrix accurate against the actual REQs/NFRs; numbers sourced.
- Reversal and operational costs stated for every option.
- The recommendation is clearly separated and does not leak into option descriptions.
- Verdict wording for G2: `approve` = fair and complete enough for the human to decide.

**G2 overview entry** (when several G2s are pending)
- Fits on one screen; the human could decide from it alone.
- Questions that flip recommendations are listed first; decision order is correct.
- Bundles are genuinely coherent, include the reference option derived from context, and are presented symmetrically (costs, novelty spent, reversal risk for each).
- One-liners match the G2 entries (no lean stated more strongly than in the entry).

**Tasks (class L)**
- Every AC covered; enablers justified; no task too large to review (split > ~1 day).
- Dependencies correct; parallelizable work not serialized; risky work scheduled early.
- Walking skeleton / integration early, not at the end.

**Test plan (class L)**
- Every AC and NFR has a verification at the right level; the riskiest behavior is tested hardest.
- Failure modes, abuse cases and boundaries from the design are covered, not just happy paths.
- Performance, resilience and evaluation sections present where the lenses require them.

## 7. Second opinion

When asked for a second opinion on a disputed finding or a logged D1 decision:
- State the question in one sentence.
- Steelman each side, cite evidence, and give a reasoned view with confidence.
- You do not decide — the arbiter or human does. Write it to `reviews/second-opinion-challenger-<n>.md`.
