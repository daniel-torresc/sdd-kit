# Presenting human decisions

The human should be able to decide from **one screen**, with the full context one click away. Every decision waiting for the human is an entry under **Waiting for the human** in a `decisions.md` — the active feature's, or `specs/000-foundation/decisions.md` for project-level decisions.

## For each pending entry

Present an entry only when it is **final** (every review of it has returned and been resolved). Never ask the human to decide on a draft.

1. Read the entry (and, for G2, the research note it links to only if the entry is unclear). When several G2 entries are pending, present the architect's overview entry first, then the entries in its decision order.
2. Print a summary of at most one screen:
   - **Decision:** the one-sentence question.
   - **Why now / what's blocked:** one line (`blocks:`).
   - **Options:** one line each with the key trade-off (for G1: approve / approve with changes / rethink scope).
   - **Recommendation (non-binding):** one line, from the entry.
   - **Needs your attention:** the assumptions to confirm (≤ 5), each with its default.
   - **Full context:** the file path and heading.
3. Ask with **AskUserQuestion**: one question per decision (options from the entry; the recommended option first, labelled "(Recommended)"). Add a second question for assumptions when they need an explicit yes/no. The user can always answer "Other" with free text.
4. If the human answers in free text (e.g. "Q1: yes, Q3: the recommended"), restate the mapping in one line ("Recording: G1 approve, H-03 accept RISK-01, G2 option B") before recording it. Record only answers the human actually gave in this session; leave unanswered entries `pending`.
5. Record the answer in the entry — `status` (approved | rejected | changes-requested) and the **Decision** line with the chosen option, the human's reasons, any conditions or overturned assumptions, `decided-by: human` and the date — then commit (`chore(sdd): record <id> decision`).
6. Act on it:
   - **approved** → continue advancing.
   - **changes-requested / overturned assumptions** → route to the preparing agent (`revise`), which reopens the affected artifacts.
   - **G2 decided** → the architect writes the ADR (`decided-by: human`) and updates `stack.yaml`.
   - **methodology accepted** → apply it to the project's constitution or config (hub, with the human's go-ahead), or note it for the plugin maintainer.
   - **rejected / rethink** → stop; ask the human how to proceed.

## Decision map

| Entry | Prepared by | When |
|---|---|---|
| G1 intent | product-lead | end of Specify (M, L) |
| G2 foundations | architect (+ challenger fairness review) | a one-way door (init, adopt, or mid-design) |
| G3 production | platform-engineer (`release`) | end of Verify, after the release plan and rollback rehearsal: merge to main and deploy |
| Risk acceptance | whoever deferred a critical/major finding | when deferred |
| Deadlock | hub | loop cap exhausted with no neutral arbiter |
| Incident mitigation (fast path) | incident-responder | immediately on triage — present at once, not batched |
| Spend / new resources | platform-engineer (`env-plan`) | a plan that adds or destroys resources |
| Methodology change | librarian (retro) | changes to the constitution, config, templates or plugin proposed in a retro |
| External write | hub | see sync.md |
