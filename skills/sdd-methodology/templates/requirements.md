---
artifact: requirements
feature: F000
owner: product-lead
status: draft
version: 1
upstream: [brief.md@1]
---

# Requirements: <feature name>

<!--
Conventions (machine-readable, see references/artifacts.md):
- Define items with headings: "### REQ-01: …", "#### AC-01.1: …".
- AC-nn.m belongs to REQ-nn.
- NFRs need a "verify:" line.
- Withdrawn items: append "[withdrawn]" to the heading.
-->

## Functional requirements

### REQ-01: <short title>
<!-- EARS forms:
  Ubiquitous:  The <system> shall <response>.
  Event:       When <trigger>, the <system> shall <response>.
  State:       While <state>, the <system> shall <response>.
  Unwanted:    If <condition>, then the <system> shall <response>.
  Optional:    Where <feature>, the <system> shall <response>. -->
When <trigger>, the <system> shall <response>.
priority: must

#### AC-01.1: <short title>
- **Given** <context>
- **When** <action>
- **Then** <observable outcome>

## Non-functional requirements

### NFR-01: <short title>
The <system> shall <measurable property>.
verify: <how it is verified — test, load test, audit, monitor>

### Quality attributes not applicable
<!-- From the NFR checklist (practice-requirements §3): attribute — reason. -->

## Out of scope
<!-- Mirrors brief non-goals; add anything clarified during specification. -->

## Assumptions

## Open questions
