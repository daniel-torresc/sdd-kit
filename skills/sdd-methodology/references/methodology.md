# The SDD methodology in detail

This document explains how a project is onboarded to SDD, and then how each piece of work travels through it, from the request to the merge: the phases, what each one aims for, what it starts from, what happens in it, what it produces, and when it is finished.

It describes the methodology, not how it is run. It doesn't say who carries out a phase, how the work is coordinated, or how a person is asked a question. Where each file lives, what it holds and how it is versioned is described in [artifacts.md](artifacts.md); the templates are in this skill's `templates/` folder.

## 1. Core concepts

### The specification is the contract

Every feature starts as a written specification: a **brief** (the problem, the users, what success looks like, the scope) and **requirements** (what the feature must do, as observable behaviour, each with acceptance criteria). Once the human approves them, they are the contract. The design, the plan, the code, the tests, the reviews and the documentation are all checked against them.

### The human decides what matters

The human decides:

- The intent: the answers to the Discover questions, and the approval of the brief, the requirements and the design.
- Hard-to-reverse choices (**one-way doors**).
- The order of the roadmap: what is built next, what waits, and what is dropped.
- Scope, risk, cost and legal matters.
- Anything that can't be resolved from the files and the evidence.
- The merge.

Everything else is decided as the work goes, inside the approved scope: how an artifact is structured, implementation details, a library within the chosen stack.

### Assumptions

When information is missing and the decision isn't the human's, the work doesn't stop. A sensible default is chosen and written down in the artifact as an assumption (`ASM-nn`), with its reason. The human sees the assumptions at the next approval and can overturn them.

### Files are the record

Everything of substance lives in files: the artifacts, the reviews, the questions and decisions, and where the feature stands. Nothing depends on a conversation being remembered, so the work can stop at any point and resume from the files.

Each feature keeps two running records next to its artifacts: its **state** (the phase, the step, what is waiting, what comes next, the tasks) and its **decisions** (every question, answer and decision about the feature, append-only). They are updated at every checkpoint, and committed on the feature branch. How they are kept is described in [artifacts.md](artifacts.md) (section 7).

### Traceability

Every item has an ID, and links point upward, from what was built to what it was built for:

```
requirement ◄── acceptance criterion ◄── task ◄── test, commit
     ▲
     └── component / interface
```

So at any point you can ask: is every requirement designed for, is every acceptance criterion delivered by a task, does every acceptance criterion have a test that passes? The IDs and how they link are defined in [artifacts.md](artifacts.md).

### Versions and staleness

The brief, the requirements, the design and the plan each carry a version and list the versions of the artifacts they were built from. When an artifact changes after it was reviewed or approved, its version goes up, and every artifact built on the older version becomes **stale**: it must be checked again, and either confirmed or revised in turn.

### Independent review

Every review judges the work against the sources it was built from (the requirements, the design, the decisions already made, the constitution), never against its author's explanation of it, and never edits what it reviews. Review and research are shared activities that any phase can call on; section 11 describes how they work.

## 2. Onboard: before the first feature

**Aim.** To establish, with the human, the project-wide context every feature builds on, so that no feature has to invent it. Onboarding runs once per project, before its first feature. The `sdd-onboarding` skill covers how it is done.

**Starts from** whatever already exists: the human's description of the project, any documents, diagrams or standards they have, and, in an existing project, the repository itself. A project may be:

- **Greenfield:** no meaningful implementation exists yet, though decisions, requirements or standards may.
- **Brownfield:** an existing system must be understood first.
- **Mixed:** for example a new service in an existing repository, with a chosen stack but no code.

### The foundational files

Onboarding produces the **foundational files**, each from its template:

