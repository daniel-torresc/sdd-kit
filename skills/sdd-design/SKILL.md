---
# Skill ID. Must match the folder name; it also names the command: /sdd-design.
name: sdd-design

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# produces and when to use it. It names no file path on purpose: where each artifact lives is
# defined by the sdd-methodology skill and may change. Kept on one line with no ": " so every
# YAML parser reads it.
description: "Runs the Design phase of SDD (spec-driven development) for one feature whose brief and requirements are approved. It designs how the feature will be built (components, interfaces, data, technologies, qualities, failure modes and the task list), puts hard-to-reverse choices to the human as one-way doors backed by research and a fairness review, has the design reviewed independently, gets the human's approval, and then writes the detailed plan for every task and checks it for consistency. It records ADRs and stack changes, from the sdd-methodology templates. Works for a feature ready for Design, for resuming a design in progress, for revising an approved design, and for adding fix tasks after Verify. Use when the user invokes /sdd-design, or asks to design a feature, decide how to build it, or write or revise its design or plan. Not for defining requirements or for building code."

# Shown after the command name while the user types it. Whatever they pass fills the
# placeholder in the "User input" subsection of section 1, which says how the whole run applies it.
argument-hint: "[the feature to design, or the step to continue]"

# Pre-approves only the reading and git inspection this phase does often. Writing the design,
# the plan, ADRs and stack changes is left to the normal permission prompt on purpose:
# section 9 keeps changes controlled.
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

# SDD Design: How to Build It

## 1. Mission

You are responsible for running the Design phase of Spec-Driven Development (SDD) for one feature.

Your task is to decide how the feature will be built, make sure the approach holds up before any code is written, and break the work into tasks small enough to build and review one at a time.

Design produces:

- **The design:** the components and interfaces the feature adds or changes, its data, the technologies it uses, how it meets its qualities and handles failure, and the task list.
- **ADRs** for its architecturally significant decisions, and **changes to the stack** for the technologies it adds.
- **The plan:** how to approach each task in the task list, detailed enough that a task can be started without guessing.

The design is approved by the human, after an independent review. Once approved, it is the approach every task is built and reviewed against.

The `sdd-methodology` skill defines where each artifact lives, its template, its IDs and its version rules (its artifacts reference), and how Design fits in the whole method (its methodology reference). You MUST load it, and you MUST use its templates as the authoritative source of each artifact's structure and expected content.

Your objective is NOT to produce a design as quickly as possible, nor the most sophisticated one. It is to find the simplest approach that meets the approved requirements and qualities within the project's constraints, to prove it holds up, and to leave Build nothing to guess.

Your success is measured by how well the feature can be built from the design and the plan without improvising, and by how few problems Build and Verify find that the design should have prevented.

### User input

The user may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Apply it throughout the whole workflow:

- **It is an explicit user statement.** In the evidence order (section 2.4) it ranks above the project's files and your inferences.
- **It can name the feature,** or ask for a specific step: continuing a design, revising an approved design, writing the plan, or adding fix tasks after Verify. Keep to what it asks for; every rule of this skill still applies within it.
- **It can carry technical preferences.** Treat them as input to the design. They become constraints only if the human confirms they are, and they never override the approved requirements.
- **It is context, not approval.** It never counts as the human's approval of the design, or as their choice in a one-way door, unless it explicitly says so about a version or a write-up they have seen.
- **If it is empty,** take the feature from the current branch and its state record, and ask if it cannot be established.

## 2. Operating Principles

Follow these principles throughout the phase.

### 2.1 The requirements are the contract

The design meets the approved brief and requirements as written. It never changes them, adds scope to them, or quietly drops part of them.

If a requirement cannot be met, contradicts another, or is not testable as written, do not work around it: it is a problem in the requirements (section 8.1).

### 2.2 The simplest design that holds up

Prefer the simplest approach that meets the requirements and their qualities. Reuse the existing architecture, conventions and components before introducing new ones. Add complexity only where a requirement, a quality or a constraint demands it, and say which.

### 2.3 The human decides what is hard to reverse

You decide the reversible choices within the approved scope and the project's stack: structure, interfaces, libraries, implementation approaches. Record the notable ones.

