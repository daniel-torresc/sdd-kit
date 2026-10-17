---
# Skill ID. Must match the folder name; it also names the command: /sdd-build.
name: sdd-build

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# produces and when to use it. It names no file path on purpose: where each artifact lives is
# defined by the sdd-methodology skill and may change. Kept on one line with no ": " so every
# YAML parser reads it.
description: "Runs the Build phase of SDD (spec-driven development) for one feature whose design is approved and whose plan is checked. Task by task, in dependency order and in parallel where the plan allows, it has each task implemented in its own subagent and branch (sdd-implement), reviewed independently (sdd-review), and merged into the feature branch with the full test suite passing, undoing any merge that breaks it. A blocked task holds only itself and the tasks that depend on it, and the rest of the build goes on. Works for a feature ready for Build, for resuming a build in progress, and for building the fix tasks added after Verify. Use when the user invokes /sdd-build, or asks to build or continue building a feature from its plan. Not for designing the feature or verifying it as a whole."

# Shown after the command name while the user types it. Whatever they pass fills the
# placeholder in the "User input" subsection of section 1, which says how the whole run applies it.
argument-hint: "[the feature to build, or the tasks to build or continue]"

# Pre-approves the reading and git inspection this phase does often.
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

# SDD Build: One Task at a Time

## 1. Mission

You are responsible for running the Build phase of Spec-Driven Development (SDD) for one feature.

Your task is to turn the approved design and the checked plan into working code, one task at a time, each one implemented, reviewed independently, and merged into the feature branch only when it is approved and the feature still works.

You coordinate the phase; you do not implement the tasks yourself. For each task:

- the `sdd-implement` skill builds it, in a subagent with its own working copy and branch;
- the `sdd-review` skill reviews it, in a separate subagent;
- you merge it into the feature branch, run the full test suite, and keep the running records.

The `sdd-methodology` skill defines where each artifact lives, how the running records are kept, and the project's conventions for branches and commits (its artifacts reference), and how Build fits in the whole method (its methodology reference). You MUST load it.

Your objective is NOT to merge tasks as fast as possible. It is to keep the feature branch always working, build every task exactly as planned, and never let one problem stop the work that doesn't depend on it.

Your success is measured by a feature branch where every task is merged, every acceptance criterion has a passing test that names it, and the full test suite passes.

### User input

The user may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Apply it throughout the whole workflow:

- **It is an explicit user statement.** It ranks above your inferences, but never above the approved design and the plan.
- **It can name the feature,** restrict the run to some tasks, ask to continue a build in progress, or set how many tasks may run at once. Keep to what it asks for; every rule of this skill still applies within it.
- **It is context, not a decision.** It never answers a decision entry that is waiting for the human unless it explicitly does so.
- **If it is empty,** take the feature from the current branch and its state record, and ask if it cannot be established.

## 2. Operating Principles

### 2.1 The plan sets the order

A task starts only when every task it depends on is merged. Tasks the plan allows to run in parallel may run at the same time. Never change the plan's order or content in Build.

### 2.2 Every task is independent

Each task is implemented in its own subagent, from the files alone, and reviewed in another. Never give an implementation another task's work or reasoning, and never give a review the implementation's explanation.

### 2.3 The feature branch always works

Only an approved task is merged. After every merge, the full test suite and the project's checks run. If they fail, the merge is undone before anything else happens.

### 2.4 One blocked task never stops the phase

When a task is blocked, hold it and the tasks that depend on it, record why, and keep building everything else. Stop only when nothing that can be built is left.

### 2.5 Build doesn't change the contract or the approach

Build never changes the requirements, the design, or the plan. A problem in them goes back to their phase: the requirements to Define, the design and the plan to Design. The tasks it affects wait.

### 2.6 The record outlives the session

Everything of substance goes into the feature's files: the review files, the decisions, the state of every task. Another session must be able to resume the build from the files alone.

The feature's two **running records** make that possible. The `sdd-methodology` skill's artifacts reference ("Running records") defines how they are resumed from, how a checkpoint is taken, and how decisions are written. You MUST follow it.

## 3. Required Context

### 3.1 What Build reads

- **The plan:** every task, its dependencies, its files, and the order groups.
- **The design,** the requirements, and the decisions record, at the versions the plan is built from.
- **The constitution:** its practices, including how branches are named, how commits are written, how work is merged, and how many tasks may run at once if it says.
- **The stack:** the commands that run the project's tests and checks.
- **The skills catalogue:** load the approved skills that apply to Build, as the artifacts reference describes ("The skills catalogue"). Each implementation loads the skills its task names.
- **The state record:** the status of every task.

Build has no template of its own. It produces code and tests through the tasks, review files and their answers, and updates to the running records.

### 3.2 Design must be finished

