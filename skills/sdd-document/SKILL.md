---
# Skill ID. Must match the folder name; it also names the command: /sdd-document.
name: sdd-document

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# produces and when to use it. It names no file path on purpose: where each artifact lives is
# defined by the sdd-methodology skill and may change. Kept on one line with no ": " so every
# YAML parser reads it.
description: "Runs the Document phase of SDD (spec-driven development) for one verified feature. It brings the project's documentation in line with what was built, not what was planned. It updates the product and architecture descriptions, every document in the project's documentation catalogue that the feature affects (company, regulatory, contractual or team documents, in the structure each one requires), and the rest of the documentation the feature's documentation impact names. Where the code and the specification differ, the code is the truth and the gap is reported. Use when the user invokes /sdd-document, or asks to document a feature, or to update the project's documentation after a feature is verified. Not for writing code or changing requirements."

# Shown after the command name while the user types it. Whatever they pass fills the
# placeholder in the "User input" subsection of section 1, which says how the whole run applies it.
argument-hint: "[the feature to document]"

# Pre-approves the reading and git inspection this phase does often.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(git status:*)
  - Bash(git log:*)
  - Bash(git diff:*)
  - Bash(git show:*)
---

# SDD Document: The Docs Match What Was Built

## 1. Mission

You are responsible for running the Document phase of Spec-Driven Development (SDD) for one feature.

Your task is to bring the project's documentation in line with what was built, so that anyone reading it, people or later SDD work, finds the product and the system as they really are.

Document updates three kinds of documentation:

- **The foundational files that describe the product and the architecture.**
- **Every document in the documentation catalogue** whose update triggers match what the feature changed: the documents the company, a regulation, a contract or the team requires, each in the structure it must keep.
- **The rest of the project's own documentation** that the feature's documentation impact names.

The `sdd-methodology` skill defines where each artifact lives, the documentation catalogue and how it is used, and how the running records are kept (its artifacts reference), and how Document fits in the whole method (its methodology reference). You MUST load it.

Your objective is NOT to write as much documentation as possible. It is to make every document the feature affects accurate, complete for its readers, and consistent with the others, and to leave none of the required ones behind.

Your success is measured by documentation that describes the feature exactly as built, with every required document updated, and every gap between the code and the specification reported.

### User input

The user may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Apply it throughout the whole workflow:

- **It is an explicit user statement.** It ranks above your inferences, but never above what the code shows.
- **It can name the feature,** point to a document that should be updated, or supply information a required document needs. Use it; every rule of this skill still applies.
- **It is context, not a decision.** It never answers a decision entry that is waiting for the human unless it explicitly does so.
- **If it is empty,** take the feature from the current branch and its state record, and ask if it cannot be established.

## 2. Operating Principles

### 2.1 Document what was built

Describe the product and the system as they are after the feature, not as they were planned. Where the code and the specification differ, the code is the truth for the documentation, and the gap is reported (section 7.1).

### 2.2 The required structure wins

A document that follows a company template, a standard, or a skill keeps that structure. Fill it in; never reorganize it, rename its sections, or drop parts it requires.

### 2.3 One fact, one place

Each kind of information has one authoritative document, as each template's source-of-truth section says. Update it there, and reference it from elsewhere, rather than copying it into several documents.

### 2.4 Write for the reader

Each document has its readers: users, operators, developers, auditors. Write what they need to know, in their language, at their level of detail. Leave out what they don't.

### 2.5 Change only documentation

Document never changes the code, the tests, the requirements, the design or the plan. A problem in them is reported, never fixed here.

### 2.6 Nothing required is skipped

Every catalogue entry the feature triggers is updated, or put to the human with what is missing. None is left behind silently.

### 2.7 The record outlives the session

Everything goes into the feature's files and the project's documentation, committed at every checkpoint. The `sdd-methodology` skill's artifacts reference ("Running records") defines how they are resumed from, how a checkpoint is taken, and how decisions are written. You MUST follow it.

## 3. Required Context

### 3.1 What Document reads

- **The documentation impact** recorded in the feature's decisions record during Build.
- **The documentation catalogue:** every active entry, with its purpose, its required structure, and what makes it need an update.
- **The product and architecture descriptions,** and their templates.
- **What was built:** the brief, the requirements, the design, the plan, the ADRs, the evidence, and the code on the feature branch, in particular its full difference from main.
- **The constitution:** any documentation practices it sets.
- **The skills catalogue:** load the approved skills that apply to Document, and the skills the catalogue's entries name as their format, as the artifacts reference describes ("The skills catalogue").

### 3.2 Verify must be finished

Document starts only when Verify has passed: the evidence's result is `pass`, and the feature review has no blocking findings.

If it hasn't, tell the human what is missing and recommend finishing Verify first (the `sdd-verify` skill). Do not document a feature that may still change.

## 4. Establish the Starting Point

Determine which situation applies, from the user input and the feature's state record.

### 4.1 A feature ready for Document

Verify has passed, and the state record moves the feature to Document. Run the whole phase.

### 4.2 A Document in progress

The state record shows the feature in Document. Resume as the artifacts reference describes ("Running records"): read the list of documents to update from the records, check which are done, and continue with the rest. Collect the answers to any decision entry that was waiting.

## 5. Records and Checkpoints

Take a checkpoint, as the artifacts reference describes, at the end of every phase below, whenever something is put to the human, and before any stop.

Record in the decisions record:

- the documents updated, and the ones that could not be;
- every required document put to the human, and their answer;
- every gap between the code and the specification, and where it was reported.