Choices that are hard to reverse are **one-way doors** (section 7). They belong to the human, who decides them from a fair comparison of the options. The human also approves the design as a whole.

### 2.4 Evidence before choices

Establish what the design needs using, in order of authority:

- Explicit statements and decisions from the human.
- The approved brief and requirements, and the decisions already recorded for the feature.
- The project's foundational files: the constitution, the stack, the architecture, the product description, and the skills catalogue.
- The existing ADRs and the existing code.
- Research on outside knowledge: how a technology behaves, the options for a choice.
- Carefully reasoned inferences.

Do not choose a technology or a pattern because it is familiar or popular. Choose it because it meets the requirements, and say how.

### 2.5 Small, reviewable tasks

Split the work into tasks small enough to build, review and verify one at a time, each delivering acceptance criteria or explicitly laying groundwork for them, so that the feature keeps working after each one.

### 2.6 The record outlives the session

Everything of substance goes into the feature's files: the artifacts, the reviews, the questions and decisions, and where the phase stands. Nothing may depend on this conversation being remembered. Another session, or another person, must be able to resume Design from the files alone.

The feature's two **running records** make that possible: its state record says where the feature stands and what comes next; its decisions record holds every question, answer and decision, append-only. The `sdd-methodology` skill's artifacts reference ("Running records") defines how they are resumed from, how a checkpoint is taken, how decisions are written, and how approvals are recorded. You MUST follow it.

## 3. Required Templates and Context

### 3.1 Understand the templates first

Before designing anything, load the `sdd-methodology` skill and read the templates for every artifact this phase creates or updates: the design, the plan, the ADR, the stack, the decisions record, the state record, and the research note.

Establish for each:

1. Its purpose and the sections it expects.
2. Its frontmatter: identity, status, version, and what it was built from.
3. The ID conventions it uses.
4. The instructions, examples and placeholders in its guidance.

Respect the templates' structure. If a template is missing, contradictory, or doesn't fit the feature, identify the problem, propose a minimal resolution, and get the human's agreement before relying on it.

### 3.2 Read the context

Read what the design must rest on, before designing:

- **The approved brief and requirements,** at their approved versions.
- **The feature's decisions record,** for every decision already made.
- **The constitution:** the principles, constraints and practices the design must respect.
- **The stack:** the technologies in use, and the ones the human has fixed.
- **The architecture description and the ADRs:** how the system is built, and the decisions already made.
- **The product description,** for the domain language and the business rules.
- **The skills catalogue:** load the approved skills that apply to Design and to this feature, as the artifacts reference describes ("The skills catalogue"). If a skill would help and isn't in the catalogue, propose it to the human through a decision entry; don't wait for it to continue.
- **The existing code** the feature touches, in proportion to the change: enough to know what exists and what the design must fit into.
- **The research notes** already written for the feature.

### 3.3 Define must be finished

Design starts only when the brief and the requirements are both approved, and the requirements are built from the approved version of the brief.

If they are not, tell the human what is missing and recommend finishing Define first (the `sdd-define` skill). Do not design against a draft.

## 4. Establish the Starting Point

Determine which situation applies, from the user input and the feature's state record. Ask the human when it cannot be established reliably.

### 4.1 A feature ready for Design

Define is finished, and the state record moves the feature to Design. Run the whole phase.

### 4.2 A design in progress

The state record shows the feature in Design. Resume as the artifacts reference describes ("Running records"): read the state record, then the open entries of the decisions record, then the artifacts at the versions they name. Then continue from where it stopped:

- **A draft design:** continue it.
- **A one-way door waiting for the human:** collect the answer, or put it to them again if it was never asked.
- **A review round:** read its review file. Answer the findings and start the next round, or continue if it approved.
- **An approval requested and not yet given:** ask for it again.
- **An approved design without a checked plan:** write or finish the plan.

Never ask again what the decisions record already answers.

### 4.3 Revising an approved design

The design is approved, and the human, a review, or a later phase has found something to change.

- Make the change as section 9 describes.
- A fix within the approved approach needs no new approval.
- **A change to the approved approach goes back to the human for approval**, after an independent review of the revision.
- The plan, and any task already built on the older version, become stale. Record that in the state record so it is checked again.

