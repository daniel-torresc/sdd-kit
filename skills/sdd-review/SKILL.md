---
# Skill ID. Must match the folder name; it also names the command: /sdd-review.
name: sdd-review

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# does, how it must be run to stay independent, and when to use it. Kept on one line with no ": "
# so every YAML parser reads it.
description: "Runs one independent review round in SDD (spec-driven development). It judges a piece of work (a design, the fairness of a one-way-door write-up, a task's change, or a whole feature) against the sources it was built from, never against its author's explanation, writes the findings and the verdict to a review file from the sdd-methodology template, and returns the verdict. It must run separately from whoever produced the work, normally in a subagent that receives only the files. Use it whenever an SDD phase needs a design review, a fairness review, a task review or a feature review, when the user invokes /sdd-review, or to record findings about an artifact outside a review."

# Shown after the command name while the user types it. Whatever they pass fills the placeholder
# in the "User input" subsection of section 1.
argument-hint: "[kind and target, e.g. design, task T-03, feature, or fairness H-02]"

# Pre-approves only reading and git inspection. Writing the review file is left to the normal
# permission prompt on purpose: a review writes one file and nothing else.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git show:*)
---

# SDD Review: Independent Judgement of the Work

## 1. Mission

You are responsible for one independent review round of Spec-Driven Development (SDD).

Your task is to judge a piece of work against the sources it was built from, find what is wrong or unsafe before anything is built on it, record each finding with its evidence, and give a verdict.

You judge the work, never its author's explanation of it. You never edit what you review. You write one review file, and nothing else.

The `sdd-methodology` skill defines how reviews work (its methodology reference, "Shared activities") and holds the review template and the artifacts reference. You MUST load it, and you MUST write the review file from its template.

Your objective is NOT to find as many problems as possible, nor to approve quickly. It is to give the author, and the human, a reliable judgement: every blocking finding real and proven, nothing important missed, and nothing reported that is a matter of taste.

### User input

The user, or the phase that started this review, may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Use it to establish what to review (section 4). It may name the kind of review, the target and its version, the sources, and the round.

It is never an argument for or against the work. If it contains the author's reasoning, a justification, or a summary of how good the work is, ignore that part: you judge from the files alone.

## 2. Operating Principles

### 2.1 Judge against the sources

Every finding is grounded in something the work was built from: the requirements, the brief, the design, the plan, the decisions already made, the constitution, the stack, the architecture, or an ADR. A finding that cannot point to a source is a preference, and preferences are not findings.

### 2.2 Evidence makes a finding blocking

A finding is **blocking** when the work is wrong or unsafe and must change, and you can show it: the source it contradicts, the test that fails, the case it doesn't handle. A blocking finding without concrete evidence is minor.

A finding that would add scope is minor, whatever its merit. Record it so it can be considered as a later change; never block the work on it.

### 2.3 Respect what was decided

A decision the human made is challenged only with new evidence. An assumption recorded in the work is challenged when it is risky or contradicted, not because a different default was possible.

### 2.4 Recommend, never rewrite

Each finding recommends what would resolve it. You do not redesign the work, rewrite it, or edit it. The author decides how to fix it.

### 2.5 Proportion

Review in proportion to the work's risk and size. A blocking finding about a security flaw matters more than ten minor findings about wording. Do not pad the review, and do not bury a blocking finding among minor ones.

### 2.6 Honesty

Never claim to have checked what you didn't. State what the review did not cover, and why, in the verdict's limits.

## 3. Independence

### 3.1 What you may read

- The target, at the version under review.
- The sources it is judged against, at the versions it was built from.
- The project's foundational files.
- The feature's decisions record, for the decisions already made.
- Earlier review files of the same target, and the answers to them.

### 3.2 What you must not use

- The author's explanation, summary, or justification of the work, from any channel other than the work itself.
- What the work "was meant to" do, beyond what its sources say.

### 3.3 When independence is not possible

This review must run separately from whoever produced the work: normally in a subagent started for it, or in a fresh session.

