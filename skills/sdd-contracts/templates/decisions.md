# Decisions: <feature>

> Every decision about this feature, in one place: what agents decided on their own, what is waiting for the human,
> what the human decided, and external writes waiting for approval. Newest last. Big architecture decisions also get an ADR.

## Waiting for the human
<!-- One entry per pending decision. The preparing agent writes it; the hub presents it and records the answer. -->

### G1 | H-nn: <the decision, in one sentence>
type: intent (G1) | foundation (G2) | production (G3) | risk | scope | legal | deadlock | external-write | mitigation | methodology | spend | setup
prepared-by: <agent>
status: pending                     # pending | approved | rejected | changes-requested
blocks: <what cannot proceed until this is decided>

**Context** — one screen at most; link the artifacts (and the research note with the full option analysis for G2).

**Options**
- **A: <name>** — pros · cons · fit · reversal cost
- **B: <name>** — …

**Recommendation (non-binding):** <option and why>

**Assumptions to confirm:** <ASM-nn: default — confirm or overturn>

**Decision** (filled by the hub with the human's answer): <option, reasons, conditions> — decided-by: human, <date>

## Decided by agents
<!-- Autonomous decisions (D1) and peer sign-offs (D2), one line each. -->

| Date | Agent | Class | Decision | Why | Refs |
|---|---|---|---|---|---|

## Docs impact
<!-- Collected by the hub from builders' handoffs; the librarian works from this list after release. -->