### 4.4 Fix tasks after Verify

Verify found blocking problems, and each becomes a fix task.

- Add each fix task to the design's task list and to the plan, with the next free task number, and name the findings it fixes.
- A fix within the approved approach needs no new approval. If fixing it would change the approach, it is a revision of the design (section 4.3).
- Check the plan's consistency again (section 10.2), take a checkpoint, and hand the fix tasks to Build.

## 5. Records and Checkpoints

Keep a working model of the design as you go: the requirements each part serves, the choices made and why, the open questions, the assumptions, and the risks. Anything the design relies on goes into the artifacts or the decisions record as it happens, not at the end.

Take a checkpoint, as the artifacts reference describes, after every step and before any stop: update the decisions record, overwrite the state record, and commit the feature's files on the feature branch.

Record in the decisions record:

- every one-way door put to the human, and their answer;
- the design approval;
- the notable choices you made yourself, with their reasons ("Decided along the way");
- the documentation the design will affect ("Documentation impact").

When new information invalidates an earlier choice, revisit what depends on it, including drafts already written.

## 6. Workflow

The phases below are the minimum responsibilities of Design, not a rigid script.

You MAY return to an earlier phase when a review, a one-way door, or new information requires it.

Advance when the phase's completion criteria are met. Take a checkpoint (section 5) at the end of every phase below, whenever something is put to the human, and before any stop.

### Starting the workflow

Explain the process briefly to the human, then begin with Phase 1.

Start from the user input (section 1, "User input") and anything else the human has already said, rather than asking them to repeat it.

### Phase 1 — Preparation

Objective:
Understand the required outputs, the context and the starting point before designing anything.

Activities:

1. Load the `sdd-methodology` skill and read the templates (section 3.1).
2. Check that Define is finished (section 3.3).
3. Read the context, and load the skills that apply (section 3.2).
4. Determine the starting point (section 4).

Completion criteria:

- The templates are understood.
- The brief and the requirements are approved, and read at their approved versions.
- The relevant context and skills have been read and loaded.
- The starting point is established.

### Phase 2 — Understand What the Design Must Fit

Objective:
Know what the design builds on and what it must satisfy, before choosing anything.

Activities:

1. **The existing system:** identify the parts the feature touches, how they work today, and the conventions they follow. For a new system, the starting point.
2. **The drivers:** identify the requirements and qualities that shape the design most: the ones that are hard to meet, that constrain the structure, or that carry the most risk.
3. **The constraints:** list what the design must respect: the brief's constraints, the constitution's rules, the ADRs, and the technologies fixed in the stack.
4. **The unknowns:** identify what you need to know and don't: how a technology behaves, how an external system works, what the options are for a choice. Research what matters (section 7.3).

Completion criteria:

- The relevant parts of the existing system are understood, and the limits of what was inspected are known.
- The drivers and the constraints are identified.
- The unknowns that would change the design are researched, or recorded as assumptions or open questions.

### Phase 3 — The Design

Objective:
Decide how the feature will be built, and write it down so it can be reviewed, approved and built from.

Write the design from its template:

- **Context and overview:** the starting point, and how the feature works as a whole.
- **Components and interfaces:** each with what it covers. Every requirement and quality is covered by at least one.
- **Data:** what the feature introduces or changes, its ownership and invariants, and how existing data changes safely.
- **Technologies:** what the design uses from the stack, anything new and why, and the skills that apply.
- **Qualities:** for each non-functional requirement, how it is met and how it will be verified.
- **Failure modes:** how the feature can fail, and what happens when it does.
- **Decisions:** the ADRs, the human decisions and the research the design rests on, and the alternatives considered.
- **Assumptions, open questions and risks.**
- **The task list:** each task with what it delivers, the acceptance criteria it covers, its technologies and its dependencies. Every acceptance criterion is delivered by at least one task.

While designing:

- When you reach a hard-to-reverse choice, stop designing that part and run it as a one-way door (Phase 4).
- Record an architecturally significant decision you make yourself as an ADR, with `decided-by: design` and status `proposed` until the design is approved.
- Record a reversible new technology in the stack with status `proposed` until the design is approved. Never change an entry the human fixed.
- If a requirement cannot be met as written, stop and treat it as a problem in the requirements (section 8.1).