- **The constitution:** the project's engineering principles, its non-negotiable constraints, and the practices everyone must follow.
- **The stack:** the technologies the project uses, and which of them the human has fixed.
- **The product description:** what the product is, why it exists, whom it serves, what it can do, its domain language and its business rules.
- **The architecture description:** how the system is structured, how its parts work together, and its known debt.
- **The skills catalogue:** the skills the project relies on as reference for its technologies, patterns, principles and practices, and the phases in which each applies.
- **The documentation catalogue:** every other document the project must keep current, such as those the company, a regulation or the team requires, and what makes each one need an update.
- **The roadmap:** the small increments the product will grow by, in the order the human has chosen (section 3).

Each file holds one kind of knowledge, and the same fact is never kept in two of them. The exact set of files is described in [artifacts.md](artifacts.md), and each has its template.

### The readiness verdict

Onboarding ends with one of three verdicts, based on what the files actually contain, not on whether they exist:

- **READY:** the files are coherent and complete enough to begin SDD. What remains open is documented and doesn't block.
- **READY WITH CAVEATS:** SDD can begin, but named limitations or open decisions need attention in the phases they affect.
- **NOT READY:** a material gap, contradiction or unresolved constraint prevents a reliable start. What must be resolved is stated.

Not every decision has to be made at onboarding. Requirements, detailed architecture and implementation choices belong to the features, unless the project can't start safely without them.

### Keeping them current

Onboarding happens once, but the foundational files live as long as the project. Features read them and use them as the project context. For example:

- Define starts from the next ready roadmap item, and reads the product description and the constitution.
- Design adds to the stack and the architecture decisions.
- Build follows the constitution's practices and the stack.
- Every phase loads the skills the catalogue lists for it and for the work at hand, and proposes new ones when they would help.
- Document brings the product and architecture descriptions, and every document in the documentation catalogue that the feature affects, in line with what was built, and closes the feature's roadmap item.

The foundational files can also be reviewed or updated deliberately at any time, outside any feature, with the same care as when they were first written. The roadmap is the one updated most often this way (section 3).

## 3. The roadmap: what to build next

**Aim.** To keep the product growing in small, independently deliverable increments, so that the next feature is always one that can be specified, built, verified and released on its own, and nothing a feature leaves for later is lost.

The roadmap is a foundational file. It holds the increments still to come, in the order the human has chosen, and those already delivered, split or dropped. Each item is a future feature: one item, one feature. The `sdd-roadmap` skill covers how it is kept.

### From coarse to ready

Only the items near the top of the roadmap need detail. An item further down can be a single outcome, even a large one. As it comes close to the top, it is refined and, when it is too large, split. Detail is added just in time, so the plan doesn't harden before the product has taught anything.

An item is **ready**, and can become the next feature, when:

- Its outcome is one sentence, for one user group, along one main flow, and can be shown working on its own.
- The product still works, and could be released, if work stops after it.
- It is a vertical slice through what users or callers observe, not a layer of the system.
- Every item it depends on is delivered.
- It needs at most one one-way door.
- None of the size signals below applies.

### Size signals

The method sets no fixed limits: how large a feature can be depends on the project, its team and its risk. A project that wants limits sets them as a practice in its constitution. Whatever the limits, an item is too large to be one feature when:

- Its outcome needs an "and": it delivers two things a user would value separately.
- It serves more than one user group, or more than one entry point or main flow.
- Parts of it could be released and used without the others.
- It needs more than one one-way door.
- Stopping halfway would leave the product unusable or unreleasable.
- It names a layer or a component ("the data model", "the API") rather than something a user or caller can observe.
- No one can say how it will be shown working once it is done.

The same signals apply later. When the requirements or the design show a feature growing beyond its item, it is split rather than built as one.

### Splitting an item

An item is split along what users observe, never along the layers of the system:

- **By workflow step:** one step of a longer journey at a time.
- **By user group or role.**
- **By rule or variation:** the main case first; other business rules, inputs or formats later.
- **Main flow first:** the less common cases later, as long as each slice handles its own failures safely.
- **Read before write,** or **manual before automated.**
- **Simple before complete:** one option, one channel or one integration first, more later.
- **Research first:** when an unknown is what makes the item large, an item that settles it comes first.

