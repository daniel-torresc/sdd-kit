---
name: practice-knowledge
description: How SDD keeps knowledge so it outlives the work — human-facing documentation kept true to what shipped (README, user guides, API reference, developer guides; docs as code; driven by the docs-impact list), the rule that knowledge lives in canonical documents rather than a separate knowledge base, and the learning loop (retrospectives with process metrics, blameless analysis, findings routed to the owners of canonical documents, methodology proposals for the human). Use when updating docs after a feature ships, running retrospectives, or deciding where something learned should be recorded.
---

# Practice: Knowledge

There is **no separate knowledge base**. What the team learns is only useful if it lands where people and agents actually look. This skill covers keeping documentation true (§1), knowing where each kind of knowledge belongs (§2), and the learning loop that routes knowledge there (§3).

## 1. Documentation

### Know the audience

| Doc | Audience | Lives in | Source of truth |
|---|---|---|---|
| README | New developers and evaluators | `README.md` | `stack.yaml` (commands), `architecture.md` (conventions) |
| User guide | End users / API consumers | `docs/guide/` | requirements (behavior), `ux.md` (copy) |
| API reference | Integrators | `docs/api/` | `contracts/` (explained, with examples) |
| Developer guide | Contributors | `docs/dev/` | `architecture.md`, ADRs |
| Runbooks | Operators | `docs/runbooks/` | platform-engineer (not the librarian's) |
| Changelog / release notes | Users | `CHANGELOG.md` | platform-engineer; edited for clarity when asked |

### Docs as code

Markdown in the repository, reviewed like code; examples copied from or checked against tests; every page states what version or behavior it describes; no duplicated facts — link to the source document instead. Plain language with the glossary's terms (`product.md`); task-oriented ("How to reset a password") over feature lists.

### Keep docs in sync (on ship)

During Release (before G3, so the docs merge with the feature), start from the **Docs impact** entries the hub collected in the feature's `decisions.md` from the builders' handoffs, then check the feature's requirements and contracts for anything they missed. Update README commands and configuration, user-guide pages for changed flows, the API reference for changed contracts (including errors and examples), and the developer guide for new conventions.

## 2. Where knowledge belongs

| Kind of knowledge | Canonical home | Owner |
|---|---|---|
| What the product is, for whom, its scope and vocabulary | `.sdd/product.md` | product-lead |
| How the system works; conventions; known debt | `.sdd/architecture.md` | architect |
| Which technologies, their skills and commands | `.sdd/stack.yaml` | architect |
| Why something was decided | ADRs (`docs/adr/`), `decisions.md` | architect / everyone |
| What a feature does and how it was built | its specs: brief, requirements, design, tasks, test plan | their owners |
| What was investigated, and what was found | research notes (`specs/<f>/research/`) | the investigating agent |
| How to operate the system | runbooks | platform-engineer |
| How users and integrators use it | README, `docs/` | librarian |
| How the methodology itself should change | proposals for the human (§3) | the human decides |

Agents read the canonical documents at the start of related work; that is how knowledge changes behavior.

## 3. Learning loop: retrospectives

### Gather facts (not opinions)

Sources: `state.yaml` history and review rounds, every review file and its answers (findings, severities, resolutions, rounds), `decisions.md`, change requests and stale events, pipeline results, the evidence pack, incidents.

### Metrics per feature

| Metric | Why |
|---|---|
| Cycle time per phase | Where time goes |
| Review rounds per artifact; loop caps hit | Spec and design quality; review calibration |
| Findings by severity, lens and phase found | Which lenses earn their cost; defects caught early vs late |
| Findings rejected or withdrawn | Reviewer noise |
| Human interruptions and answer latency | Autonomy health |
| Change requests; stale re-validations | Upstream churn |
| Defects found in Verify or after release | Escapes |
| Fix attempts and unblocks per task | Task sizing and context quality |

### Analyze (blameless)

What worked and must be kept? Where did we lose time or quality? Which findings arrived later than they could have, and which phase or agent could have caught them? Which human interruptions were unnecessary — or missing? Look for **patterns across features**, not single anecdotes.

### Route the outcomes

- **Knowledge about the product, the system, a test gap or an operational gap** → findings to the owner of the canonical document (§2), in `reviews/retro-librarian-r<n>.md`. The owner updates the document.
- **Methodology proposals** — changes to the constitution, the config, templates or the plugin itself → entries for the human in `decisions.md`: the problem (with evidence links), the proposed change and where, the expected effect, and how to measure it. Accepted proposals change the project's constitution or config, or are taken to the plugin maintainer; plugin skills and agents are never edited in place.
- **Cross-feature retros** (every ~5 features or monthly): trends in the metrics, and the status of earlier proposals.