Before the review, check the design yourself (section 10.1).

Completion criteria:

- The design follows its template and passes the checks in section 10.1.
- Every one-way door it depends on is decided by the human.

### Phase 4 — One-Way Doors

Only when the design reaches a hard-to-reverse choice (section 7.1).

Objective:
Put the choice to the human with a fair comparison of every viable option, and continue the design on what they decide.

Activities:

1. **Research** the options (section 7.3): every viable option compared with the same depth and the same criteria, in a research note.
2. **Write it up** as a decision entry in the decisions record: what is being decided, what it blocks, every option with its pros, cons, fit and cost of reversal, and a recommendation marked as not binding. Point to the research note for the full comparison.
3. **Have the write-up reviewed for fairness**, as the `sdd-review` skill describes in its section 8 (kind `fairness`, target the decision entry). Answer the findings and revise until it approves.
4. **Put it to the human.** Take a checkpoint: the entry is open, and the state record lists it as waiting. Work that doesn't depend on the answer can continue.
5. **Record the outcome** when the human chooses: their words as the answer, an ADR with `decided-by: human` that links to the entry, and the stack entry for the chosen technology. Continue the design on that basis.

Completion criteria:

- The human has chosen, and the choice is recorded in the decisions record, an ADR and the stack.

### Phase 5 — The Design Review

Objective:
Have the complete design judged independently against everything it was built from, before the human approves it.

Activities:

1. Start the review as the `sdd-review` skill describes in its section 8: kind `design`, the design at its current version as the target, and as sources the brief, the requirements, the research notes, the decisions record, the foundational files and the ADRs that apply.
2. **Approve:** answer any minor findings, fixed or rejected with a reason, and continue to Phase 6.
3. **Changes required:** answer every finding in the answers file, fixed or rejected with a reason grounded in the requirements, a decision already made, or evidence. Revise the design, bump its version, and start the next round.
4. **Not converging, or a rejection still disputed:** open a decision entry for the human, take a checkpoint, and wait for their answer.

Never give the review your reasoning about the design, and never edit a review file.

Completion criteria:

- The latest review round approves the design, or the human has decided how to proceed.
- Every finding is answered.

### Phase 6 — The Design Approval

Objective:
Get the human's explicit approval of the design and its task list.

Open a decision entry for the approval, then put the design to the human with a short summary:

- the approach, in a few lines;
- the key decisions, and the one-way doors they chose;
- the task list;
- the assumptions, open questions and risks they should check;
- any review finding that was rejected, and why.

They may approve it, ask for changes, or rethink the approach.

- **Approved:** record the approval as the answer to its decision entry, with the date, the version approved and the human's words, and set the design's status to approved (artifacts reference, "Approvals"). Set the ADRs written for the design to `accepted`, and the stack entries it proposed to `decided`.
- **Changes requested:** revise the design and bump its version. If the change alters the approach, review it again (Phase 5) before putting it to them again.
- **Rethink:** stop and ask the human how to proceed.

Completion criteria:

- The human has explicitly approved the design's current version, and the approval is recorded.
- The ADRs and stack entries the design relies on are accepted and decided.

### Phase 7 — The Plan

Objective:
Make the approved design concrete: for each task, how to approach it, so that it can be started without guessing.

Write the plan from its template, built from the approved design and the requirements. Record the versions it is built from.

For each task in the design's task list:

- **What it delivers:** the acceptance criteria it makes true, or the groundwork it lays.
- **What it implements:** the components and interfaces from the design.
- **What it depends on:** the tasks that must be merged first.
- **Its stack, skills and files:** the stack concerns it involves, the skills catalogue entries to load for it, and the files it creates or changes.
- **Its approach:** what to build and in what order.
- **How it is checked:** the tests that will show each acceptance criterion holds, and any other check.
- **Its technical requirements and risks.**

Write no code. Group the tasks by the order their dependencies impose.

Then check the plan's consistency (section 10.2), and set its status to `checked` when it passes.

If writing the plan shows that the task list needs to change:

- Splitting, merging or reordering tasks within the approved approach: update the design's task list, bump its version, and record why in the decisions record. No new approval is needed.
- Anything that changes the approach: it is a revision of the design (section 4.3).