Each piece becomes an item of its own, with its own outcome, and the original is closed as split.

### The first items

In a greenfield project, the first item is usually a **walking skeleton**: the thinnest slice that delivers one small outcome a user can observe, end to end, through the real structure of the system and the real release path. It settles the foundational choices once, so the items after it only add behaviour.

In a brownfield project, the items come from the gaps between the current and the planned capabilities in the product description, from known debt whose repayment has an observable outcome, and from any existing backlog, brought in as candidates that point back to it rather than copied.

### Who changes it, and when

| When | What changes |
|---|---|
| Onboard | The first roadmap: the planned capabilities sliced into items, the first ones ready, the order approved by the human. |
| Any time, outside a feature | Items are refined, split, placed, reordered or dropped. The order, the placing and the dropping are the human's decisions. |
| Define | The feature starts from a ready item. A request that is not on the roadmap, or is too large, is checked and split first, and the remainder is added as candidates. |
| Design | A feature that turns out too large is split with the human, and what is taken out becomes candidates. |
| Document | The delivered item is closed, and the feature's follow-ups are added as candidates. |
| Release | A request, while the pull request is open, to defer something becomes a candidate. |

Changes made during a feature are made on its branch and reach main with its merge, so the human sees them in the pull request.

### Keeping it aligned

The roadmap plans the order of change; it never describes the product, the behaviour or the design. An item names, by ID, the capability it advances and the items it depends on. What it means in detail is in the brief and the requirements of the feature that builds it. Whether it is in progress is in that feature's state record, not in the roadmap. Once it is delivered, the product description shows the capability as built, and the roadmap shows which feature delivered it.

## 4. The phases

```
   ONBOARD            once per project: the foundational files and the first roadmap
      │
   ROADMAP            any time: refine, split and order the coming increments
      │               ✔ the order
   ┄┄┄│┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  every feature: one ready item
      ▼
   DEFINE ──────► DESIGN ──────► BUILD ──────► VERIFY ──────► DOCUMENT ──────► RELEASE
   what & why     how, in tasks   task by task  the whole      docs match      the human
                                                feature        what was built  merges
   ✔ brief        [✔ one-way door] ▲             │
   ✔ requirements ✔ design         │             │ blocking problems
                                   └─ fix tasks ◄┘
```

✔ = a human approval or decision. [✔ one-way door] = when there is a hard-to-reverse choice. Each feature delivers one roadmap item; Document closes it and adds the feature's follow-ups to the roadmap.

Onboarding runs once per project (section 2), before its first feature. After it, every feature goes through the phases in order, and each phase starts only when the one before it has finished.

### Starting a feature

A feature starts from a ready roadmap item, usually the first in the order: the human picks it, or brings a request that is checked against the roadmap first (section 5). It gets the next free number and a short name, its own branch from the latest main, and its own folder holding its state and decisions records. Then it enters Define.

## 5. Define: what to build and why

**Aim.** To agree with the human on the problem, who has it, what success looks like and exactly what the feature must do, before anyone thinks about how. Everything later is checked against what is agreed here.

**Starts from** the roadmap item, the human's request and, in an existing project, the product description. Nothing technical.

### Choosing the item

The feature delivers exactly one roadmap item. When the human names one, or asks what is next, it is the first ready item in the order. When the human brings a request instead, it is matched to an item; if there is none, it is checked against the readiness criteria (section 3). An item or request that is too large is split before the feature opens: the human chooses the piece to build, and the rest is added to the roadmap as candidates.

### Discover: the question loop

1. Work out what must be known to write the brief and the requirements.
2. Anything the files or outside research can answer is not asked.
3. Every other question whose answer would change the brief or the requirements goes to the human, each with why it matters and a recommended answer.
4. The answers are recorded word for word. The next round never asks again what was answered.

