---
name: practice-research
description: Research practice for the SDD researcher — framing a research question, search strategy, source selection and credibility, current official documentation, triangulation, citing every claim, confidence levels, separating facts from inferences, technology option analyses that feed G2 entries, technology reference notes for unfamiliar technologies, and domain/market/regulatory research. Use when answering a routed Q-nn, preparing technology options, or writing a technology reference.
---

# Practice: Research

## 1. Frame

Restate the question in one sentence, name the **decision it informs** and who will make it, and define what "answered" means (e.g. "a comparison of 3–4 viable options against REQ/NFR IDs"). Time-box it; research that doesn't change a decision is waste.

## 2. Search and sources

| Source tier | Examples | Use for |
|---|---|---|
| Primary | Current official documentation, specifications/RFCs, laws and regulator guidance, release notes, pricing pages, source code | Facts, capabilities, limits, versions, prices |
| Secondary | Reputable engineering blogs, benchmarks with published methodology, conference talks, academic papers | Experience, trade-offs, performance |
| Tertiary | Forums, Q&A, social posts | Signals of problems — never the only source for a claim |

Prefer the newest authoritative source; record the retrieval date. Check versions — an answer for v2 may be wrong for v3.

## 3. Rigor

- **Cite every factual claim** (link + date). No citation → mark it as inference.
- **Triangulate** important claims across independent sources.
- **Separate** facts, inferences and your recommendation.
- **Confidence** per finding: high (primary sources agree), medium (secondary or partial), low (single/tertiary source).
- Note what you could **not** find — absence of evidence is a finding.
- Look for **disconfirming** evidence for the option you lean towards.

## 4. Output: research note

`specs/<f>/research/Q-nn-<slug>.md` (project-level research lives in the foundation feature, `specs/000-foundation/research/`), from the template: why (question, decision informed), how (approach), findings with confidence, options if a choice is being informed, conclusion, the decision taken (filled once decided), open questions and sources. The same template serves every kind: questions, technology options, technology references, codebase investigations, spikes and domain research.

## 5. Technology option analysis (feeds G2)

Use `practice-tech-selection`: derive the decision criteria from the context, include the reference option (derived from context, with its reasoning) and every viable option, evidence per criterion (fit to named REQ/NFR IDs, maturity, ecosystem, operational cost with a sourced monthly estimate, lock-in and reversal cost, license, security record, team/hiring, longevity), and one-line exclusions for non-viable options. Present options symmetrically; your lean, if any, goes in a separate section. The architect writes the G2 entry from it.

## 6. Technology reference

When a decided technology is unfamiliar to the team and no adequate guidance is available, write a research note (kind `technology-reference`) from current official documentation: version researched, idioms and project layout, tooling (formatting, linting, type checking, testing, packaging), testing patterns, security and performance pitfalls, common mistakes. It must be good enough for an engineer to work from. It is project knowledge, not a reusable skill; the architect links it from the technology's entry in `.sdd/stack.yaml`.

**Candidate skills.** When asked, propose technology-specific skills for a stack entry: what each covers, its source, maintenance, and fit for the decided version, so the human can choose which to install and list.

## 7. Domain, market and regulation

For product-lead: competitor behavior (public sources only), user expectations, domain rules, and regulation. Regulatory findings are **information, not legal advice**: summarize the rule, cite the regulator's text, and flag it for D3 interpretation when it changes scope.
