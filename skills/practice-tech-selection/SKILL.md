---
name: practice-tech-selection
description: How to choose technologies from context in SDD — deriving decision criteria from the requirements, NFRs and constraints of the specific product; identifying the reference option for each decision from context rather than defaults; finding every viable option; evaluating options with evidence (fit, maturity, ecosystem, operational cost, lock-in and reversal cost, license, security record, team capability, longevity); the novelty budget; reasoning about coupled decisions; and presenting a fair G2 package and one-page decision brief for the human to decide. Use when choosing a language, framework, datastore, hosting, identity provider, frontend approach or any significant component, and when preparing or reviewing G2 packages.
---

# Practice: Technology selection

There are **no default technologies** in this methodology. Every choice is derived from the context of the product being built. The only fixed technologies are those the human has stated as constraints (`fixed: true` entries in `.sdd/stack.yaml`).

## 1. Start from the context, not the catalogue

Before naming any technology, write down for the decision:
- **What it must do**: the REQ/NFR IDs it serves, with their numbers (latency, throughput, availability, data volume, consistency, offline, compliance).
- **Constraints**: technologies fixed by the human (`fixed: true` in `.sdd/stack.yaml`), existing systems it must integrate with, data residency, budget, deadlines, licensing policy.
- **Context of the people**: who will build and operate it (the agent team and the humans who inherit it), existing skills, operational capacity.
- **Horizon**: expected scale and how long the decision must hold.
- **Reversibility**: what reversing it would cost (rewrite, data migration, vendor exit).

These become the **decision criteria**, weighted for this product. Generic criteria (§3) refine them; they never replace them.

## 2. The reference option

Each decision gets one **reference option**, derived from context and stated with its reasoning:
1. the technology the project or organization **already runs** for this concern, if any (switching has a cost that must be justified); otherwise
2. the **simplest option that plausibly meets the criteria**: fewest moving parts, most widely understood, least to operate.

The reference option is not a recommendation and is not stored anywhere. Its job is to make every other option justify itself against a concrete, sensible alternative, so the analysis never becomes a contest between fashionable choices.

## 3. Find every viable option

List all options that plausibly meet the criteria: the reference option, the established alternatives, and anything newer that the requirements specifically favor. Exclude non-viable ones explicitly, with one line each giving the reason (e.g. "fails NFR-03: no multi-region writes"). Ask the researcher for an option analysis when the space is unfamiliar or moving fast.

## 4. Evaluate with evidence

| Criterion | Questions |
|---|---|
| Fit | Which criteria from §1 does it meet natively, with effort, or not at all? |
| Maturity | Production track record, release cadence, history of breaking changes |
| Ecosystem | Libraries, integrations, documentation quality, community |
| Operational cost | What must be run, patched, backed up and monitored; money per month at expected and peak scale (with source) |
| Lock-in and reversal cost | Proprietary APIs, data export, cost and time to migrate away |
| License | Permissive vs copyleft vs source-available (copyleft or unknown is a human decision) |
| Security record | Vulnerability history, response time, supply-chain posture |
| Team capability | Can the agents and the humans who inherit it build and operate it well? |
| Longevity | Backing organization, funding, bus factor |

Use primary sources and current versions. Separate facts (cited) from judgments (labeled).

## 5. Novelty budget

Each project can afford only a little novelty. Every option that is new to the project, immature, or niche spends from that budget. Spending it requires stating what the novelty buys that the reference option cannot. If the budget is spent, prefer the established option.

## 6. Coupled decisions

Some decisions constrain each other (frontend rendering ↔ backend framework ↔ identity ↔ hosting). Identify the couplings, the **order** in which decisions should be made, and **coherent bundles**: combinations that fit together, each with total cost, novelty spent and reversal risk. State which combinations do not fit and why.

## 7. G2 package (one-way doors)

Write `gates/G2-<slug>.md` (feature) or `.sdd/gates/G2-<slug>.md` (project) from the gate template:
1. The decision in one sentence, and why it is a one-way door.
2. The decision criteria from §1, with their weights.
3. Options (the reference option plus every viable alternative), each with **symmetric depth**: pros, cons, fit per criterion, reversal cost, operational cost, novelty spent, license.
4. A comparison matrix with short evidence per cell.
5. A **non-binding recommendation** in its own section. The option descriptions must read the same with or without it.
6. What is blocked until the human decides, and what can proceed.

When several G2s are pending together, add `G2-brief.md`, one screen long:
- the questions that would flip recommendations, listed first;
- the decision order;
- 2–3 coherent bundles;
- one line per decision;
- how to answer.

The challenger reviews the packages and the brief for fairness before the human sees them. After the decision, the architect records an ADR with `decided-by: human` and the human's reasons, and updates `.sdd/stack.yaml`: the chosen technology, version, `decided-by: human-at-G2`, the ADR link, and the technology skills agents should load for it (agreed with the human; the researcher may propose candidates).

## 8. Smaller choices (two-way doors)

For a library or tool within an already decided stack: check fit, maintenance, license and known vulnerabilities; prefer what the project already uses; log the choice (D1), and record it in `.sdd/stack.yaml` if it is a technology agents need specific knowledge of (`decided-by: architect`). A new **runtime** dependency also goes through security-engineer's dependency review (D2).
