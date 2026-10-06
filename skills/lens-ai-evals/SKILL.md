---
name: lens-ai-evals
description: AI/LLM evaluation lens for SDD consultants, independent of model or vendor — for features that call language or ML models: turning "good output" into measurable criteria, designing evaluation datasets (typical, edge, adversarial, regression), choosing graders (programmatic, model-graded with rubrics, human), thresholds and regression gates, non-determinism, prompt and model versioning, safety and prompt-injection defenses, cost and latency budgets, fallbacks, data handling, and production quality monitoring. Use when a feature includes model calls or model-driven behavior.
---

# Lens: AI evaluations

Model behavior is probabilistic and changes when prompts, models or inputs change. Ordinary tests can't prove it works. **Evaluations** measure how often it works well enough, and they gate every change.

## 1. Define quality as measurable criteria (Specify)

For each requirement that depends on model output, define criteria with thresholds:

| Criterion | Example measure |
|---|---|
| Task correctness | % of cases graded correct against a reference or rubric |
| Groundedness | % of claims supported by the provided sources (no fabrication) |
| Format compliance | % of outputs valid against the output schema |
| Refusal behavior | Refuses what it must; doesn't refuse what it shouldn't |
| Safety | No harmful, biased or policy-violating outputs on the adversarial set |
| Tone and style | Rubric score, where it matters to users |

Add NFRs for **latency** (per call and per journey), **cost** (per request, per user, per month) and **behavior when the model is unavailable** (fallback, degraded mode, queue, honest error).

## 2. Design the evaluation set

- **Typical** cases from real or realistic inputs, proportional to expected usage.
- **Edge** cases: long, empty, multilingual, ambiguous, malformed.
- **Adversarial** cases: prompt injection, jailbreak attempts, sensitive data requests, misleading sources.
- **Regression** cases: every production failure becomes a case.
- Size each slice so a difference at the threshold is detectable, not noise. Version the dataset with the feature.

## 3. Choose graders

Prefer, in order:
1. **programmatic checks** (schema validity, exact or normalized matches, citations present in sources);
2. **model-graded** with a written rubric and reference answers, calibrated against human judgments on a sample;
3. **human review** for what can't be automated, on a sample, with a clear rubric.

Report per criterion, not one blended score.

## 4. Thresholds, variance and gates

- Thresholds come from the requirements. Run enough samples (and repetitions where outputs vary) to separate real change from noise.
- **Regression gate**: any change to prompts, models, parameters, retrieval or tools runs the evaluation set, and a drop beyond tolerance blocks the change.
- Record the model identifier, parameters, prompt version and dataset version with every result.

## 5. Design for model behavior

- Prompts, model identifiers and parameters are **versioned configuration**, not inline strings.
- Outputs are validated against a schema before use; invalid outputs follow a defined path (retry once, fall back, or fail honestly).
- Timeouts, bounded retries and a fallback (another model, a simpler path, a cached answer, a graceful message).
- **Prompt-injection defenses** whenever untrusted text reaches the model:
  - separate instructions from data;
  - restrict what tools and actions the model can trigger;
  - validate and authorize model-proposed actions like any user input;
  - never give the model secrets or permissions it doesn't need.
- Data handling follows its classification: what may be sent to a model provider, retained, or logged (privacy lens).

## 6. Verify and operate

- Evaluation results per criterion go in the evidence pack, with cost and latency measurements.
- In production: monitor quality signals (user feedback, sampled grading, refusal and error rates), cost against budget, and drift after any provider-side model change. Feed failures back into the regression set.

## Review checklist

- [ ] Every model-dependent REQ has measurable criteria and thresholds
- [ ] Dataset covers typical, edge, adversarial and regression cases, versioned
- [ ] Graders chosen and calibrated; results per criterion
- [ ] Regression gate on prompt/model/parameter changes
- [ ] Versioned prompts and models; schema-validated outputs; fallbacks
- [ ] Injection defenses wherever untrusted text reaches the model
- [ ] Latency and cost budgets measured; production monitoring planned

Severity: unsafe, ungrounded or injection-driven behavior in a critical journey → **critical**; quality below threshold, missing regression gate, or unbounded cost → **major**.