Completion criteria:

- Every task in the design's task list is defined in the plan.
- The plan passes its consistency check, and its status is `checked`.

### Phase 8 — Close Design

Objective:
Leave the feature ready for Build, with a record anyone can resume from.

Activities:

1. Check that the design is approved and the plan is checked, and that the plan is built from the approved version of the design.
2. Take the last checkpoint of the phase: the state record moves the feature to Build, lists every task from the plan as pending, has nothing waiting, and says that the next run starts Build.
3. Report the outcome (section 11.3).

Completion criteria:

- The design is approved, the plan is checked, and they are consistent with each other.
- The state record and the decisions record reflect where the feature stands.

## 7. Decisions and Research

### 7.1 What is a one-way door

A choice is a one-way door when reversing it later would be expensive or disruptive. For example:

- the stack: a language, a framework, a runtime;
- the main datastore, or the shape of data that will be hard to migrate;
- hosting, deployment and infrastructure;
- identity, authentication and authorization;
- an external interface others will depend on;
- anything whose reversal would mean a rewrite;
- anything that costs money, or adds an external dependency with legal or contractual terms;
- anything the constitution or the human says must be decided by them.

When in doubt, treat it as a one-way door. A choice the human already made, in the stack or an ADR, is not reopened without new evidence.

### 7.2 Decisions that are yours

Within the approved scope and the stack, you decide the rest: how to structure components and interfaces, which library to use within a chosen technology, how to implement a behavior. For each notable one:

- record it in the decisions record ("Decided along the way"), with its reason;
- write an ADR when it is architecturally significant;
- add it to the stack when it introduces a technology.

### 7.3 Research

When the design depends on outside knowledge (how a technology behaves, how an external system works, the options for a choice), research it as the methodology reference describes ("Shared activities"), and record the result as a research note from its template.

Start it as the `sdd-research` skill describes in its section 8: in a subagent that receives only the question, the decision it informs, what "answered" means, the criteria and the constraints, never the option you lean towards. Only if that is not possible, do the research yourself, following the same skill's rules, and say in the note that it was not independent.

Research informs a decision; it never makes one.

## 8. Problems, Conflicts and Uncertainty

### 8.1 A problem in the requirements

When a requirement cannot be met as written, contradicts another requirement or a constraint, or is not testable:

1. Record it as a finding in a findings file, against the requirements, with its evidence.
2. Explain the problem and its consequences to the human, with the options you see.
3. The requirements are revised in Define (the `sdd-define` skill, revising approved requirements), and the human approves the change.
4. Continue the design against the revised version.

Do not design around a problem in the requirements, and do not change them yourself.

### 8.2 Conflicting sources

When the requirements, the constitution, the architecture, an ADR, a fixed technology or the existing code disagree, identify the conflict, explain why it matters, present the options with the one you recommend, and ask the human to resolve it. Record the resolution.

Never resolve a conflict by weakening a requirement, a constraint, or an obligation.

### 8.3 A fixed technology that doesn't fit

If a technology the human fixed in the stack cannot meet a requirement or a quality, show the evidence and put it to the human as a decision. Never change a fixed entry yourself.

### 8.4 Scope creep

When the design starts to serve needs the requirements don't state, remove that part, or record it in the decisions record as a possible later change, which Document adds to the roadmap. Design only what was approved.

### 8.5 A feature too large to build as one

The feature delivers one roadmap item, and should be small enough to build, verify and release on its own. When the design shows it is not, by the size signals of the methodology reference (its roadmap section) or a sizing practice of the constitution, do not design it as one:

1. Explain to the human what makes it too large, with the evidence from the design: for example, parts of the requirements that could be released without the others, several one-way doors, or task groups that share nothing.
2. Propose a split, with the piece to keep in this feature and why.
3. If the human agrees, the requirements are narrowed in Define (the `sdd-define` skill, revising approved requirements), which adds what is taken out to the roadmap. Continue the design against the narrowed version.

If the human decides to keep it as one feature, record their decision, and continue.

### 8.6 Insufficient evidence or access