The loop has no fixed number of rounds. It ends when nothing important is left open, or when the human says to use the recommended answers, in which case they stand.

### The brief

Written from the item, the request and the answers: the problem, the users, how success is measured, the smallest valuable slice, and what is out of scope. The scope may narrow the item, never widen it; what Discover adds beyond it goes to the roadmap as a candidate, unless the human decides to change the item. What is still unknown and isn't the human's to decide is recorded as an assumption.

The human reviews and approves it. If they ask for changes, it is revised and put to them again.

### The requirements

Written from the approved brief:

- **Requirements** (`REQ-nn`), each with **acceptance criteria** (`AC-nn.m`) that anyone could check without asking.
- **Qualities** the feature needs (`NFR-nn`), each observable and measurable, with how it will be verified.

Everything is written as behaviour a user or caller can observe, including how users interact with what is built. Nothing technical. The human approves them the same way as the brief.

**Produces** the brief and the requirements, both approved, and the Discover questions and answers in the decisions record.

**Finished when** both the brief and the requirements are approved. From here on, they are the contract.

## 6. Design: how to build it

**Aim.** To decide how the feature will be built, make sure the approach holds up before any code is written, and break the work into tasks small enough to build and review one at a time.

**Starts from** the approved brief and requirements, the existing code, the foundational files, the existing architecture decisions (ADRs), and any research notes.

### The design and its task list

The design covers the components and interfaces, the data, the technology choices, service levels, capacity and failure modes, and the **task list**: each task with what it delivers, the acceptance criteria it covers, its technologies and its dependencies.

- Every requirement and quality is covered by some component or interface.
- Every acceptance criterion is covered by some task.
- Architecturally significant choices get an ADR, and new technologies are added to the stack.
- Technologies the human has fixed in the stack are never changed.

A requirement that can't be met, or that contradicts another, is not worked around: it is a problem in the requirements (section 12).

A feature that turns out too large to build as one, by the size signals of section 3, is not designed as one: the split is put to the human, the requirements are narrowed in Define, and what is taken out goes to the roadmap as candidates.

### One-way doors

Some choices are hard to reverse: the stack, the main datastore, hosting, identity, anything whose reversal would mean a rewrite, or that costs money. These are the human's to make:

1. Research (section 11) compares every viable option with the same depth.
2. The decision is written up: what is being decided, what it blocks, every option with its pros, cons, fit and cost of reversal, and a recommendation marked as not binding.
3. The write-up is reviewed for fairness (section 11): every viable option present, all judged evenly, and the recommendation following from the evidence.
4. The human chooses.
5. The choice gets an ADR and is recorded in the stack, and the design continues on that basis.

### The design review

The complete design is reviewed independently (section 11) against everything before it: the brief, the requirements, the research and the decisions already made. The review looks for gaps, contradictions, risky assumptions, unhandled failures, and requirements the design doesn't meet.

### The design approval

The human approves the design and its task list. They may approve it, ask for changes (the design is revised and put to them again), or decide to rethink the approach.

### The detailed plan

Once the design is approved, the plan says, for each task in the task list, how to approach it: what it delivers, the tasks it depends on, its technologies, the files and interfaces it touches, how it will be tested, and its risks. It contains no code.

The plan is then checked for consistency:

- Every acceptance criterion is delivered by some task.
- Every task names what it delivers, its technologies and its files.
- The dependencies have no cycles.

The plan has no review and no human approval of its own: it is the approved design made concrete.

**Produces** the approved design with its task list, any ADRs and stack changes, and the plan.

**Finished when** the design is approved and the plan passes its consistency check.

## 7. Build: one task at a time

**Aim.** To turn the plan into working code, one task at a time, each reviewed before it joins the feature, so the feature branch is always in a working state.

**Starts from** the approved design and the plan. A task can start once every task it depends on is merged. Independent tasks can run in parallel.