## 6. Workflow

The phases below are the minimum responsibilities of Document, not a rigid script.

### Starting the workflow

Explain the process briefly to the human, then begin with Phase 1.

Start from the user input (section 1, "User input") and anything else the human has already said, rather than asking them to repeat it.

### Phase 1 — Preparation

Objective:
Know what was built and what documentation it affects, before writing anything.

Activities:

1. Load the `sdd-methodology` skill, and read the artifacts reference, its documentation catalogue section, and the Document section of the methodology reference.
2. Check that Verify has passed (section 3.2).
3. Read the context, and load the skills that apply (section 3.1).
4. Determine the starting point (section 4).

Completion criteria:

- Verify has passed.
- What the feature changed is understood from the code, not only from the specification.

### Phase 2 — What to Update

Objective:
Establish the complete list of documents the feature affects.

Build the list from:

1. **The product description:** what the feature changes in the product's capabilities, users, domain concepts, business rules or objectives.
2. **The architecture description:** what the feature changes in the system's components, interfaces, data, cross-cutting concerns, deployment, decisions, or known debt.
3. **The documentation catalogue:** every active entry whose `update-when` matches what the feature changed. When in doubt whether a trigger matches, include the entry and say why.
4. **The documentation impact:** every document the feature's tasks named.
5. **The README and the rest of the project's documentation:** anything else a reader would now find wrong or missing.

For each document, note what must change, and why.

Completion criteria:

- Every document the feature affects is on the list, with what must change.
- Every catalogue entry is either on the list or judged not triggered by the feature.

### Phase 3 — Update the Documents

Objective:
Bring every document on the list in line with what was built.

For each document:

1. Read it as it is now.
2. Update it to describe what was built, following its template, its required format, or its skill. Keep everything that is still valid.
3. Use the product's domain language, and reference the authoritative document for anything kept elsewhere.
4. When the code and the specification differ, document the code, and report the gap (section 7.1).
5. When the information a required document needs is not available, do not invent it: open a decision entry for the human with what is missing, and continue with the other documents.

For the product and architecture descriptions, update their version, as their templates' maintenance guidelines say.

Completion criteria:

- Every document on the list is updated, or put to the human with what is missing.

### Phase 4 — Check the Documentation

Objective:
Make sure the documentation is accurate, complete and consistent before the feature is released.

Check it as section 9 describes, and fix what the check finds.

Completion criteria:

- The documentation passes the checks in section 9.

### Phase 5 — Close Document

Objective:
Leave the feature ready for Release.

Activities:

1. Take the last checkpoint of the phase: the state record moves the feature to Release, and says that the next run opens the pull request. If a required document is still waiting for the human, the status says so, and the feature waits.
2. Report the outcome (section 10.3).

Completion criteria:

- Every document the feature affects is updated, or waiting for the human with what is missing.
- The state record and the decisions record reflect where the feature stands.

## 7. Problems

### 7.1 A gap between the code and the specification

When the code does something the requirements or the design don't say, or doesn't do something they say:

1. Document what the code does.
2. Record the gap as a finding in a findings file, against the specification, with the evidence.
3. Open a decision entry for the human: the specification is revised to match the code, or the code is fixed through a fix task.

A gap Verify should have caught is reported the same way, and noted as such.

### 7.2 A required document that doesn't exist

When a catalogue entry names a document that doesn't exist yet, create it from its required format if the format is known. If it isn't, put it to the human.

### 7.3 A required document that cannot be completed

When a document needs information only the human or another team has (an owner, an approval reference, an operational contact), never invent it. Put it to the human with what is missing, and continue with the rest.

### 7.4 A catalogue that is out of date

When the documentation catalogue lists a document that moved or no longer exists, or misses one that clearly must be kept, propose the change to the human through a decision entry. Never change the catalogue without their approval.

## 8. Change Management

- Document changes the project's documentation, the product and architecture descriptions, and the running records. It never changes the code, the tests, the requirements, the design, the plan, or the documentation catalogue itself without the human's approval.
- Preserve the valid content of every document you update; never delete what is still true.
- Commit at every checkpoint, following the project's version-control practices. Never commit to main, and do not push or merge unless the human asks.
- Do not claim that a document was updated or checked unless it actually was.

## 9. Quality Checks

- **Accurate:** every statement about the feature matches the code on the feature branch.
- **As built:** nothing planned and not built is described as existing.
- **Complete:** every document on the list is updated, and every triggered catalogue entry is covered.
- **Structured:** every required document keeps its template, standard, or format.
- **Consistent:** the same fact is not stated differently in two documents, and each is kept in its authoritative place.
- **Working references:** links, paths, commands and examples point to what exists and work as written.
- **For its readers:** each document says what its readers need, and nothing they don't.

## 10. Interaction Style

### 10.1 Collaboration

Be concise and transparent. Document asks the human little: only for information a required document needs, decisions about gaps between the code and the specification, and changes to the catalogue.

### 10.2 When the human can't answer now

If a decision is pending and the human can't answer in this session, take a checkpoint: the open entries stay in the decisions record, and the state record lists them as waiting. Update every document that doesn't depend on the answer, then stop at a clean point and say what is needed to continue. The next run resumes from the files (section 4.2).

### 10.3 Final report

When Document is finished, or when you stop, report:

1. Where the feature stands, and its next step.
2. Every document updated, and what changed in each.
3. Every triggered catalogue entry, and its outcome.
4. Every gap between the code and the specification, and where it was reported.
5. Anything waiting for the human, and what is missing.
6. Anything you couldn't verify.
