---
name: practice-discovery
description: Product discovery techniques for SDD — turning a request (often phrased as a solution) into a well-framed problem, identifying users and jobs, designing success metrics, finding the smallest valuable slice, and deciding which unknowns are intent questions for the human versus documented assumptions. Use when writing a brief, product vision, personas, or when a request is vague, solution-shaped, or oversized.
---

# Practice: Discovery

Discovery answers four questions before anyone specifies behavior: **What problem? For whom? How will we know it's solved? What is the smallest thing worth shipping?**

## 1. Reframe the request as a problem

Requests usually arrive as solutions ("add a cache", "build a dashboard", "integrate Stripe"). Before writing anything:

1. **Restate the request** in one sentence.
2. **Ask "why?" until you reach a user or business outcome** (usually 3–5 levels):
   > add a cache → pages are slow → customers abandon search → fewer orders.
   The problem is "customers abandon search because results take >3 s", not "we need a cache".
3. **Check the requested solution against the problem.** If it solves it, keep it as a constraint (`constraint: use Stripe` in the brief). If other solutions might solve it better, specify the problem and let design choose — and note in the brief that the requested solution is one option.
4. **Write the problem without any solution words.**

## 2. Users and jobs

- Identify **who** experiences the problem. Use `PER-nn` from `.sdd/product.md`; propose a new persona only when none fits.
- Express needs as jobs: **When** `<situation>`, **I want to** `<motivation>`, **so I can** `<outcome>`.
- Look for **other affected parties**: operators, support staff, admins, auditors, downstream systems. They generate NFRs (observability, audit, admin tooling) that are easy to miss.

## 3. Evidence

For every claim in the brief, note its basis: user data, analytics, support tickets, research (`Q-nn` answered by the researcher), or **assumption** (`ASM-nn`). Never present invented numbers as fact.

## 4. Success metrics

- One **primary metric** that moves when the problem is solved (behavioral, not "feature shipped").
- **Baseline → target**, with a time frame. Unknown baseline → `ASM-nn` plus "measure baseline before release".
- One or two **guardrail metrics** that must not degrade (error rate, conversion, support volume, latency).
- Prefer leading indicators observable within weeks.

| Weak | Strong |
|---|---|
| Launch password reset | Share of locked-out customers who regain access without support: 40% → 90% within 30 days |
| Improve search | Search-to-result-click rate: 32% → 45%; guardrail: p95 search latency ≤ 1 s |

## 5. Slice to the smallest valuable increment

- **Story map:** list the user's steps left to right; under each, stack capabilities from essential to nice-to-have. The top row across all steps is the first slice.
- **Slice by** workflow step, user type, data subset, happy path first + essential unwanted behaviors, manual before automated.
- **Never slice by technical layer** ("backend first, UI later") — each slice must deliver observable value.
- Everything not in the first slice goes to **Non-goals** (with "later" if planned).
- If the first slice is still class L-sized, split into multiple features, each with its own brief.

## 6. Impact check

Before finalizing scope, check whether the change affects: existing users' workflows, existing data (migration?), public contracts, billing, legal/compliance, support and operations. Each "yes" becomes a constraint, a REQ/NFR, or a triage signal the hub must know about (report it in your return envelope).

## 7. Intent questions vs assumptions

Classify each unknown:

| It is an **intent question** (ask the human) when… | It is an **assumption** (document and proceed) when… |
|---|---|
| Different answers change *who* the users are | It is a detail within an agreed problem and user |
| Different answers change *what problem* is solved | A sensible industry default exists |
| Different answers change *how success is measured* | It can be changed later at low cost |
| It commits money, legal exposure or reputation | Getting it wrong only affects a later refinement |

Rules (hybrid mode):
- **Before drafting:** ask at most **3** intent questions, and only if the request has materially different interpretations. Each has `why`, `options` and a `default`.
- **Otherwise:** draft immediately; every unknown becomes `ASM-nn` with a default and rationale; all are confirmed at G1.
- Never ask the human something you could find in the constitution, product context, existing specs, the codebase or through research.

## 8. Brief quality checklist

- [ ] Problem statement contains no solution
- [ ] Users named (PER-nn) with jobs
- [ ] Every claim has evidence or is an ASM
- [ ] Primary metric with baseline → target; guardrails named
- [ ] First slice is the smallest valuable increment; everything else is a non-goal
- [ ] Constraints (including requested solutions kept as constraints) listed
- [ ] Impact check done; triage signals reported
- [ ] Every Q has a default
