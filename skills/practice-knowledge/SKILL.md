---
name: practice-knowledge
description: How SDD captures knowledge so it outlives the work — human-facing documentation kept true to what shipped (README, user guides, API reference, developer guides; docs as code), the project knowledge base (lessons, decision index, FAQ), and the learning loop (retrospectives with process metrics, blameless analysis, lessons and methodology improvement proposals). Use when updating docs after a feature ships, recording lessons or decisions, running retrospectives, or proposing changes to the methodology.
---

# Practice: Knowledge

Three things make an engineering organization remember. Each has a different purpose:

| Part | Purpose | Reader | Output |
|---|---|---|---|
| Documentation (§1) | Describe the shipped product so people can use, integrate, operate and contribute | Users, integrators, developers | README, `docs/` |
| Knowledge base (§2) | Keep what the team learned and decided findable, so agents start from precedent | The agents (and the human) | `.sdd/knowledge/` |
| Learning loop (§3) | Improve the methodology itself from evidence | The human and the methodology owners | `retro.md`, lessons, MIPs |

## 1. Documentation

### Know the audience

| Doc | Audience | Lives in | Source of truth |
|---|---|---|---|
| README | New developers and evaluators | `README.md` | conventions, operations commands |
| User guide | End users / API consumers | `docs/guide/` | requirements (behavior), ux.md (copy) |
| API reference | Integrators | `docs/api/` | `contracts/` (generated, then explained) |
| Developer guide | Contributors | `docs/dev/` | conventions, architecture overview, ADRs |
| Runbooks | Operators | `docs/runbooks/` | platform-engineer (not yours) |
| Changelog / release notes | Users | `CHANGELOG.md` | platform-engineer generates; you edit for clarity when asked |

### Docs as code

Markdown in the repo, reviewed like code; examples are tested or copied from tests; every page states what version/behavior it describes; no duplicated facts — link to the source artifact instead. Write in plain language with the glossary's terms; task-oriented ("How to reset a password") over feature lists.

### Keep docs in sync (on ship)

When a feature passes G3, update the docs its behavior touches: README commands/config, user guide pages for changed flows, API reference from the changed contract (including errors and examples), developer guide for new conventions. Diff the feature's requirements and contracts against the docs to find what changed.

## 2. Knowledge base (`.sdd/knowledge/`)

- `lessons.md` — `LES-nn`: what happened, why it matters, what to do differently, links (retro, incident, review). Only lessons that would change future behavior.
- `decisions.md` — an index of ADRs and human gate decisions (one line each, link), so agents find precedent quickly.
- `faq.md` — recurring questions from reviews and escalations, with answers and sources.

Agents read these at the start of related work; keep them short and current.

### External knowledge sync (optional)

If `.sdd/config.yaml` enables `knowledge.external_sync`, prepare a sync bundle (decisions, lessons, feature summaries) in `.sdd/knowledge/outbox/`; the hub pushes it to the configured knowledge base after the human approves (external write).

## 3. Learning loop: retrospectives and improvement

### Gather facts (not opinions)

Sources: `state.yaml` history and loops, every review file (findings, severities, resolutions, rounds), gates and their decisions, `log.md`, change requests and stale events, CI results, the evidence pack, incidents and postmortems.

### Metrics per feature

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

### Analyze (blameless)

Ask: what worked and must be kept? Where did we lose time or quality? Which findings arrived later than they could have (and which phase/agent could have caught them)? Which human interruptions were unnecessary — or missing? Look for **patterns across features**, not single anecdotes.

### Outputs

- `specs/<f>/retro.md` from the template: facts and metrics, keep/change, lessons (→ `.sdd/knowledge/lessons.md`), and proposals.
- **Methodology improvement proposals** in `.sdd/improvements.md` as `MIP-nn`: the problem (with evidence links), the proposed change (which file: constitution, config, template, skill, agent, hub), expected effect, how to measure it, and who decides:
  - project config/templates → architect or tech-lead (D2) unless it changes a human gate;
  - constitution and human gates → **D3**;
  - plugin skills/agents themselves → proposals for the plugin maintainer (the human), never edited in place.
- Periodic cross-feature retro (every ~5 features or monthly): trend metrics and the MIP backlog status.
