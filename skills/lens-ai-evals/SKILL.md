---
name: lens-ai-evals
description: AI/LLM evaluation lens for SDD consultants — for features that call language or ML models: defining quality criteria as measurable evals, building golden datasets (typical, edge, adversarial cases), choosing graders (exact/programmatic, model-graded with rubrics, human review), thresholds and regression gates, safety and prompt-injection tests, cost and latency budgets, model/prompt versioning, and production monitoring of quality. Use when a feature includes model calls.
---

# Lens: AI evaluations

## Specify
- Turn "good output" into **measurable criteria** per REQ: correctness, groundedness (claims supported by provided sources), format compliance, refusal behavior, tone — each with a threshold (e.g. ≥ 90% pass on the golden set).
- NFRs for **latency** (p95 per call and per journey), **cost** per request/user/month, and **availability** behavior when the model API fails (fallback, degrade, queue).

## Design
- Prompts, model IDs and parameters are **versioned config**, not inline strings; structured outputs validated against schemas; retries/timeouts/fallback models; caching where safe.
- **Prompt-injection** defenses when untrusted text reaches the model: separate instructions from data, constrain tools/actions, validate outputs before acting, never give the model secrets it doesn't need.
- Logging of prompts/outputs respects data classification (no personal data unless allowed).

## Evals
- `specs/<f>/evals.md`: criteria, dataset composition (typical, edge, adversarial, regression cases from bugs), graders (programmatic first; model-graded with a written rubric and spot-checked by humans), thresholds.
- Dataset in `tests/evals/` (test-engineer executes in CI as a regression gate on prompt/model changes).

## Verify / Operate
Eval results in the evidence pack with per-criterion scores; cost and latency measured; production monitoring of quality signals (user feedback, sampled grading) and drift.

Severity: unsafe or ungrounded outputs in a critical journey, or injection leading to actions → **critical**; below-threshold quality or unbounded cost → **major**.
