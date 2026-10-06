---
name: lens-finops
description: FinOps (cost) lens for SDD consultants, independent of provider — making cost a design input: identifying cost drivers, estimating monthly cost at expected and peak scale with sources, unit economics (cost per user, request or transaction), comparing to the budget, cost-aware design choices, unbounded-cost risks and their limits, allocation tagging, budgets and alerts, and comparing actuals to estimates after release. Use when a feature adds cloud resources, paid services, model calls, or anything billed by usage.
---

# Lens: FinOps

Cost is a non-functional requirement: it constrains design the way latency does, and usage-based billing can turn a bug or an attack into a large bill. This lens makes cost **explicit, bounded and owned**.

## 1. Identify cost drivers

For every new resource or service, list what it is billed on:
- compute time or provisioned capacity;
- storage volume and operations;
- network egress and cross-region traffic;
- per-request or per-unit pricing (managed services, third-party APIs, model tokens);
- observability volume (logs, metrics, traces);
- licenses and seats.

## 2. Estimate

- Monthly cost at **expected** and **peak** scale, using the capacity estimates (`.sdd/operations/capacity.md`), with the pricing source and date.
- **Unit economics**: cost per active user, per request or per transaction. Does it fit the product's economics?
- Compare against the budget in the constitution or config. If no budget is stated, record an `ASM` and flag it for the human.
- State the uncertainty: which assumptions dominate the estimate.

## 3. Cost-aware design

- Right-size from measurements, not guesses; scale down or to zero for low or spiky load.
- Choose pricing models that fit the usage shape (provisioned vs on-demand vs commitments, which are D3 spend).
- Cache expensive calls; batch where latency allows.
- Lifecycle and retention policies for storage and logs; sample high-volume telemetry.
- Keep data and compute close to avoid egress.
- Prefer simpler architectures. Every extra managed service is a recurring line item.

## 4. Bound the unbounded

Usage-based costs exposed to users or automation need limits:
- rate limits and quotas per user or tenant;
- caps on retries and fan-out;
- budget alerts at thresholds;
- a kill switch for runaway jobs.

Bounding unbounded cost exposure is a security and reliability concern too (cost-based denial of service).

## 5. Allocation and governance

Tag every resource with project, environment and feature so cost can be attributed. Budgets and alerts are configured by platform-engineer. Any new spend or commitment is a D3 decision with the estimate attached.

## 6. After release

Compare actuals to the estimate after the first billing period. A deviation over 25% becomes a finding, with the cause (wrong assumption, unexpected usage, leak) and a fix or an updated estimate.

## Review checklist

- [ ] Cost drivers listed for every new resource or service
- [ ] Monthly estimate at expected and peak scale, sourced and dated; unit economics
- [ ] Compared to budget (or budget flagged as missing)
- [ ] Unbounded usage capped; budget alerts and kill switch
- [ ] Resources tagged for allocation
- [ ] Actuals vs estimate scheduled for review

Severity: unbounded cost exposure → **critical**; estimate missing or above budget → **major**.