Each task goes through three steps:

1. **Implement.** On its own branch, created from the feature branch, the task is built together with the tests that show its acceptance criteria hold, following the constitution's practices and the stack. Each test names the acceptance criterion it proves. The task is done when its tests and the project's checks pass. It stays within the task: work the task doesn't ask for is reported, not done. Documentation the change affects is noted for Document.
2. **Review.** The change is reviewed independently (section 11) against the task, its acceptance criteria, the design and the constitution. Blocking findings are fixed and the change is reviewed again, until it is approved. If the plan turns out to be what's wrong, the task goes back to the plan.
3. **Merge.** The approved task branch is merged into the feature branch, and the full test suite runs. If anything fails, the merge is undone and the task goes back to be fixed.

If the design or the plan turns out not to work in practice, the build doesn't improvise: the task waits while the design or plan is corrected (section 12). A requirement that turns out wrong or untestable is a problem in the requirements.

**Produces** code and tests, merged task by task into the feature branch, and notes on the documentation affected.

**Finished when** every task in the plan is reviewed and merged into the feature branch, and the full test suite passes.

## 8. Verify: the whole feature

**Aim.** To confirm that the feature as a whole does what the requirements say, independently of how each task was built.

**Starts from** the feature branch with every task merged.

1. **Full check.** Every check the project has runs against the feature branch. The results are recorded as evidence, together with the traceability matrix showing which test proves each acceptance criterion.
2. **Feature review.** The whole feature, its full difference from main, is reviewed independently (section 11) against the requirements, the design and the evidence.

If the full check fails or the review finds blocking problems, each becomes a **fix task**, added to the task list and the plan. Fix tasks go through Build like any other task, and then Verify runs again from the start. A problem that lies in the requirements, not the code, is a problem in the requirements (section 12).

A quality that cannot be verified in the environment available is recorded as unverified, with the reason, and put to the human: they accept verifying it later, as a recorded risk, or provide what is needed. It never passes silently.

**Produces** the evidence (check results and the traceability matrix) and the feature review.

**Finished when** the full check passes, every acceptance criterion has a passing test, and the feature review has no blocking findings.

## 9. Document: the docs match what was built

**Aim.** To bring the project's documentation in line with what was built.

**Starts from** the documentation impact collected during Build, the documentation catalogue, the brief, the requirements, the design, the plan, the ADRs, the evidence and the code.

Three kinds of documentation are updated, to describe what was built, not what was planned:

- the foundational files that describe the product and the architecture;
- every document in the documentation catalogue whose update triggers match what the feature changed, keeping the structure each one requires;
- the rest of the project's own documentation that the documentation impact names.

It also brings the roadmap up to date: the item the feature delivered is closed, and the feature's follow-ups (deferred open questions, scope exclusions worth a later feature, work reported but not done, rejected minor findings worth revisiting) are added as candidates, so that they reach main with the feature and the human sees them in the pull request.

Where the code and the specification differ, the code is the truth, and the gap is reported as a problem in the specification. A required document that cannot be updated with the information available is put to the human, never skipped.

**Produces** updated documentation and an updated roadmap.

**Finished when** the documentation describes the feature as built, and the roadmap shows the item delivered and holds the follow-ups.

## 10. Release: the human merges

**Aim.** To hand the finished feature to the human for the merge, with everything they need to decide, and to close the feature once it is merged.

**Starts from** a feature that has passed Verify and finished Document, with nothing waiting for the human.

