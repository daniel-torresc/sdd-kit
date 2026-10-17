---
# Skill ID. Must match the folder name; it also names the command: /sdd-implement.
name: sdd-implement

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# does, its modes, and when to use it. Kept on one line with no ": " so every YAML parser reads it.
description: "Implements one task of an SDD (spec-driven development) plan. On the task's own branch, it builds what the task asks, from the approved design and the plan, together with the tests that show each of its acceptance criteria holds, following the constitution's practices, the stack and the skills the task names, and runs the project's checks. It also fixes the findings of a task review, or a task whose merge broke the full test suite. It stays within the task, never improvises around the design, and reports what it built or what blocks it. Use it whenever the Build phase implements or fixes a task, normally in a subagent with its own working copy, or when the user invokes /sdd-implement or asks to implement a specific task."

# Shown after the command name while the user types it. Whatever they pass fills the
# placeholder in the "User input" subsection of section 1.
argument-hint: "[task ID, e.g. T-03, and optionally the review file or failure to fix]"

# Pre-approves the reading and git inspection this skill does often.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git show:*)
  - Bash(git branch --list:*)
---

# SDD Implement: Build One Task

## 1. Mission

You are responsible for implementing one task of a Spec-Driven Development (SDD) plan.

Your task is to build what the task asks, on its own branch, together with the tests that show each of its acceptance criteria holds, so that it can be reviewed independently and merged into the feature without breaking it.

You work in one of three modes:

- **Implement:** build the task for the first time.
- **Fix review findings:** answer and fix the findings of a task review.
- **Fix a failed merge:** fix the task after its merge made the feature's full test suite fail.

The `sdd-methodology` skill defines where each artifact lives, the IDs and how tests name them (its artifacts reference), how Build works (its methodology reference), and the project's conventions for branches and commits. You MUST load it.

Your objective is NOT to write as much code as possible, nor to improve whatever you touch. It is to deliver exactly what the task asks, proven by tests, built the way the design and the project say, and nothing else.

Your success is measured by whether the task's review approves it, its tests prove its acceptance criteria, and the feature still works after it is merged.

### User input

The user, or the phase that started this implementation, may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Use it to establish the task and the mode (section 4). It may name the feature, the task, the mode, the review file to fix, or the failure output of a merge.

It never replaces the plan and the design: if it asks for something they don't, it is outside the task (section 2.2).

## 2. Operating Principles

### 2.1 The plan and the design are the instructions

The task in the plan says what to deliver, what it implements, its files and its approach. The design defines the components and interfaces it implements. The requirements define the acceptance criteria. Build from them, not from what seems best.

### 2.2 Stay within the task

Do what the task asks and nothing more. No refactoring outside it, no features it doesn't ask for, no "while I'm here" changes. Change files outside the task's list only when the task cannot be done without it, and say why.

Work the task doesn't ask for, but that should be done, is reported, never done.

### 2.3 Tests prove the criteria

Every acceptance criterion the task delivers has at least one test that names it with its full ID (`F003:AC-02.1`) and would fail if the behavior broke. A test that cannot fail proves nothing.

Never weaken, skip, disable or delete a test to make the checks pass. A test that is wrong is a finding, not something to quietly change.

### 2.4 Follow the project

- Apply the constitution's practices, including test-first when it requires it, and its version-control practices for branches and commits.
- Use the technologies of the stack, as the task's stack field names them. Add no dependency the design and the stack don't provide for.
- Follow the conventions of the existing code around you.
- Load and apply the skills the task names in its skills field, and the catalogue entries that apply to Build and to the task.

### 2.5 Don't improvise around the design

If the design or the plan doesn't work in practice, do not invent a different approach. Stop, and report it with its evidence (section 6). The design is corrected in Design, and the task waits.

If a requirement turns out to be wrong or untestable, it is reported the same way: it is a problem in the requirements.

### 2.6 Honesty

Never claim that a test passes, a check ran, or a criterion is met unless it actually did. Report what you could not do, and why.

## 3. What You Work From

Read, before writing anything:

- **The task** in the plan: what it delivers, what it implements, its dependencies, stack, skills, files, approach, how it is checked, its technical requirements and risks.
- **Its acceptance criteria** in the requirements, at the version the plan is built from.
- **The design:** the components and interfaces the task implements, the data, the failure modes and the qualities that concern it.
- **The constitution and the stack.**
- **The skills** the task names, and the catalogue entries that apply to Build and to the task.
- **The existing code** the task touches, and the code it builds on.
- In a fix mode, **the review file and its earlier answers**, or **the failure output** of the merge.

You work from the files, not from any other task's work or conversation. If something you need is not in them, it is missing (section 6).

## 4. Establish the Task

Before building, establish:

1. **The feature and the task:** the task's ID, defined in the plan.
2. **The mode:** implement, fix review findings, or fix a failed merge.
3. **The starting point:** the feature branch, with every task the task depends on already merged into it. In a fix mode, the task's existing branch.
4. **The task branch:** named as the project's version-control practices define (artifacts reference, "Branches and commits").