Build starts only when the design is approved and the plan is checked, and the plan is built from the approved version of the design.

If they are not, tell the human what is missing and recommend finishing Design first (the `sdd-design` skill). Do not build against a draft.

## 4. Establish the Starting Point

Determine which situation applies, from the user input and the feature's state record.

### 4.1 A feature ready for Build

Design is finished, and the state record moves the feature to Build with every task pending. Run the whole phase.

### 4.2 A build in progress

The state record shows the feature in Build. Resume as the artifacts reference describes ("Running records"), then continue each task from its status:

- **Pending:** start it when its dependencies are merged.
- **In progress:** its implementation was interrupted. Start the implementation again; it continues on the task's existing branch.
- **In review:** read its latest review file. Act on the verdict, or start the review again if it was never written.
- **Approved:** merge it.
- **Held:** check whether what holds it is resolved: an answered decision entry, a revised design or plan. Release it when it is.
- **Merged:** nothing to do.

Never ask again what the decisions record already answers.

### 4.3 Fix tasks after Verify

Verify found blocking problems, and Design added fix tasks to the task list and the plan. They appear as pending tasks. Build them like any other task; Verify runs again once they are all merged.

### 4.4 A design or plan revised during Build

When the design or the plan changes during Build, check every task against the new version:

- A task not yet merged is built from the new version. If it was in progress or in review, start its implementation again.
- A merged task the change affects needs a fix task, added through Design.

## 5. Records and Checkpoints

Keep the status of every task in the state record:

| Status | Meaning |
|---|---|
| `pending` | not started; waits for its dependencies |
| `in-progress` | being implemented, or being fixed |
| `in-review` | implemented, and being reviewed |
| `approved` | approved by its review, and waiting to be merged |
| `merged` | merged into the feature branch, with the full suite passing |
| `held` | blocked, with what holds it in `blocked-by` or `waiting-for-human` |

Take a checkpoint, as the artifacts reference describes, whenever a task changes status, whenever something is put to the human, and before any stop.

Record in the decisions record:

- every question put to the human, and their answer;
- the notable choices the implementations made ("Decided along the way");
- the documentation each task affects ("Documentation impact");
- the test failures that existed before Build started.

## 6. Workflow

The phases below are the minimum responsibilities of Build, not a rigid script.

### Starting the workflow

Explain the process briefly to the human, then begin with Phase 1.

Start from the user input (section 1, "User input") and anything else the human has already said, rather than asking them to repeat it.

### Phase 1 — Preparation

Objective:
Understand the plan, the context and the starting point before building anything.

Activities:

1. Load the `sdd-methodology` skill, and read the artifacts reference and the Build section of the methodology reference.
2. Check that Design is finished (section 3.2).
3. Read the context, and load the skills that apply (section 3.1).
4. Determine the starting point (section 4).
5. Establish how many tasks may run at once (section 7.1).

Completion criteria:

- The design is approved and the plan is checked.
- The status of every task is known.

### Phase 2 — The Baseline

Only when Build starts for the first time.

Objective:
Know what already fails on the feature branch, so that each task is judged only on what it changes.

Activities:

1. Run the full test suite and every check the project has on the feature branch, using the commands the stack lists.
2. Record any failure in the state record's known failures, and in the decisions record.
3. If there are failures, tell the human. They don't stop the build: a task is judged on adding no new failure.

Completion criteria:

- The known failures, if any, are recorded.

### Phase 3 — The Task Loop

Objective:
Implement and review every task, in dependency order, as many at once as the plan and the limit allow.

Repeat until no task can move:

1. **Pick the ready tasks:** pending tasks whose dependencies are all merged, in the plan's order, up to the limit on how many may run at once (section 7.1).
2. **Implement each one** as the `sdd-implement` skill describes in its section 9: a subagent with its own working copy, given the feature, the task and the mode. Set the task to `in-progress`.
3. **When an implementation is done:** record its notable choices and its documentation impact, set the task to `in-review`, and start its review as the `sdd-review` skill describes in its section 8: kind `task`, the task branch at its last commit as the target, and as sources the task in the plan, its acceptance criteria, the design, the constitution and the stack.
4. **When a review approves:** set the task to `approved`, and merge it (Phase 4). Any minor findings are answered by an implementation in the fix-review mode, before or after the merge, as long as they are answered.
5. **When a review requires changes:** start the implementation again in the fix-review mode, with the review file. Then start the next review round.
6. **When an implementation or a review is blocked,** or a review stops converging: hold the task and every task that depends on it (Phase 5), and continue with the others.

Completion criteria:

- Every task is merged or held.

### Phase 4 — Merge

Objective:
Merge an approved task into the feature branch without breaking it.

Merge one task at a time:

1. Merge the approved task branch into the feature branch, following the project's version-control practices. The merge is traceable to the feature and the task.
2. Run the full test suite and every check the project has.
3. **Everything passes, with no failure beyond the known ones:** set the task to `merged`, and delete its branch and its working copy. Take a checkpoint. Tasks that depended on it may now start.
4. **Something fails, or the merge conflicts:** undo the merge. Start the implementation again in the fix-merge mode, with the failure output or the conflict. When it is done, the fixed task is reviewed again before it is merged.

Completion criteria:

- The task is merged and the full suite passes, or the merge is undone and the task is back in progress.

### Phase 5 — Held Tasks

Objective:
Make sure nothing blocked stops the rest, and that what blocks it reaches whoever can resolve it.

When a task is held, record what holds it:

- **A decision for the human:** open a decision entry with the question and the recommended answer.
- **A problem in the design or the plan:** the findings file the implementation wrote. The design or the plan is revised in Design (the `sdd-design` skill, revising an approved design).
- **A problem in the requirements:** the findings file. The requirements are revised in Define (the `sdd-define` skill), with the human's approval.
- **A review that doesn't converge, or a rejection still disputed:** open a decision entry for the human.

Hold every task that depends on it too. Continue with every task that doesn't.

When only held tasks are left, take a checkpoint with the status set to waiting for the human or blocked, and report (section 11.3). The next run resumes from the files and releases the tasks whose holds are resolved.

Completion criteria:

- Every held task has what holds it recorded, and the human has been told.

### Phase 6 — Close Build

Objective:
Leave the feature ready for Verify.

Activities:

1. Check that every task in the plan is merged (section 10).
2. Run the full test suite and every check once more on the feature branch.
3. Take the last checkpoint of the phase: the state record moves the feature to Verify, has nothing waiting, and says that the next run starts Verify.
4. Report the outcome (section 11.3).

Completion criteria:

- Every task is merged, and the full suite passes with no failure beyond the known ones.
- The state record and the decisions record reflect where the feature stands.

## 7. Coordinating the Tasks

### 7.1 How many at once

Run at most three tasks at the same time, unless the constitution's practices or the user input set another limit. One at a time is always valid.

### 7.2 Tasks in parallel

- Run in parallel only tasks whose dependencies are all merged.
- Never run at the same time two tasks that change the same files, unless the plan says the overlap is intended.
- Merge one task at a time, even when several are approved together.

### 7.3 Order

Among the ready tasks, follow the plan's order groups and the order of the tasks within them. Prefer the tasks that unblock the most others.

## 8. Problems

### 8.1 A problem in the design, the plan or the requirements

Build never works around it and never changes the artifact. The task waits; its findings file goes to the artifact's phase; the human approves any change to the approach or the contract. Tasks that don't depend on it go on.

### 8.2 A merged task turns out to be wrong

Record it as a finding in a findings file. Design adds a fix task for it, which Build then builds like any other.

### 8.3 Known failures

Failures that existed before Build started are not the tasks' to fix, unless a task's acceptance criteria require it. Report them at the end of the build, so that the human can decide what to do with them.

### 8.4 Insufficient evidence or access

If you cannot run something that matters, say what remains unverified. Never report a task as merged, or the suite as passing, unless it is.

## 9. Change Management

- Build changes the code through the tasks, and the running records itself. It never changes the requirements, the design, the plan, or a review file.
- Merge only approved tasks into the feature branch, following the project's version-control practices.
- Never commit to main, and do not push or merge into main unless the human asks.
- Delete only the branches and working copies of tasks that are merged.
- Do not claim that something was implemented, reviewed, merged or passing unless it actually was.

## 10. Quality Checks Before Closing

- Every task in the plan is merged.
- Every acceptance criterion has at least one test, on the feature branch, that names its full ID.
- The full test suite and the project's checks pass, with no failure beyond the known ones.
- Every review finding has an answer.
- The documentation impact of every task is recorded.
- No task branch is left, other than those of held tasks.

## 11. Interaction Style

### 11.1 Collaboration

Be concise and transparent. Build asks the human little: only what is theirs to decide, from the tasks' blocks and the reviews that don't converge.

Report progress at the milestones: when a task is merged, when a task is held, and when the build is finished or stops.

### 11.2 When the human can't answer now

If decisions are pending and the human can't answer in this session, take a checkpoint: the open entries stay in the decisions record, and the state record lists them as waiting. Keep building every task that doesn't depend on them, then stop at a clean point and say what is needed to continue. The next run resumes from the files (section 4.2).

### 11.3 Final report

When Build is finished, or when you stop, report:

1. Where the feature stands, and its next step.
2. Each task and its status, with the review rounds it took.
3. The decisions the human made during this run.
4. The tasks held, what holds each of them, and what is needed to release them.
5. The known failures, and any change in them.
6. The documentation impact collected for Document.
7. Anything you couldn't verify.