1. **Bring the feature up to date.** The feature branch is updated with the latest main, as the project's version-control practices say, and the full test suite and the checks run again. Conflicts or failures go back to Build as fix tasks; Release never fixes code.
2. **Release chores.** Whatever the project's practices or its documentation catalogue require for a release, such as a version bump, a changelog entry or release notes, is done. The method itself requires none.
3. **The pull request.** The feature branch is pushed and a draft pull request is opened into main. Its description says what the feature does; links to the brief, the requirements, the design and the evidence; lists the decisions the human made and the ADRs; states what the human accepts by merging (assumptions, open risks, unverified qualities, known failures); names the documentation updated and the roadmap item it delivers, with the follow-ups added; and says how to try it.
4. **While it is open.** A failing check on the pull request goes back for fix tasks, as in Verify. The human's comments on it are their input: a fix within the approved approach becomes a fix task, a change to the requirements goes back to Define, a request to defer something becomes a roadmap candidate, and a question is answered.
5. **Closing.** Once the human merges it, the feature is done, and its roadmap item, closed on the feature branch, is delivered on main. Its merged branch is cleaned up as the project's practices say.

Deploying is the project's own process, after the merge; it is not part of the method.

**Produces** the draft pull request, and, once it is merged, the closed feature.

**Finished when** the human merges the pull request. Merging into main is always the human's act. If the human closes it without merging, or wants something different instead, that is a decision for them to make, not a guess.

## 11. Shared activities: review and research

Review and research are not phases of their own. Every phase can call on them, and they follow the same rules wherever they happen. Both are carried out independently of the work they serve: separately from whoever produced it, and from the files alone.

### Review

**Aim.** To judge a piece of work against the sources it was built from, independently of its author, before anything is built on it.

**Where it happens:**

| Review | What is reviewed | Judged against | Phase |
|---|---|---|---|
| Design review | the complete design and its task list | the brief, the requirements, the research, the decisions already made, the foundational files | Design |
| Fairness review | the write-up of a one-way door | the research note, the requirements | Design |
| Task review | the change a task makes | the task in the plan, its acceptance criteria, the design, the constitution | Build |
| Feature review | the whole feature: its full difference from main | the requirements, the design, the evidence | Verify |

**Independence.** The review receives the work and its sources, never the author's explanation or reasoning. It judges against the sources, not against preferences, and a decision the human made is challenged only with new evidence. It never edits what it reviews.

**Findings.** Each finding has an ID, a severity, where it is, what is wrong, the evidence, and the recommended fix:

- **Blocking:** the work is wrong or unsafe and must change. A blocking finding without concrete evidence is minor.
- **Minor:** worth fixing, but doesn't hold the work up. Anything that adds scope is minor.

**Verdict and answers.** A review ends with a verdict: `approve` when nothing is blocking, `changes-required` otherwise. Every finding is answered, one answer per finding: fixed, which bumps the artifact's version, or rejected with a reason grounded in the requirements, a decision already made, or evidence. A disagreement that survives a revision goes to the human.

**Rounds.** After a revision, the next round first checks whether each earlier finding is resolved, then looks only for problems the revision introduced. If the rounds stop converging, with the same blocking findings coming back or new ones appearing each round, the review goes to the human, who decides how to proceed.

**Findings outside a review.** Any phase that finds a defect in an artifact it is not producing records it as a finding in a review file of its own, and keeps going if it can. The finding is answered the same way.

**Produces** a review file for each round, and the answers to its findings.

**Finished when** the verdict is `approve`, or the human decides how to proceed.

### Research

**Aim.** To answer a question that needs knowledge from outside the project's files, with evidence, so that a decision rests on facts rather than guesses.

**Where it happens:** in any phase. For example, the domain, the users, the market or a regulation during Discover; the options for a one-way door, or how a technology behaves, during Design; how a library behaves during Build.

**Independence.** Research informs a decision; it never makes one. For a choice, every viable option is compared with the same depth and the same criteria, whichever option the work leans towards. Facts are cited, inferences are marked as such, and confidence is stated.

**Steps:**

1. State the question, the decision it informs, and what "answered" means.
2. Gather the evidence: sources, the existing code, anything tried out.
3. Record each finding with its confidence.
4. For a choice, compare every viable option on its fit with the requirements and qualities, the evidence, its cost, the cost of reversing it, and its risks.
5. Give the answer with an overall confidence, and a recommendation only when one was asked for, marked as such.
6. State what is still unknown, and how it could be established.

