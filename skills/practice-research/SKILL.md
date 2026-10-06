---
name: practice-research
description: Research practice for the SDD researcher — framing a research question, search strategy, source selection and credibility, current-documentation lookups (context7), triangulation, citing every claim, confidence levels, separating facts from inferences, technology option analyses that feed G2 packages, stack briefs for technologies without a stack skill, and domain/market/regulatory research. Use when answering a routed Q-nn, preparing technology options, or writing a stack brief.
---

# Practice: Research

## 1. Frame

Restate the question in one sentence, name the **decision it informs** and who will make it, and define what "answered" means (e.g. "a comparison of 3–4 viable options against REQ/NFR IDs"). Time-box it; research that doesn't change a decision is waste.

## 2. Search and sources

| Source tier | Examples | Use for |
|---|---|---|
| Primary | Official docs (via context7 or the vendor site), specifications/RFCs, laws and regulator guidance, release notes, pricing pages, source code | Facts, capabilities, limits, versions, prices |
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

`specs/<f>/research/Q-nn-<slug>.md` (or `.sdd/research/` for project-level), from the template: question, decision informed, summary answer (3–5 lines), findings with confidence and sources, options table if applicable, implications for REQ/NFR/design, open questions, sources list.

## 5. Technology option analysis (feeds G2)

Use `practice-tech-selection`: include the baseline, every viable option, evidence per criterion (fit to named REQ/NFR IDs, maturity, ecosystem, operational cost with a sourced monthly estimate, lock-in and reversal cost, license, security record, team/hiring, longevity), and one-line exclusions for non-viable options. Present options symmetrically; your lean, if any, goes in a separate section. The architect builds the G2 package from it.

## 6. Stack brief

When a decided stack has no `stack-*` skill, write `.sdd/briefs/<stack>.md` from the stack-brief template, from current official docs: version researched, idioms and project layout, tooling (formatter, linter, type checker, test runner, package manager), testing patterns, security and performance pitfalls, common mistakes. It must be good enough for an engineer to work from; the librarian may promote it to a skill later.

## 7. Domain, market and regulation

For product-lead: competitor behavior (public sources only), user expectations, domain rules, and regulation. Regulatory findings are **information, not legal advice**: summarize the rule, cite the regulator's text, and flag it for D3 interpretation when it changes scope.
