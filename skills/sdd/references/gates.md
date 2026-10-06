# Presenting human decisions

The human should be able to decide from **one screen**, with the full package one click away.

## For each pending gate or D3 escalation

Present a gate only when its package is **final** (every review of it has returned and been resolved). Never ask the human to decide on a draft.

1. Read the gate file (and `G2-brief.md` when several G2s are pending — present the brief, not each package).
2. Print a summary of at most one screen:
   - **Decision:** the one-sentence question.
   - **Why now / what's blocked:** one line.
   - **Options:** one line each with the key trade-off (for G1: approve / approve with changes / rethink scope).
   - **Recommendation (non-binding):** one line, from the package.
   - **Needs your attention:** the ATTN-marked assumptions or questions (≤ 5), each with its default.
   - **Full package:** the file path.
3. Ask with **AskUserQuestion**: one question per decision (options from the package; the recommended option first, labelled "(Recommended)"). Add a second question for ATTN assumptions when they need an explicit yes/no. The user can always answer "Other" with free text.
4. If the human answers in free text (e.g. "Q1: yes, Q3: the recommended"), restate the mapping in one line ("Recording: 1A strict, 2A accept RISK-01, 3B '¡Hola'") before recording it. Record only answers the human actually gave in this session; if a question is unanswered, leave the gate `pending`.
5. Record the answer in the gate file — `status` (approved | rejected | changes-requested), `decided-by: human`, `decided-on: <date>`, and the **Decision** section with the chosen option, the human's reasons and any conditions or overturned assumptions — then commit (`chore(sdd): record <gate> decision`).
6. Act on it:
   - **approved** → continue advancing.
   - **changes-requested / overturned assumptions** → route to the preparing agent (`revise`), which reopens the affected artifacts.
   - **G2 decided** → architect writes the ADR (`decided-by: human`).
   - **rejected / rethink** → stop; ask the human how to proceed.

## Gate map

| Gate | Prepared by | When |
|---|---|---|
| G1 intent | product-lead | end of Specify (M, L) |
| G2 foundations | architect (+ challenger fairness review) | a one-way door (init, or mid-design) |
| G3 production | platform-engineer (`release`) | end of Verify, after the release plan and rollback rehearsal: merge to main and deploy |
| Risk acceptance | whoever deferred a critical/major finding | when deferred |
| Deadlock | hub | loop cap exhausted with no neutral arbiter |
| Incident mitigation (fast path) | incident-responder | immediately on triage — present at once, not batched |
| Spend / new resources | platform-engineer (`env-plan`) | a plan that adds or destroys resources |
| Methodology changes (MIP) | librarian | constitution or gate changes proposed in a retro |
| External sync | hub | pending outbox entries (see sync.md) |
