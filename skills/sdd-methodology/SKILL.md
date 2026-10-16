---
# Skill ID. Must match the folder name.
name: sdd-methodology

# Always in context: Claude uses it to decide when to load this skill. It says that the skill
# explains the methodology and its files (not how to run it), and the moments that need them.
# Kept on one line with no ": " so every YAML parser reads it.
description: "Explains SDD (spec-driven development), the methodology, and the files it produces. It covers its principles, the one-time onboarding and the six phases of every feature (Define, Design, Build, Verify, Document, Release), what each aims for, starts from, produces and needs before it is finished, where the human approves, the shared review and research activities, and what happens when a problem or change appears. It also defines the project layout, every SDD file and its template, versions and staleness, and the IDs that link requirements to design, tasks and tests. Use it whenever you need to understand SDD or where a piece of work sits in it, before working on any SDD phase, whenever you create or fill an SDD file from its template, need to know where a file goes or which file holds something, read or assign an ID, or when the user asks how SDD works."

# Reference knowledge, not an action: hide it from the / menu. Claude can still load it on its
# own whenever the description matches.
user-invocable: false
---

# SDD methodology

SDD (spec-driven development) builds software from written specifications. Every feature starts as a specification the human approves, and everything built afterwards (the design, the plan, the code, the tests, the documentation) is traced back to it and checked against it.

This skill explains the methodology: its principles, its phases, and the files a project following it holds. The templates for those files are in this skill's `templates/` folder.

## Principles

1. **Specify before building.** What is needed and why is agreed before deciding how, and how is agreed before anything is built.
2. **The approved specification is the source of truth.** Everything produced afterwards derives from it and is judged against it.
3. **The human decides what matters.** Intent, scope, risk, cost, legal matters, and choices that are hard to reverse belong to the human. Everything else is decided along the way, within what was approved.
4. **Make the implicit explicit.** Assumptions, decisions, open questions and their reasons are written down where they can be reviewed and overturned. A gap is filled with a recorded assumption rather than a silent guess.
5. **Everything is traceable.** Every piece of work links back to the need it serves, and every need links forward to the evidence that it is met.
6. **Evidence over assertion.** Work is finished when checks and reviews show that it meets its specification, not when someone says it is done.
7. **Review is independent.** Work is judged against its sources, never against its author's explanation of it.
8. **Changes propagate.** When something changes, everything derived from it is checked again. A change to intent, scope or the approved approach goes back to the human.
9. **The record outlives the work session.** All state lives in versioned artifacts, not in memory or conversation, so work can pause, resume or change hands at any point.
10. **Small, verifiable steps.** Work is split into pieces small enough to build, review and verify one at a time, and the system keeps working after each one.

## The phases

```
   ONBOARD            once per project: the foundational files
      │
   ┄┄┄│┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄  every feature
      ▼
   DEFINE ──────► DESIGN ──────► BUILD ──────► VERIFY ──────► DOCUMENT ──────► RELEASE
   what & why     how, in tasks   task by task  the whole      docs match      the human
                                                feature        what was built  merges
   ✔ brief        [✔ one-way door] ▲             │
   ✔ requirements ✔ design         │             │ blocking problems
                                   └─ fix tasks ◄┘
```

✔ = a human approval. [✔ one-way door] = when there is a hard-to-reverse choice.

**Onboard** runs once per project, before its first feature. It establishes the **foundational files** for working with SDD: the project-wide context every feature reads and keeps current, namely its engineering principles and practices, its technology stack, what the product is, how the system is built, and the skills the project relies on.

After it, every feature goes through the phases in order, and each phase starts only when the one before it has finished.

