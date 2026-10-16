---
artifact: review
feature: [feature ID]
kind: [design | fairness | task | feature | findings]
target: [file@version, or task branch@commit]
sources: [file@version, the files the target is judged against]
round: [n]
verdict: [approve | changes-required]
---

# Review: <target>, round <n>

> Records one independent review round: the findings about the target, judged against the sources it was built from, and the verdict.
> The review judges the work, never its author's explanation of it, and never edits what it reviews.
> A review file is never changed once written. The answers to its findings go in a separate answers file, and the next round is a new review file.

---

## 1. Earlier Findings

From round 2 on, first state what happened to each finding of the previous round. Omit this section in round 1, and in a findings file.

| Finding | Answer | Status | Note |
|---|---|---|---|
| [R1-01] | [Fixed / Rejected] | [Resolved / Not resolved / Rejection accepted / Rejection disputed] | [What was checked, or why the rejection is disputed] |

---

## 2. Findings

Record each problem found. In round 2 and later, record only problems the revision introduced or the earlier answers left open.

Each finding states one problem, precisely enough that someone who has not seen the review can act on it. Finding IDs carry the round number; in a findings file, they carry the file's number instead.

### R1-01: [The problem, in one line]

- **Severity:** [Blocking | Minor]
- **Where:** [file#ID, or path:line]
- **What is wrong:** [The problem, and why it matters]
- **Evidence:** [What shows it: the source it contradicts, a test result, a quotation]
- **Recommended fix:** [What would resolve it]

Repeat for each finding.

A blocking finding means the work is wrong or unsafe and must change. A blocking finding without concrete evidence is minor. A finding that would add scope is minor.

---

## 3. Verdict

- **Verdict:** [Approve | Changes required]
- **Blocking findings:** [Number, and their IDs]
- **Minor findings:** [Number]
- **Converging:** [Yes | No: the same blocking findings return, or new ones appear each round]
- **Limits of this review:** [What was not checked, and why, or None]

The verdict is `approve` when no finding is blocking, and `changes-required` otherwise.

### 3.1 What Should Be Kept

Optionally, note what is good in the work and should not be lost in a revision.

---

## 4. Maintenance Guidelines

This file is never changed once written.

- The answers go in `<this file's name>-answers.md`, one line per finding: `R1-03: fixed (design.md@3)` or `R1-03: rejected: <reason>`. A rejection is grounded in the requirements, a decision already made, or evidence.
- After a revision, the next round is a new file with the next round number.
- A disagreement that survives a revision, or rounds that stop converging, go to the human through the feature's decisions record.

### Source of Truth

- This file is the canonical record of what this round found and its verdict.
- The answers file records how each finding was resolved.
- The target and its sources are the artifacts reviewed; this file never repeats their content.
