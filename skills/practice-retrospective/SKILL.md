---
name: practice-retrospective
description: Retrospective and methodology-improvement practice for SDD — gathering facts from state.yaml history, reviews, gates, logs and incidents; process metrics (cycle time per phase, review rounds, findings by severity and lens, escalations, human interruptions, rework from stale artifacts, defects escaping to Verify or production); blameless analysis; turning patterns into lessons and methodology improvement proposals (MIP) for the constitution, config, templates, skills and agents. Use after a feature ships (or is abandoned), after incidents, and periodically across features.
---

# Practice: Retrospectives and methodology improvement

## 1. Gather facts (not opinions)

Sources: `state.yaml` history and loops, every review file (findings, severities, resolutions, rounds), gates and their decisions, `log.md`, change requests and stale events, CI results, the evidence pack, incidents and postmortems.

## 2. Metrics per feature

| Metric | Why |
|---|---|
| Cycle time per phase | Where time goes |
| Review rounds per artifact; loop caps hit | Spec/design quality and review calibration |
| Findings by severity, lens and phase found | Which lenses earn their cost; defects caught early vs late |
| Findings rejected/withdrawn | Reviewer noise |
| Human interruptions (gates, D3) and answer latency | Autonomy health |
| Change requests and stale re-validations | Upstream churn |
| Defects found in Verify / after release | Escapes |
| Fix attempts and unblocks per task | Task sizing and context quality |

## 3. Analyze (blameless)

Ask: what worked and must be kept? Where did we lose time or quality? Which findings arrived later than they could have (and which phase/agent could have caught them)? Which human interruptions were unnecessary — or missing? Look for **patterns across features**, not single anecdotes.

## 4. Outputs

- `specs/<f>/retro.md` from the template: facts and metrics, keep/change, lessons (→ `.sdd/knowledge/lessons.md`), and proposals.
- **Methodology improvement proposals** in `.sdd/improvements.md` as `MIP-nn`: the problem (with evidence links), the proposed change (which file: constitution, config, template, skill, agent, hub), expected effect, how to measure it, and who decides:
  - project config/templates → architect or tech-lead (D2) unless it changes a human gate;
  - constitution and human gates → **D3**;
  - plugin skills/agents themselves → proposals for the plugin maintainer (the human), never edited in place.
- Periodic cross-feature retro (every ~5 features or monthly): trend metrics and the MIP backlog status.