| Phase        | Aims to                                                                                                               | Produces                                                     | Finished when                                                                               |
|--------------|-----------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| **Onboard**  | establish, with the human, the project-wide context features build on, once per project                               | the foundational files, and a readiness verdict              | the files pass validation and the project is ready for SDD, or ready with stated caveats    |
| **Define**   | agree on the problem, the users, what success looks like and what the feature must do, before anyone thinks about how | the brief and the requirements, with acceptance criteria     | the human approves both                                                                     |
| **Design**   | decide how to build it, prove the approach before any code, and split the work into tasks                             | the design with its task list, ADRs, stack changes, the plan | the human approves the design and the plan passes its consistency check                     |
| **Build**    | turn the plan into working code, one reviewed task at a time                                                          | code and tests, each task reviewed and integrated            | every task is reviewed and integrated, and the full test suite passes                       |
| **Verify**   | confirm the whole feature does what the requirements say                                                              | the evidence and a feature review                            | all checks pass, every acceptance criterion has a passing test, no blocking findings        |
| **Document** | bring the documentation in line with what was built                                                                   | updated documentation                                        | the documentation describes the feature as built                                            |
| **Release**  | hand the feature to the human                                                                                         | a draft pull request                                         | the human merges it                                                                         |

There are only two ways back. Blocking problems found in Verify become fix tasks that go through Build again. An approved artifact that turns out to be wrong is corrected at any point, and everything built on it is re-checked.

## Shared activities

Two activities are not phases: any phase calls on them, and they follow the same rules wherever they happen. Both are carried out independently of the work they serve, from the files alone.

| Activity     | Aims to                                                                                   | Used in                                                                                     | Produces                                         |
|--------------|-------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|--------------------------------------------------|
| **Review**   | judge a piece of work against the sources it was built from, never its author's reasoning | the design review and the fairness review of a one-way door (Design), each task (Build), the whole feature (Verify) | a review file with findings and a verdict, and the answers to each finding |
| **Research** | answer a question that needs outside knowledge, with evidence and a stated confidence     | any phase: the domain and regulation in Define, the options for a one-way door in Design, how a technology behaves | a research note that the work cites              |

## Project layout

```
<project>/
├── .sdd/                          the foundational files: the project as a whole
│   ├── constitution.md            principles, non-negotiable constraints, practices
│   ├── stack.yaml                 the technology stack; the human's fixed choices
│   ├── product.md                 what the product is, for whom, what it can do
│   ├── architecture.md            how the system is built, its conventions and debt
│   └── skills.yaml                the skills the project relies on, and when each applies
├── docs/
│   ├── adr/ADR-NNNN-<slug>.md     one architecture decision each
│   └── …                          the project's own documentation
├── README.md
└── specs/
    └── NNN-<slug>/                one folder per feature (feature ID F<NNN>)
        ├── state.yaml             where the feature stands
        ├── decisions.md           every question, answer and decision
        ├── brief.md               the problem, users, outcome, success, scope
        ├── requirements.md        the behaviour, acceptance criteria, qualities
        ├── research/              one note per researched question
        ├── design.md              how it is built, and the task list
        ├── plan.md                how to approach each task
        ├── reviews/               one file per review round, and the answers
        └── evidence/              the full check's results and the traceability matrix
```

Every file that has a template starts from it. Each brief, requirements, design and plan carries a version and the versions it was built from, so a change makes everything built on the older version stale. Every item has an ID, and IDs link what was built to what it was built for.

## In detail

[references/methodology.md](references/methodology.md) explains the method in full:

- **The core concepts:** the contract, decisions and assumptions, the record, traceability, versions and staleness, and how reviews work.
- **Onboarding:** what the foundational files hold, the readiness verdict, and how features keep them current.
- **Each phase:** its aim, what it starts from, its steps in order, what it produces, and when it is finished.
- **The shared activities:** how a review works (findings, verdicts, answers, rounds) and how research is done.
- **What can happen at any point:** problems, changes to approved artifacts, outside knowledge, and questions for the human.
- **A reference table** of every step.

[references/artifacts.md](references/artifacts.md) explains the files in full:

- **The layout and the template rules.**
- **Every project and feature file:** what it is, its template, when it is created, what it is built from.
- **Frontmatter, versions and staleness.**
- **Every ID,** where it is defined, and how IDs link.
- **The skills catalogue:** which skills to load in each phase, and how new ones are added.
- **The running records:** how a feature is resumed, how a checkpoint is taken, and how decisions and approvals are recorded.