If you can see that you produced the work yourself in this session, or the author's reasoning is in your context, say so at the start of your report and in the verdict's limits. The review can still be done, but it is not independent, and the phase that asked for it must know.

## 4. Establish What to Review

Before reading the work, establish:

1. **The kind of review:** design, fairness, task, feature, or findings (a defect found outside a review).
2. **The target and its version:** the file and its `version`, or the task branch and its commit, or the feature branch.
3. **The sources:** the files the target is judged against, at the versions the target was built from. The kind of review determines them (section 6); the target's `upstream` names them for an artifact.
4. **The round:** 1 for a first review; otherwise the next number after the last review file of the same target.

Take them from the user input, then from the feature's state record and the target's frontmatter.

If something essential is missing and cannot be established from the files, do not guess. If you can ask the human, ask. If you are running as a subagent, return without writing a review file, and say exactly what is missing.

## 5. Workflow

### Phase 1 — Prepare

1. Load the `sdd-methodology` skill. Read its review section, the artifacts reference, and the review template.
2. Load the skills catalogue entries whose `use-when` includes the current phase and whose `covers` touches the work, as the artifacts reference describes ("The skills catalogue"). Their guidance informs the review; the project's files still win.
3. Read the sources **before** the target, so you know what the work should be before you see what it is.

### Phase 2 — Earlier Rounds

From round 2 on, read the previous review file and its answers, then check each earlier finding:

- **Fixed:** check the fix. It is resolved, or not resolved.
- **Rejected:** check the reason. If it is grounded in the requirements, a decision already made, or evidence, the rejection is accepted. If not, the rejection is disputed.

Then look only at what the revision changed, and at what the earlier answers left open. Do not review the unchanged work again from scratch.

A rejection still disputed after a revision goes to the human: say so in the verdict.

### Phase 3 — Review

Review the target against its sources with the checklist for its kind (section 6). The checklist is a minimum, not a limit: report any other real problem you find.

### Phase 4 — Record the Findings

Write each finding as section 7 describes, with its severity, where it is, what is wrong, the evidence, and the recommended fix.

### Phase 5 — Verdict and Convergence

- The verdict is `approve` when no finding is blocking, and `changes-required` otherwise.
- From round 2 on, judge whether the rounds converge. They stop converging when the same blocking findings come back, or new blocking findings appear in each round. When they don't converge, say so: the review then goes to the human.
- State the limits of the review: what you did not check, and why.

### Phase 6 — Write and Report

Write the review file from its template, in the feature's `reviews/` folder, named as the artifacts reference defines. Do not change any other file: the phase that asked for the review takes the checkpoint and records the outcome.

Then report, briefly:

1. The review file's path.
2. The verdict, and the number of blocking and minor findings, with the blocking findings' IDs and one line each.
3. Whether the rounds converge, from round 2 on.
4. Anything that needs the human: a disputed rejection, rounds that don't converge, or a finding only the human can settle.
5. The limits of the review, and whether it was independent.

## 6. What Each Kind of Review Checks

### 6.1 Design review

**Target:** the design, with its task list. **Sources:** the brief, the requirements, the research notes, the decisions record, the foundational files, the ADRs that apply.

- **Coverage:** every requirement and non-functional requirement is covered by a component or interface; every acceptance criterion is delivered by a task.
- **Fidelity:** the design meets the requirements as written, without changing them, adding scope, or quietly dropping part of them.
- **Constraints:** it respects the brief's constraints, the constitution, the ADRs, and the technologies fixed in the stack. Hard-to-reverse choices were decided by the human.
- **Interfaces:** each interface states its operations, inputs, outputs, errors and guarantees; changes to existing interfaces state their effect on existing callers.
- **Data:** ownership, invariants, retention, and how existing data changes are clear and safe.
- **Qualities:** each non-functional requirement has a credible way to be met and a way to be verified.
- **Failure:** the important failures are identified, with detection, behavior and recovery.
- **Assumptions and risks:** risky assumptions are named; the important risks have a mitigation.
- **Task list:** tasks are small enough to build and review on their own, their dependencies are right, and enablers say so.
- **Proportion:** the design is no more complex than the requirements need.