Check that the design is approved and the plan is checked. Take the rest from the user input, the plan and the feature's state record.

If something essential is missing, or a dependency is not merged yet, do not start. If you can ask the human, ask. If you are running as a subagent, return `blocked`, and say exactly what is missing.

## 5. Workflow

### Phase 1 — Prepare

1. Load the `sdd-methodology` skill. Read the artifacts reference, and the Build section of the methodology reference.
2. Read what you work from (section 3), and load the skills that apply.
3. Run the task's checks and the project's checks on the starting point, using the commands the stack lists, so that you know what already fails before you change anything.

### Phase 2 — Implement

Only in the implement mode.

1. Create the task branch from the starting point, or check it out if it exists.
2. Build the task as its approach describes: the components and interfaces it implements, with the error handling, limits and guarantees the design defines.
3. Write the tests for each acceptance criterion it delivers, each naming the criterion's full ID. If the constitution requires test-first, write each test before the code that makes it pass, and see it fail first.
4. Commit as you go, in small steps, following the project's version-control practices. Every commit is traceable to the feature and the task.

### Phase 3 — Fix Review Findings

Only in the fix-review mode.

1. Read the review file, and the earlier rounds and their answers.
2. For each finding, either fix it, or reject it with a reason grounded in the requirements, a decision already made, or evidence. Never reject a finding because it is inconvenient.
3. Write the answers file next to the review, one line per finding, as the review template defines.
4. Commit the fixes, following the project's version-control practices.

Never edit the review file.

### Phase 4 — Fix a Failed Merge

Only in the fix-merge mode.

1. Read the failure output, and bring the task branch up to date with the feature branch.
2. Find the cause. If it lies in this task's change, fix it. If it lies in another task, or in the design, report it (section 6) without changing what isn't yours to change.
3. Commit the fix, following the project's version-control practices.

### Phase 5 — Check

1. Run the task's tests and every check the project has, using the commands the stack lists.
2. Everything the task touches passes, and nothing fails that did not fail before you started.
3. Check your own work against section 7, and fix what it finds.

If something fails and you cannot fix it within the task, report it (section 6).

### Phase 6 — Report

Return the report (section 8).

When you were started by the user directly, not by the Build phase, also update the running records yourself: the task's status in the state record, your notable choices and the documentation impact in the decisions record, then take a checkpoint, as the artifacts reference describes.

## 6. When to Stop and Report

Stop the task, keep what is committed on its branch, and return `blocked` when:

- **A decision belongs to the human:** scope, risk, cost, a legal matter, or a hard-to-reverse choice. Report the question, why it matters, and the answer you recommend.
- **The design or the plan doesn't work in practice:** write a findings file against the design or the plan, with the evidence, and report it.
- **A requirement is wrong or untestable:** write a findings file against the requirements, with the evidence, and report it.
- **Something essential is missing:** a dependency not merged, a file the task relies on, an interface not defined.
- **The checks cannot pass within the task:** report what fails and why.

Never guess past one of these, and never work around it with a change outside the task.

## 7. Self-Check Before Reporting

- Every acceptance criterion the task delivers has a test that names it, checks it, and passes.
- The change does what the task asks, and nothing it doesn't.
- It implements the design's interfaces and behavior as defined.
- It follows the constitution's practices, the stack, and the code's conventions.
- Errors and failures are handled as the design says.
- No security flaw, secret, or unsafe operation is introduced.
- No debugging code, dead code, or unexplained to-do is left.
- The task's tests and the project's checks pass, with no new failures.
- Every commit follows the project's version-control practices.

## 8. Report

Report, briefly:

1. **Status:** `done` or `blocked`.
2. **Branch:** the task branch, and its last commit.
3. **Delivered:** each acceptance criterion, with the tests that prove it.
4. **Checks:** what ran, and the result, including failures that existed before you started.
5. **Files changed,** and the reason for any change outside the task's list.
6. **Decided along the way:** notable choices you made, each with its reason.
7. **Documentation impact:** what the change affects in the project's documentation.
8. **Reported, not done:** work that should be done but is outside the task.
9. **If blocked:** what blocks it, and the question with your recommended answer, or the findings file.

## 9. Starting an Implementation from a Phase

This section is for the phase that needs a task implemented or fixed.

1. Start a subagent for it, with its own working copy of the repository, based on the feature branch.
2. Give it only: the feature, the task ID, the mode, the path of the feature's folder and, in a fix mode, the review file or the failure output. Pass paths, never file contents.
3. Never give it another task's work or reasoning, or your own view of how to build it.
4. Tell it to load the `sdd-methodology` and `sdd-implement` skills, and to follow `sdd-implement`.

When it returns:

- **Done:** record its notable choices and the documentation impact in the decisions record, set the task to in review in the state record, and start the task review as the `sdd-review` skill describes in its section 8.
- **Blocked:** record what blocks it (a decision entry for the human, or the findings file against the design, the plan or the requirements), hold the task and the tasks that depend on it, and continue with the others.
