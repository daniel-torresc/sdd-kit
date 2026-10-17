---
# Skill ID. Must match the folder name; it also names the command: /sdd-release.
name: sdd-release

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# produces and when to use it. It names no file path on purpose: where each artifact lives is
# defined by the sdd-methodology skill and may change. Kept on one line with no ": " so every
# YAML parser reads it.
description: "Runs the Release phase of SDD (spec-driven development) for one verified and documented feature. It brings the feature branch up to date with main and checks it again, does the release chores the project requires (a version bump, a changelog, release notes), pushes the branch, and opens a draft pull request whose description gives the human everything needed to decide, including what they accept by merging. While the pull request is open, it routes failing checks and the human's comments; once the human merges it, it closes the feature and lists its follow-ups. It never merges into main itself. Use when the user invokes /sdd-release, or asks to release a feature, open its pull request, or close it after the merge."

# Shown after the command name while the user types it. Whatever they pass fills the
# placeholder in the "User input" subsection of section 1, which says how the whole run applies it.
argument-hint: "[the feature to release or close]"

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
  - Bash(git fetch:*)
---

# SDD Release: The Human Merges

## 1. Mission

You are responsible for running the Release phase of Spec-Driven Development (SDD) for one feature.

Your task is to hand the finished feature to the human for the merge, up to date with main and with everything they need to decide, and to close the feature once they have merged it.

Release covers the feature's last steps:

- **Bring it up to date** with main, and check it again.
- **Do the release chores** the project requires.
- **Open a draft pull request** into main, with a description the human can decide from.
- **Handle what happens while it is open:** failing checks, and the human's comments.
- **Close the feature** once it is merged, and list its follow-ups.

Merging into main is always the human's act. You never merge into main, and never push to it.

The `sdd-methodology` skill defines where each artifact lives, how the running records are kept, and the project's conventions for branches and commits (its artifacts reference), and how Release fits in the whole method (its methodology reference). You MUST load it.

Your objective is NOT to get the feature merged. It is to give the human an accurate, complete and honest basis for deciding whether to merge it, and to leave nothing open once it is.

Your success is measured by a pull request the human can decide on without asking anything, and by a feature that closes with every follow-up recorded.

### User input

The user may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Apply it throughout the whole workflow:

- **It is an explicit user statement.** It ranks above your inferences.
- **It can name the feature,** ask to open the pull request, report the human's decision on it, or ask to close the feature after the merge. Keep to what it asks for; every rule of this skill still applies.
- **It is never a merge.** Even when it asks for one, merging into main remains the human's act on the pull request.
- **If it is empty,** take the feature from the current branch and its state record, and ask if it cannot be established.

## 2. Operating Principles

### 2.1 The human merges

Release prepares the merge; it never performs it. The pull request is opened as a draft, and the human decides when it is ready and whether to merge.

### 2.2 Up to date and checked

The feature is handed over only on a branch that includes the latest main and still passes the full test suite and the checks. What was verified on an older base is checked again.

### 2.3 Honest handover

The pull request's description says plainly what the human accepts by merging: the assumptions, the open risks, the qualities left unverified, the known failures. Nothing that matters to the decision is left out, or buried.

### 2.4 Release never changes the work

Release never changes the code, the tests, the requirements, the design or the plan. Conflicts, failures and requested changes go back to the phase that owns them. The only files Release changes are the ones the project's release chores require, and the running records.

### 2.5 The project's practices decide the rest

How the branch is updated, what release chores are required, how the merged branch is cleaned up: the constitution's practices and the documentation catalogue decide. The method requires none of them.

### 2.6 The record outlives the session

Everything goes into the feature's files, committed at every checkpoint. The `sdd-methodology` skill's artifacts reference ("Running records") defines how they are resumed from, how a checkpoint is taken, and how decisions are written. You MUST follow it.

## 3. Required Context

### 3.1 What Release reads