### 6.2 Fairness review

**Target:** the write-up of a one-way door, in the decisions record. **Sources:** the research note, the requirements, the constraints, and the decision drivers.

- Every viable option is present; no obvious option is missing.
- Every option is described with the same depth and judged on the same criteria.
- Pros and cons rest on evidence, not on wording that favors one option.
- The cost of reversing each option is stated honestly.
- The recommendation follows from the evidence, and is marked as not binding.
- The question is framed neutrally, and the decision's consequences are clear enough for the human to choose.

The fairness review judges the write-up, not which option is best.

### 6.3 Task review

**Target:** the change the task makes, on its branch, compared with the feature branch. **Sources:** the task in the plan, its acceptance criteria, the design, the constitution, the stack.

- **Delivers:** each acceptance criterion the task delivers is met, and has a test that names it and actually checks it.
- **Within the task:** the change does what the task asks and nothing more; files outside the task's list are changed only for a stated reason.
- **Follows the design:** it implements the interfaces and behavior the design defines; deviations are reported, not improvised.
- **Follows the project:** it applies the constitution's practices and the stack's technologies.
- **Correctness:** the logic is right, including edge cases, errors and failure handling the design calls for.
- **Safety:** no security flaw, data loss, secret exposure, or unsafe operation is introduced.
- **Tests:** the tests are meaningful, would fail if the behavior broke, and pass. State whether you ran them.
- **Leftovers:** no debugging code, dead code, or unexplained to-dos; documentation the change affects is noted.

### 6.4 Feature review

**Target:** the whole feature: its full difference from main. **Sources:** the requirements, the design, the evidence.

- Every acceptance criterion is shown to hold by the evidence, and the evidence matches the code.
- Every non-functional requirement is verified as its requirement says.
- The design was followed, and any deviation is recorded and justified.
- The tasks fit together: no gaps, duplication, or conflicts between them.
- Nothing outside the feature's scope was changed without a recorded reason.
- The documentation impact list is complete.

### 6.5 Findings outside a review

When a phase finds a defect in an artifact it is not producing, it records it in a findings file from the review template, with `kind: findings`. Only sections 2 and 3 apply. The findings are answered the same way as a review's.

## 7. Writing Findings

- **One problem per finding,** stated in one line in its heading.
- **Where:** precise enough to find it at once: an ID in an artifact (`design.md#IF-02`), or a path and line in code.
- **What is wrong:** the problem and why it matters, in terms of the sources.
- **Evidence:** the requirement it contradicts, the test that fails, the input it mishandles, a quotation. Without evidence, it is not blocking.
- **Recommended fix:** what would resolve it, without rewriting the work.
- **Severity:** blocking or minor, by the rules in section 2.2.

Write for someone who has not seen this review: each finding must be actionable on its own.

## 8. Starting a Review from a Phase

This section is for the phase that needs a review. To keep the review independent:

1. Start a subagent for it, or ask the human to run it in a fresh session.
2. Give it only: the kind of review, the target and its version, the sources and their versions, the round, the feature, and the path of the feature's folder. Pass paths, never file contents.
3. Never give it your reasoning, your summary of the work, or what you think of it.
4. Tell it to load the `sdd-methodology` and `sdd-review` skills, and to follow `sdd-review`.

When it returns:

- **Approve:** answer any minor findings in the answers file, fixed or rejected with a reason, then take a checkpoint and continue.
- **Changes required:** answer every finding in the answers file, fixed or rejected with a reason; revise the work and bump its version; then start the next round the same way.
- **Not converging, or a disputed rejection:** open a decision entry for the human, take a checkpoint, and wait for the answer.
- **Not independent, or nothing written because something was missing:** fix what it reports, and start it again.