**Produces** a research note, which the work that asked for it cites.

**Finished when** the question is answered with a stated confidence, or what cannot be established is stated, with how it could be.

## 12. What can happen at any point

### A problem in an artifact

A defect found in an artifact, in a review or during other work, is recorded as a finding in a review file (section 11), and the work goes on if it can. The artifact is then corrected, or the finding is rejected with a reason, one answer per finding. If the disagreement survives, the human decides.

### A change to an approved artifact

Fixing a problem, or the human changing their mind, can change an artifact that was already approved. It is revised and its version goes up, so every artifact built on the older version becomes stale and is checked again.

- A fix within what the human approved needs no new approval.
- **A change to the scope, the intent or the approved approach goes back to the human for approval** before the work built on it continues.

### Outside knowledge

Any question needing outside knowledge (the market, regulation, the domain, how a library behaves, the options for a technology decision) can be researched at any point, as section 11 describes. Research informs a decision; it never makes one.

### A question only the human can answer

Any decision that belongs to the human (section 1) is put to them with a recommended answer, and their answer is recorded in the decisions record. Work that doesn't depend on the answer can go on in the meantime.

## 13. Reference

### Every step in order

| Phase           | Step                       | Starts from                                                   | Produces                                          | Ends with                                            |
|-----------------|----------------------------|---------------------------------------------------------------|---------------------------------------------------|------------------------------------------------------|
| Onboard (once)  | Foundational files         | the human's description, existing documents, the repository   | the foundational files, the first roadmap, readiness verdict | READY, or READY WITH CAVEATS                 |
| Roadmap (any time) | Refine, split, order     | the product description, the roadmap, delivered features      | ready items, in order                             | **human decides the order**                          |
| Define          | Choose the item            | the roadmap, the request                                      | the item, split first if too large                | one ready item                                       |
|                 | Discover                   | the request, the product description, earlier answers         | questions and answers in the decisions record     | nothing important open, or "use the recommendations" |
|                 | Brief                      | the request, the answers                                      | brief                                             | **human approval**                                   |
|                 | Requirements               | the approved brief                                            | requirements                                      | **human approval**                                   |
| Design          | Design and task list       | brief, requirements, code, foundational files, ADRs, research | design, ADRs, stack changes                       | a complete design                                    |
|                 | One-way door (when needed) | the decision, the requirements                                | research note, decision write-up, fairness review | **human decision**, then an ADR                      |
|                 | Design review              | the design and everything before it                           | review file                                       | approval                                             |
|                 | Design approval            | the design, its task list, open findings                      | —                                                 | **human approval**                                   |
|                 | Plan                       | the approved design                                           | plan                                              | consistency check clean                              |
| Build, per task | Implement                  | the task, its criteria, design, constitution, stack, code     | code and tests on the task branch                 | tests and checks pass                                |
|                 | Review                     | the change, the task, its criteria, design                    | review file                                       | approval                                             |
|                 | Merge                      | the approved task branch                                      | merge into the feature branch                     | full suite passes                                    |
| Verify          | Full check                 | the feature branch                                            | evidence, traceability matrix                     | —                                                    |
|                 | Feature review             | the whole feature, the evidence                               | review file                                       | no blocking findings, or fix tasks back to Build     |
| Document        | Documentation              | everything that was built, the documentation notes            | updated documentation and roadmap                 | docs match what was built, item closed               |
| Release         | Update and release chores  | the documented feature branch, the latest main                | updated branch, version or changelog if required  | full suite passes                                    |
|                 | Pull request               | the updated feature branch                                    | draft pull request                                | **the human merges**                                 |
|                 | Close                      | the merged pull request                                       | the feature done                                  | feature closed                                       |
