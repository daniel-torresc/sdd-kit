---
artifact: research
id: Q-[nn]
feature: [feature ID]
status: [in-progress | done | superseded]
version: [version]
asked-in: [Phase and step, e.g. Design / one-way door H-02]
informs: [The decision or artifact it informs, e.g. H-02, brief.md, design.md]
superseded-by: []
---

# Research: <the question>

> Answers one question that needs knowledge from outside the project's files, with the evidence, the confidence, and what is still unknown.
> For a choice, it compares every viable option with the same depth and the same criteria, whichever option the work leans towards.
> Research informs a decision; it never makes one. The work that asked for it cites this note.

---

## 1. Question

- **Question:** [The question, in one sentence]
- **Informs:** [The decision or artifact that depends on the answer]
- **Answered means:** [What the answer must establish to be useful]
- **Criteria:** [For a choice: the criteria every option is judged on, traced to requirements, qualities, and constraints]
- **Constraints:** [What limits the answer: technologies fixed in the stack, budget, regulation, deadlines]

Research IDs share one `Q-nn` series per feature with the Discover questions.

---

## 2. Method

Describe how the question was researched: the sources consulted, the code examined, and anything tried out.

State the limits of the research: what could not be accessed, checked, or tried, and why.

---

## 3. Findings

Record each finding with its evidence and confidence. Cite facts by their source; mark inferences as such.

### Finding 1: [The finding, in one sentence]

- **Evidence:** [What supports it, citing the sources by number, e.g. S1, S3]
- **Kind:** [Fact | Inference]
- **Confidence:** [High | Medium | Low]

Repeat for each finding.

---

## 4. Options

Only when the question is a choice. Compare every viable option on the criteria in section 1, with the same depth for each. Include the option already in use, or doing nothing, when it is viable.

| Option | Fit with the criteria | Evidence | Cost | Cost of reversing it | Risks |
|---|---|---|---|---|---|
| [Option] | [How well it meets each criterion] | [Sources, e.g. S2] | [Effort, money, operation] | [Low / Medium / High, and why] | [Main risks] |

Repeat for each option. Add a subsection per option when the table cannot hold what matters.

---

## 5. Answer

- **Answer:** [The answer, in a few lines]
- **Confidence:** [High | Medium | Low], [why]
- **Recommendation:** [Only when one was asked for: the option recommended and why, marked as not binding. Otherwise: None]

---

## 6. Still Unknown

State what could not be established, why it matters, and how it could be established.

- [Unknown]: [How it could be established]

---

## 7. Sources

List every source cited. Never cite a source that was not read.

| # | Source | Kind | Retrieved |
|---|---|---|---|
| S1 | [Title, and link or location] | [Primary / Secondary / Code / Experiment] | [YYYY-MM-DD] |

---

## 8. Maintenance Guidelines

This note MUST reflect the evidence as it was when it was written.

- Bump `version` on every change once the note is `done`, and say what changed and why.
- When newer evidence makes the note wrong, write a new note that supersedes it, and set this note's `status` to `superseded` and its `superseded-by`.
- Never change a finding or an answer without new evidence.

### Source of Truth

- This note is the canonical record of the evidence and the answer to its question.
- The decision it informs is recorded in the feature's decisions record, or in an ADR; this note never records a decision.
- The artifacts that rely on it cite it by its ID.
