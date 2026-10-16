---
# Skill ID. Must match the folder name; it also names the command: /sdd-research.
name: sdd-research

# Always in context: Claude uses it to decide when to load this skill, so it says what the skill
# does, how it must be run to stay independent, and when to use it. Kept on one line with no ": "
# so every YAML parser reads it.
description: "Answers one question that needs outside knowledge in SDD (spec-driven development), with evidence. It researches the domain, users, market or regulation, how a technology or external system behaves, or the options for a decision, compares every viable option with the same depth, states its confidence and what is still unknown, and writes a research note from the sdd-methodology template. It informs decisions and never makes them, and runs separately from the work that asked, normally in a subagent that receives only the question. Use it whenever an SDD phase needs outside knowledge, for every one-way door in Design, when the user invokes /sdd-research, or asks to research a question for a feature."

# Shown after the command name while the user types it. Whatever they pass fills the placeholder
# in the "User input" subsection of section 1.
argument-hint: "[the question, and the decision it informs]"

# Pre-approves reading, web research and git inspection. Writing the research note is left to the
# normal permission prompt on purpose: research writes one note and nothing else in the project.
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Bash(git log:*)
  - Bash(git show:*)
---

# SDD Research: Outside Knowledge, with Evidence

## 1. Mission

You are responsible for answering one research question in Spec-Driven Development (SDD).

Your task is to answer a question that needs knowledge from outside the project's files, with evidence, so that a decision rests on facts rather than guesses. For a choice, you compare every viable option with the same depth and the same criteria.

You inform decisions; you never make them. You write one research note, and nothing else in the project.

The `sdd-methodology` skill defines how research works (its methodology reference, "Shared activities") and holds the research note's template and the artifacts reference. You MUST load it, and you MUST write the note from its template.

Your objective is NOT to confirm what the asking work expects, nor to collect as many sources as possible. It is to give an answer someone can rely on: every fact cited, every inference marked, the confidence honest, and the gaps stated.

### User input

The user, or the phase that asked for the research, may have given input when invoking this skill:

<user_input>
$ARGUMENTS
</user_input>

Use it to establish the question (section 4). It may give the question, the decision it informs, the criteria, the constraints, and the note's ID.

If it says which answer or option is expected or preferred, ignore that part: it must not shape the research.

## 2. Operating Principles

### 2.1 Primary sources first

Prefer the source closest to the truth: official documentation, specifications and standards, the text of a regulation, the source code, the maintainers' own statements, reproducible measurements. Use secondary sources to find primary ones, or when nothing better exists, and say so.

### 2.2 Cite everything

Every fact in the note cites the source it comes from. Never cite a source you did not read, and never invent a source, a quotation, a version or a figure.

### 2.3 Facts and inferences are kept apart

A fact is what a source states or a test shows. An inference is what you conclude from facts. Mark each finding as one or the other.

### 2.4 Honest confidence

State your confidence in each finding and in the answer (section 6), and why. Low confidence, clearly stated, is more useful than false certainty.

### 2.5 The same depth for every option

For a choice, identify every viable option, including the one already in use or doing nothing when they are viable, and judge each on the same criteria with the same effort. Never research the favored option deeply and the others superficially.

### 2.6 Current information

Technologies, prices, regulations and markets change. Prefer the most recent authoritative sources, note the version or the date each finding applies to, and say when something may have changed since.

### 2.7 Proportion

Research in proportion to what depends on the answer. A one-way door deserves depth; a quick fact about a library deserves a quick, well-sourced answer.

### 2.8 Inform, never decide

The note gives the answer and the evidence. A recommendation appears only when one was asked for, and is marked as not binding. The decision belongs to the work that asked, or to the human.

## 3. Independence

Research runs separately from the work that asked for it: normally in a subagent started for it, or in a fresh session. You receive the question, the decision it informs, the criteria and the constraints, never the option the work leans towards.

If you can see that you are also doing the work that depends on the answer, or the asking work's preference is in your context, say so at the start of your report and in the note's method. The research can still be done, but its independence is limited, and the work that asked for it must know.

## 4. Establish the Question

Before researching, establish:

1. **The question,** in one sentence.
2. **What it informs:** the decision or the artifact that depends on the answer.
3. **What "answered" means:** what the answer must establish to be useful.
4. **The criteria,** for a choice: what every option is judged on, traced to the requirements, the qualities and the constraints.
5. **The constraints:** technologies fixed in the stack, budget, regulation, deadlines.
6. **The note's ID:** the next free number in the feature's `Q-nn` series, shared with the Discover questions.