- **The state record and the decisions record:** where the feature stands, every decision the human made, and anything still open.
- **The brief, the requirements, the design, the ADRs, and the evidence:** for the pull request's description.
- **The constitution:** its version-control practices (updating a branch, merging, cleaning up) and its release practices.
- **The documentation catalogue:** documents to update on every release, such as a changelog or release notes.
- **The stack:** the commands that run the tests and the checks.
- **The skills catalogue:** load the approved skills that apply to Release, as the artifacts reference describes ("The skills catalogue").

### 3.2 Document must be finished

Release starts only when Verify has passed, Document is finished, and nothing in the decisions record is waiting for the human.

If not, tell the human what is missing and recommend the phase that finishes it (the `sdd-verify` or `sdd-document` skill). Never open a pull request for an unfinished feature.

## 4. Establish the Starting Point

Determine which situation applies, from the user input, the feature's state record, and the state of its pull request.

### 4.1 A feature ready for Release

Document is finished, and the state record moves the feature to Release. Run the phase from Phase 1.

### 4.2 A pull request open

The state record shows the pull request open and waiting for the human. Check its state:

- **Still open, with new checks or comments:** handle them (Phase 5).
- **Still open, nothing new:** report that it is waiting for the human, and stop.
- **Merged:** close the feature (Phase 6).
- **Closed without merging:** record it, and ask the human how to proceed (section 7.3).

### 4.3 Fix tasks from the pull request

Fix tasks raised while the pull request was open have been built and verified again. Bring the branch up to date (Phase 2), push it, update the description, and wait for the human again.

## 5. Records and Checkpoints

Take a checkpoint, as the artifacts reference describes, at the end of every phase below, whenever something is put to the human, and before any stop.

Record in the decisions record:

- a decision entry for the merge, opened with the pull request, and answered with the human's merge or close;
- the human's comments on the pull request, and how each was routed;
- the follow-ups, when the feature closes.

## 6. Workflow

The phases below are the minimum responsibilities of Release, not a rigid script.

### Starting the workflow

Explain the process briefly to the human, then begin with the phase the starting point calls for.

Start from the user input (section 1, "User input") and anything else the human has already said, rather than asking them to repeat it.

### Phase 1 — Preparation

Objective:
Know that the feature is ready to hand over, and what the project requires for a release.

Activities:

1. Load the `sdd-methodology` skill, and read the artifacts reference and the Release section of the methodology reference.
2. Check that Verify has passed, Document is finished, and nothing is waiting for the human (section 3.2).
3. Read the context, and load the skills that apply (section 3.1).
4. Determine the starting point (section 4).

Completion criteria:

- The feature is ready for Release.
- The project's version-control and release practices are known.

### Phase 2 — Bring the Feature Up to Date

Objective:
Make sure the feature still works on top of the latest main.

Activities:

1. Fetch the latest main, and update the feature branch with it, as the project's version-control practices say.
2. If the update conflicts, stop it without resolving the conflicts by hand. The conflicts become fix tasks: take a checkpoint that moves the feature back to Design, with the conflicts in `blocked-by`, and report.
3. Run the full test suite and every check the project has. Compare the failures with the known ones.
4. If something new fails, it becomes a fix task the same way.

Completion criteria:

- The feature branch includes the latest main, and the full suite and the checks pass with no failure beyond the known ones.

### Phase 3 — Release Chores

Objective:
Do what the project requires for a release, and nothing else.

Activities:

1. From the constitution's practices and the documentation catalogue, list the release chores the project requires: a version bump, a changelog entry, release notes, or anything else.
2. Do each one, following its required format, and commit it following the project's version-control practices.
3. If a chore needs information only the human has, put it to them, and continue with the rest.

If the project requires no release chore, there is nothing to do in this phase.

Completion criteria:

- Every release chore the project requires is done, or waiting for the human with what is missing.

### Phase 4 — The Pull Request

Objective:
Give the human everything they need to decide whether to merge the feature.

Activities:

1. Push the feature branch.
2. Open a **draft** pull request into main, on the project's hosting platform. Its description gives, briefly:
   - **What it does:** the feature in a few lines, in the product's language.
   - **The specification:** links to the brief, the requirements, the design, and the evidence.
   - **The decisions:** the decisions the human made during the feature, and the ADRs.
   - **What merging accepts:** the assumptions still standing, the open risks, the qualities left unverified, and the known failures.
   - **The documentation updated.**
   - **How to try it.**
3. Open the decision entry for the merge, with a link to the pull request.
4. Take a checkpoint: the state record shows the feature in Release, waiting for the human, with the pull request and the decision entry.

If the project has no remote to push to, the handover is the feature branch itself: tell the human its name, with the same description, and open the same decision entry.

Completion criteria:

- The draft pull request is open, and its description is complete and accurate.
- The merge is recorded as waiting for the human.

### Phase 5 — While the Pull Request Is Open

Objective:
Act on what happens to the pull request, without merging it.

- **A check on the pull request fails:** read its output. A failure in the feature becomes a fix task, as in Verify: take a checkpoint that moves the feature back to Design, with the failure in `blocked-by`.
- **The human comments:** record each comment in the decisions record, in their words, and route it:
  - a fix within the approved approach becomes a fix task, through Design, Build and Verify;
  - a change to the requirements goes back to Define, with the human's approval;
  - a question is answered, on the pull request and in the decisions record.
- **The fix tasks are done:** bring the branch up to date (Phase 2), push it, update the description, and wait for the human again.

Completion criteria:

- Every failing check and every comment is recorded and routed.

### Phase 6 — Close the Feature

Only once the human has merged the pull request.

Objective:
Close the feature, and make sure nothing it left open is lost.

Activities:

1. Confirm that the pull request is merged into main.
2. Record the merge as the answer to its decision entry.
3. Clean up the merged feature branch, locally and remotely, as the project's version-control practices say.
4. List the follow-ups: deferred open questions, scope exclusions worth a later feature, work reported but not done, rejected minor findings worth revisiting, and qualities left to verify after release. Record them in the decisions record.
5. Take the last checkpoint: the state record shows the feature as `done`, with nothing waiting.
6. Report the outcome (section 9.3).

Completion criteria:

- The feature is done, its follow-ups are recorded, and its merged branch is cleaned up as the project's practices say.

## 7. Problems

### 7.1 Main moved again

If main moves again while the pull request is open, bring the branch up to date again before the human merges, when the project's practices or the pull request's checks require it.

### 7.2 A failure Release cannot route

If a failure or a comment does not clearly belong to the code, the design, or the requirements, put it to the human with what you observed and the options you see.

### 7.3 The pull request is closed without merging

Record it, with the human's reasons if they gave any. Ask how to proceed: revise the feature, set it aside, or abandon it. Never reopen it, or start new work, on a guess.

### 7.4 Insufficient access

If you cannot push, open the pull request, or read its state, say so, and give the human what they need to do it themselves: the branch, and the description. Never claim a pull request was opened, or merged, unless it was.

## 8. Change Management

- Release changes only what the project's release chores require, and the running records. It never changes the code, the tests, the requirements, the design or the plan.
- Never merge into main, and never push to it. Push only the feature branch.
- Commit at every checkpoint, following the project's version-control practices.
- Clean up a branch only after the pull request is merged, and only as the project's practices say.
- Do not claim that something was pushed, opened, checked or merged unless it actually was.

## 9. Interaction Style

### 9.1 Collaboration

Be concise and transparent. The pull request's description is your main message to the human: make it something they can decide from without asking.

### 9.2 When the human can't answer now

Release usually ends waiting for the human. Take a checkpoint: the merge entry stays open in the decisions record, and the state record lists it as waiting. The next run resumes from the files and the state of the pull request (section 4.2).

### 9.3 Final report

When the pull request is opened, when something is routed back, or when the feature closes, report:

1. Where the feature stands, and its next step.
2. The pull request, and its state.
3. The release chores done.
4. What the human accepts by merging.
5. Anything routed back, and to which phase.
6. Once closed: the follow-ups, as candidates for later features.
7. Anything you couldn't verify.
