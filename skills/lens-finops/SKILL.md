---
name: lens-finops
description: FinOps (cost) lens for SDD consultants — estimating the monthly cost of new cloud resources and third-party services at expected and peak scale, comparing cost to the budget in the constitution/config, cost-aware design choices (right-sizing, serverless vs always-on, storage tiers, egress, caching), tagging for cost allocation, budgets and alerts, and spotting cost risks (unbounded usage, per-request pricing, data egress). Use when a feature adds cloud resources or paid services.
---

# Lens: FinOps

## Design
- **Estimate** monthly cost per new resource/service at expected and peak scale (from `.sdd/operations/capacity.md`), with the pricing source and date; total vs the budget (`ASM` if no budget is stated → flag for the human).
- **Cost drivers**: compute hours, storage and IOPS, data egress, managed-service per-request pricing, third-party API calls (incl. model calls), logs/metrics volume.
- **Cost-aware choices**: right-size; scale to zero for spiky/low traffic; lifecycle policies for storage; cache expensive calls; sample high-volume telemetry.
- **Unbounded cost** risks (per-request pricing exposed to abuse, runaway loops, egress) need limits (quotas, rate limits, budget alerts).

## Plan / Release
Resources tagged (project, environment, feature) for allocation; budget alerts configured by platform-engineer; the cost estimate attached to the D3 decision package for any new spend.

## Operate
Compare actual vs estimate after the first month; deviations > 25% become a finding.

Severity: unbounded cost exposure → **critical**; estimate above budget or missing → **major**.