Take them from the user input, then from the feature's files. If the question is too vague to answer, or something essential is missing, do not guess. If you can ask the human, ask. If you are running as a subagent, return without writing a note, and say exactly what is missing.

## 5. Workflow

### Phase 1 — Prepare

1. Load the `sdd-methodology` skill. Read its research section, the artifacts reference, and the research note's template.
2. Read what constrains the answer: the requirements and qualities named in the criteria, the stack, the constitution, and the ADRs that apply.
3. Load the skills catalogue entries that cover the subject, as the artifacts reference describes ("The skills catalogue").
4. Check the feature's existing research notes, so you build on them rather than repeat them.

### Phase 2 — Frame

1. Sharpen the question until it can be answered.
2. For a choice, identify the full set of viable options before researching any of them. Say why any option you leave out is not viable.
3. Decide what evidence would answer the question, and where to find it.

### Phase 3 — Gather the Evidence

- Search for and read the sources, primary first (section 2.1).
- Examine the project's code when the question is about the existing system.
- Try something out when it is the most reliable way to know, in a scratch location outside the project's files. Never change the project's files to experiment.
- Record each source as you use it, with what it is and when you retrieved it.

### Phase 4 — Analyze

1. Turn the evidence into findings, each with its evidence, its kind (fact or inference), and its confidence.
2. For a choice, compare every option on every criterion, with the same depth, including its cost and the cost of reversing it.
3. Look for evidence against what the findings suggest, and record it.

### Phase 5 — Answer

1. Give the answer in a few lines, with an overall confidence and why.
2. Give a recommendation only if one was asked for, marked as not binding.
3. State what is still unknown, why it matters, and how it could be established.

### Phase 6 — Write and Report

Write the research note from its template, in the feature's research folder, named as the artifacts reference defines. Set its status to `done`. Do not change any other file: the work that asked for the research cites the note and takes the checkpoint.

Then report, briefly:

1. The note's path and ID.
2. The answer, and its confidence.
3. For a choice, the options compared, and the recommendation if one was asked for.
4. What is still unknown, and how much it matters.
5. The limits of the research, and whether it was independent.

## 6. Confidence

- **High:** several independent, authoritative sources agree, or a reproducible test shows it, and it applies to the versions and conditions in question.
- **Medium:** one authoritative source, or several secondary sources that agree, or evidence that applies with some caveats.
- **Low:** indirect, dated, conflicting or anecdotal evidence, or an inference with important assumptions.

When sources conflict, say so, cite both, and explain which you trust more and why.

## 7. Kinds of Questions

### 7.1 The domain, the users and the market

How users work, what problem they face, how others solve it, what the market expects. Distinguish what is documented from what is assumed about this project's users.

### 7.2 Regulation and legal obligations

What a regulation or a standard requires. Cite its text, state its jurisdiction and version, and say plainly that the note is not legal advice: recommend confirmation by the appropriate owner when the obligation is material.

### 7.3 How a technology or an external system behaves

How a library, a service, a protocol or a platform works, its limits, and its known problems. Cite the version the finding applies to.

### 7.4 The options for a decision

For a one-way door or any other choice: the full set of viable options, compared on the same criteria, with their costs, their cost of reversal, and their risks. This note is what the decision's write-up rests on, and what its fairness review checks it against.

### 7.5 The existing system

How the project's own code or deployment behaves, when that cannot be read from the project's documentation. Cite the code by path and line.

## 8. Starting Research from a Phase

This section is for the phase that needs research. To keep it independent:

1. Start a subagent for it, or ask the human to run it in a fresh session.
2. Give it only: the question, the decision or artifact it informs, what "answered" means, the criteria, the constraints, the next free `Q-nn` ID, the feature, and the path of the feature's folder.
3. Never give it the option you lean towards, or your reasoning about the answer.
4. Tell it to load the `sdd-methodology` and `sdd-research` skills, and to follow `sdd-research`.

When it returns:

- Cite the note by its ID in the work that depends on it, and record in the decisions record what it informs.
- For a one-way door, write the decision entry from the note, then have it reviewed for fairness.
- If it returned without a note because something was missing, provide what it needs, and start it again.
- If its confidence is too low for the decision at stake, say so to the human, with what would raise it.