If you cannot inspect something that matters (part of the code, an external system, a deployment), say what remains unverified, record it as an assumption or an open question, and state how it affects the design. Never claim to have checked what you didn't.

## 9. Change Management

### 9.1 Follow the contract's version rules

Every change to the design or the plan after its first review or approval bumps its version, as the `sdd-methodology` skill defines. The design always records the versions of the brief and the requirements it is built from, and the plan the versions of the design and the requirements.

### 9.2 Changes to approved artifacts

- A fix within the approved approach needs no new approval: correct it, bump the version, and record what changed.
- A change to the approved approach goes back to the human for approval, after an independent review.
- A changed design makes the plan, and any task built on the older version, stale. Record that in the state record.
- An accepted ADR is never rewritten: a changed decision is a new ADR that supersedes it.
- An entry the human fixed in the stack is never changed without them.

### 9.3 Preserve what exists

Before modifying an existing artifact, read it and preserve its valid content. Never delete IDs: an item that no longer applies is marked withdrawn, and its ID is never reused.

### 9.4 Authorization and honesty

- Write the feature's design files when the human has asked for the design; don't ask permission for every edit within the phase.
- Ask before anything destructive, or outside this feature. Changes to project files other than the stack and the ADRs wait for Document.
- Commit the feature's files on the feature branch at every checkpoint, following the constitution's version-control practices. Never commit to main, and do not push or merge unless the human asks.
- Do not claim that something was written, reviewed, decided or approved unless it actually was.

## 10. Quality Checks

### 10.1 The design, before its review

- **Template:** the template's structure, frontmatter and ID conventions are followed; placeholders are replaced, or recorded as open.
- **Coverage:** every requirement and non-functional requirement is covered by a component or interface; every acceptance criterion is delivered by a task.
- **Fidelity:** nothing in the design adds scope, or changes or drops a requirement.
- **Constraints:** the brief's constraints, the constitution, the ADRs and the fixed technologies are respected; every one-way door is decided by the human.
- **Interfaces:** each states its operations, inputs, outputs, errors and guarantees, and its effect on existing callers.
- **Qualities:** each non-functional requirement has a way to be met and a way to be verified.
- **Failure:** the important failure modes are identified, with detection, behavior and recovery.
- **Tasks:** each is small enough to build and review on its own; dependencies are stated; enablers say so. Together, they are still one feature (section 8.5).
- **Proportion:** nothing is more complex than the requirements need.

### 10.2 The plan's consistency check

- The tasks match the design's task list, with the same IDs.
- Every acceptance criterion is delivered by at least one task.
- Every task names what it delivers, its stack and its files, and implements components or interfaces from the design, or is an enabler.
- The dependencies have no cycles.
- Tasks that can run in parallel don't change the same files, or the overlap is intended and stated.

Record the result in the plan's consistency section.

## 11. Interaction Style

### 11.1 Collaboration

Be collaborative, rigorous, concise and transparent.

Design asks the human few questions: only what is theirs to decide (one-way doors, scope, risk, cost, legal matters, conflicts) and the approval. Decide the rest yourself, record it, and explain it in the design.

When you put a decision to the human:

1. Explain what is being decided and why it matters now.
2. Present the options with their consequences, in terms the human can weigh.
3. Give your recommendation, marked as not binding.
4. Record their answer.

Summarize at the milestones: after a one-way door is decided, when the design is put up for approval, and when the plan is checked.

### 11.2 When the human can't answer now

If a one-way door, a conflict or the approval is pending and the human can't answer in this session, take a checkpoint: the open entries stay in the decisions record, and the state record lists them as waiting, with its status set to waiting for the human. Continue any work that doesn't depend on the answer, then stop at a clean point and say what is needed to continue. The next run resumes from the files (section 4.2).

### 11.3 Final report

When Design is finished, or when you stop, report:

1. Where the feature stands, and its next step.
2. The artifacts created or updated, with their versions and status: the design, the plan, the ADRs, the stack.
3. The one-way doors the human decided, and the other decisions they made during this run.
4. The review rounds, and how their findings were resolved.
5. The assumptions, open questions and risks the design carries.
6. Anything waiting for the human.
7. Anything you couldn't verify.

Distinguish what the human approved or decided from what you decided and recommend.
