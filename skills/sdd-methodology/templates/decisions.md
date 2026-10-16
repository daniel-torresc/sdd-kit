---
artifact: decisions
feature: [feature ID]
---

# Decisions: <feature name>

> Records every question, answer, and decision about a feature: what was put to the human and what they decided, the Discover questions and their answers, the notable choices made along the way, and the documentation the feature affects.
> This document is the feature's record of why it is the way it is. Together with the state record, it lets any later session resume the feature from the files alone.
> It is append-only: entries are added, never rewritten. It points to the artifacts by ID and version and never duplicates their content.

---

## 1. Human Decisions

Record every decision put to the human, other than the Discover questions: approvals, re-approvals, one-way-door choices, disputes, scope, risk, cost and legal matters, and anything else that only the human can settle.

Create the entry when the decision is put to the human, with its status `Open`. When the human answers, fill in the answer fields once. Nothing else in the entry changes afterwards.

### H-01: [The decision, in one sentence]

- **Raised in:** [Phase and step, e.g. Define / brief approval]
- **Concerns:** [IDs and versions, e.g. brief.md@2, REQ-03]
- **Blocks:** [What cannot go on until this is decided]
- **Context:** [One paragraph; link to the files that hold the detail]
- **Options:** [For a choice: each option with its pros, cons, fit, and cost of reversing it. For an approval: approve, approve with changes, or rethink]
- **Recommendation (not binding):** [The recommended option and why]
- **Status:** [Open | Decided]
- **Answer:** [The human's words, verbatim]
- **Decided on:** [YYYY-MM-DD]

Repeat for each decision.

---

## 2. Discover Questions

Record the Define phase's questions, in the rounds in which they were asked, with the human's answers verbatim.

Each round only follows up on what earlier answers opened or left unclear. A question that was answered is never asked again.

When the human accepts the recommended answers, record their words as the answer of each question they cover.

### Round 1

#### Q-01: [Question]

- **Why it matters:** [What the answer changes in the brief or the requirements]
- **Recommended:** [The recommended answer and why]
- **Answer:** [The human's words, verbatim]
- **Answered on:** [YYYY-MM-DD]

Repeat for each question, and for each round.

---

## 3. Decided Along the Way

Record the notable choices made without the human, within the approved scope: those someone would later ask "why this?" about.

Small gaps filled with a default are assumptions in the relevant artifact, not entries here.

| Date | Decision | Why | Refs |
|---|---|---|---|
| [YYYY-MM-DD] | [What was decided] | [The reason] | [IDs and versions] |

---

## 4. Documentation Impact

Record the documentation the feature's changes affect, as they are noticed. Document starts from this list.

| Date | Document | What changes | Refs |
|---|---|---|---|
| [YYYY-MM-DD] | [README, a page in docs/, the product or architecture description] | [What must be added, changed, or removed] | [IDs] |

---

## 5. Maintenance Guidelines

This document is append-only.

- Add entries at the end of their section. Never rewrite or delete an earlier entry.
- The only change allowed to an existing entry is filling in its answer fields once, when the human answers.
- To correct an entry, add a new one that names the entry it corrects and why.
- Record the human's answers verbatim. A summary or an interpretation is never recorded as their answer.
- Date every entry, and name the IDs and versions it concerns.

### Source of Truth

- This document is the canonical record of what was asked, answered, and decided about the feature.
- The feature's state record says where the feature stands and points to the open entries here; it never repeats them.
- An approval is recorded here, and mirrored by the `status` of the approved artifact. If the two disagree, this document is correct and the artifact is fixed.
- The artifacts hold the content that was decided. This document records the decision, not the content.
