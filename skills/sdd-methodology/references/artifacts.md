# The SDD artifacts in detail

This document describes every file an SDD project holds: where it lives, what it is for, which template it starts from, what it is built from, in which phase it is created and updated, how it is versioned, and the IDs it uses.

The templates are in this skill's `templates/` folder. When and why each file is produced is explained in [methodology.md](methodology.md).

## 1. Layout

```
<project>/
├── .sdd/                          the foundational files: the project as a whole
│   ├── constitution.md
│   ├── stack.yaml
│   ├── product.md
│   ├── architecture.md
│   ├── skills.yaml
│   ├── documentation.yaml
│   └── roadmap.md
├── docs/
│   ├── adr/ADR-NNNN-<slug>.md     one architecture decision each
│   └── …                          the project's own documentation
├── README.md
└── specs/
    └── NNN-<slug>/                one folder per feature; NNN gives the feature ID F<NNN>
        ├── state.yaml
        ├── decisions.md
        ├── brief.md
        ├── requirements.md
        ├── research/Q-nn-<slug>.md
        ├── design.md
        ├── plan.md
        ├── reviews/
        └── evidence/
```

The feature folder's name starts with its number: `specs/003-password-reset/` is feature `F003`.

## 2. Templates

Every file that has a template starts from it.

- **Read the template before creating the file.** Its guidance says what each section must contain.
- **Keep its structure:** its frontmatter fields, its headings and their order. Fill sections in; don't rename them, and don't add sections the template doesn't define.
- **Replace every placeholder** (`<…>`, `[…]`), or say explicitly that it is still open.
- **A template that doesn't fit is a problem to report,** not something to work around silently.

## 3. Project files

These describe the project as a whole and outlive any single feature. The seven files in `.sdd/` are the **foundational files**, established at onboarding. Every one of them is required.

| File                                 | What it is                                                                                                                                | Template          | Created | Read or updated by                                              |
|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------|---------|-----------------------------------------------------------------|
| `.sdd/constitution.md`               | the project's engineering principles, non-negotiable constraints, and the practices everyone must follow                                  | `constitution.md` | Onboard | read by every phase; changed only deliberately, with the human  |
| `.sdd/stack.yaml`                    | the project's technology stack, its commands, and the tools its work relies on (issue tracker, docs space, …); entries marked `fixed: true` are the human's constraints and never change without the human | `stack.yaml`      | Onboard | Design adds or updates entries                                  |
| `.sdd/product.md`                    | what the product is, why it exists, whom it serves, what it can do, its domain language and its business rules                            | `product.md`      | Onboard | Define reads it; Document updates it                            |
| `.sdd/architecture.md`               | how the system is structured, how its parts work together, its conventions and known debt                                                 | `architecture.md` | Onboard | Design reads it; Document updates it                            |
| `.sdd/skills.yaml`                   | the skills the project relies on as reference for its technologies, patterns, principles and practices, and when each applies             | `skills.yaml`     | Onboard | read by every phase; entries added once the human approves them |
| `.sdd/documentation.yaml`            | every document the project must keep current beyond the foundational files (company, regulatory, contractual or team documents) and when each must be updated (section 10) | `documentation.yaml` | Onboard | Document updates the documents it lists; entries added once the human approves them |
| `.sdd/roadmap.md`                    | the small increments the product will grow by, in the order the human has chosen, and those delivered, split or dropped (section 11) | `roadmap.md` | Onboard | Define reads it and adds candidates; Document closes the delivered item and adds follow-ups; reordered, placed or dropped only by the human |
| `docs/adr/ADR-NNNN-<slug>.md`        | one architecturally significant decision: its context, the options, the choice and its consequences                                       | `adr.md`          | Design  | superseded by a later ADR, never rewritten                      |
| `README.md`, `docs/` (except `adr/`) | the project's own documentation for users and developers                                                                                  | none              | —       | Document updates it                                             |

Each foundational file holds one kind of knowledge, and the same fact is never kept in two of them. Where a template has a **Source of Truth** section, it says which file owns which kind of information.

## 4. Feature files

These live in the feature's folder, `specs/NNN-<slug>/`. "Built from" names the files a file is derived from: when one of them changes, this file may be stale (section 5).

| File                                | What it is                                                                                                                                                                                                 | Template          | Created in                              | Built from                                |
|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|-----------------------------------------|-------------------------------------------|
| `state.yaml`                        | where the feature stands: the roadmap item it delivers, phase, step, status, what the next run must do, what waits, tasks, stale files, history (section 7)                                                                              | `state.yaml`      | feature start; updated after every step | —                                         |
| `decisions.md`                      | every question, answer and decision about the feature: the human's decisions and approvals, the Discover questions and answers, the choices made along the way, and the documentation affected (section 7) | `decisions.md`    | feature start; added to throughout      | —                                         |
| `brief.md`                          | the problem, the users, the desired outcome, the success criteria, the scope and non-goals, constraints, assumptions, open questions and risks                                                             | `brief.md`        | Define                                  | the request and the Discover answers      |
| `requirements.md`                   | the requirements and their acceptance criteria, the qualities the feature needs, and the exclusions, as observable behaviour                                                                               | `requirements.md` | Define                                  | `brief.md`                                |
| `research/Q-nn-<slug>.md`           | the answer to one question, with evidence, confidence and sources; for a choice, every viable option compared                                                                                              | `research.md`     | any phase                               | —                                         |
| `design.md`                         | how the feature is built: components, interfaces, data, technologies, qualities, failure modes, and the task list                                                                                          | `design.md`       | Design                                  | `brief.md`, `requirements.md`             |
| `plan.md`                           | how to approach each task: what it delivers, its dependencies, technologies and files, how it is checked, its risks                                                                                        | `plan.md`         | Design                                  | `design.md`, `requirements.md`            |
| `reviews/<kind>[-<target>]-r<n>.md` | one review round: the findings and the verdict; for example `design-r1.md`, `task-T-03-r2.md`, `fairness-H-02-r1.md`, `feature-r1.md`                                                                      | `review.md`       | Design, Build, Verify                   | the file under review                     |
| `reviews/findings-<n>.md`           | findings about an artifact, raised outside a review                                                                                                                                                        | `review.md`       | any phase                               | —                                         |
| `reviews/<review-file>-answers.md`  | the answer to each finding: `R1-03: fixed (design.md@3)` or `R1-03: rejected: <reason>`, one line per finding                                                                                              | none              | after each review                       | the review                                |
| `evidence/README.md`                | one Verify run: the checks and their results, the traceability matrix (which test proves each acceptance criterion), how each quality was verified, and what failed                                        | `evidence.md`     | Verify                                  | `requirements.md`, `design.md`, `plan.md` |

## 5. Frontmatter, versions and staleness

The brief, the requirements, the design and the plan carry this frontmatter (each template shows its exact fields):

| Field      | Meaning                                                                     |
|------------|-----------------------------------------------------------------------------|
| `artifact` | which artifact this is                                                      |
| `feature`  | the feature ID, for example `F003`                                          |
| `status`   | `draft`, `approved` or `superseded`; the plan, which has no approval, uses `checked` instead of `approved` |
| `version`  | an integer, bumped on every change after the first review or approval       |
| `upstream` | the version of each file this version was built from, as `<file>@<version>` |

The foundational files carry a `version` and a `status` of `draft`, `active` or `superseded`. ADRs, research notes and reviews have their own fields, shown in their templates. The decisions record carries only its `artifact` and `feature`: it is append-only, so it has no version.

When a file's `version` is higher than the one another file lists for it in `upstream`, that other file is **stale**. It is checked again: if it still holds, its `upstream` entry is bumped to the current version; otherwise it is revised, which bumps its own version in turn.

Each `upstream` entry names a file that exists in the feature folder.

## 6. IDs

IDs are local to a feature, except `ADR`, `CAP` and `RM`, which are numbered across the whole project. Across features, prefix the feature: `F003:REQ-02`.

An ID is defined by a heading that starts with it, such as `### REQ-02: <title>`. IDs are never reused or renumbered: an item that no longer applies keeps its heading, marked `[withdrawn]`, and is never deleted.

`ASM`, `OQ` and `RISK` IDs form one series per feature, shared by every file that uses them.

| ID               | Meaning                                                                     | Defined in                                               |
|------------------|-----------------------------------------------------------------------------|----------------------------------------------------------|
| `SC-nn`          | success criterion, with its measurement and target                          | `brief.md`                                               |
| `CON-nn`         | constraint the solution must respect, with its source                       | `brief.md`                                               |
| `REF-nn`         | reference supporting the brief                                              | `brief.md`                                               |
| `REQ-nn`         | requirement                                                                 | `requirements.md`                                        |
| `AC-nn.m`        | acceptance criterion; `nn` is the number of its requirement                 | `requirements.md`                                        |
| `NFR-nn`         | a quality the feature needs, observable and measurable, with a Verify field | `requirements.md`                                        |
| `C-nn` / `IF-nn` | component / interface                                                       | `design.md`                                              |
| `T-nn`           | task                                                                        | `plan.md` (listed in the task-list table of `design.md`) |
| `Q-nn`           | Discover question, or research note                                         | `decisions.md`, `research/`                              |
| `OQ-nn`          | open question carried by an artifact, with its proposed default             | `brief.md`, `requirements.md`                            |
| `H-nn`           | decision waiting for the human, including one-way-door decisions            | `decisions.md`                                           |
| `ASM-nn`         | assumption, with the default chosen                                         | any feature file                                         |
| `RISK-nn`        | risk                                                                        | any feature file                                         |
| `R<round>-nn`    | finding in a review round                                                   | `reviews/`                                               |
| `ADR-NNNN`       | architecture decision, numbered across the whole project                    | `docs/adr/`                                              |
| `CAP-nn`         | product capability, numbered across the whole project                       | `.sdd/product.md`                                        |
| `RM-nn`          | roadmap item: one future feature, numbered across the whole project         | `.sdd/roadmap.md`                                        |

Links point upward, from what was built to what it was built for: a feature names the roadmap item it delivers in its state record, a roadmap item names the capability it advances, an acceptance criterion belongs to its requirement, a component or interface names the requirements it covers, a task names the acceptance criteria it delivers, and a test names the acceptance criterion it proves, with its full ID (`F003:AC-02.1`).

## 7. Running records

Each feature keeps two running records next to its artifacts. They are what lets the work stop at any point and resume from the files alone.

|         | `state.yaml`                                              | `decisions.md`                                    |
|---------|-----------------------------------------------------------|---------------------------------------------------|
| Answers | where the feature stands, and what happens next           | what was asked, answered and decided, and why     |
| Shape   | small and structured; **overwritten** at every checkpoint | entries in sections; **append-only**              |
| Read    | first, by every run of every phase                        | when resuming, approving, reviewing, or disputing |

The records point to the artifacts by ID and version; they never duplicate their content.

### 7.1 Resuming

A run never relies on memory of an earlier session. It resumes in this order:

1. Read `state.yaml`: the phase, the step, the status, and what the next run must do.
2. Read the open entries of `decisions.md` that `state.yaml` points to, and any answers recorded since.
3. Read the artifacts at the versions the records name.

If the records and the artifacts disagree, stop and reconcile them before going on.

### 7.2 Checkpoints

A checkpoint is taken after every step, and before any stop: when the work waits for the human, is blocked, the phase ends, or the session ends. At each checkpoint:

1. **`decisions.md`:** add what happened since the last checkpoint: questions put to the human, their answers, decisions, notable choices, documentation impact.
2. **`state.yaml`:** overwrite `phase`, `step`, `status`, `next`, `waiting-for-human`, `blocked-by`, `tasks`, `known-failures` and `stale` so they describe the present, and add one line to `history`.
3. **Commit** the feature's changed files on the feature branch, never on main, with a message that says what happened, following the project's version-control practices (section 9).

### 7.3 Writing decisions

- Add entries at the end of their section; never rewrite or delete an earlier one.
- The only change allowed to an existing entry is filling in its answer fields once, when the human answers.
- A correction is a new entry that names the entry it corrects and why.
- The human's answers are recorded verbatim.
- Every entry is dated and names the IDs and versions it concerns, such as `brief.md@2`, `REQ-03` or `H-02`.

### 7.4 Approvals

An approval is recorded twice, on purpose:

- In `decisions.md`, as the answer to its `H-nn` entry, with the date, the version approved, and the human's words: this is the proof.
- In the approved artifact, whose `status` becomes `approved`: this mirrors it.

If the two ever disagree, `decisions.md` is correct and the artifact is fixed.

### 7.5 What is waiting

Everything waiting for the human lives in one place: an open `H-nn` entry, or an unanswered `Q-nn` question, in `decisions.md`. `state.yaml` lists only their IDs, in `waiting-for-human`, and sets `status` to `waiting-for-human` when nothing else can go on.

Work that doesn't depend on the answer can continue in the meantime.

## 8. The skills catalogue

Skills carry established practice for the technologies, patterns and practices a project uses. The skills catalogue, `.sdd/skills.yaml`, says which skills the project relies on and when each one applies. Every project has one, established at onboarding and kept current.

- **Load what matches.** At the start of every step, load the `approved` entries whose `use-when` includes the current phase and whose `covers` touches the work: the technologies a task names, the patterns and practices it involves. Apply their guidance. Do not load entries that don't match.
- **The project's files win.** When a skill's guidance conflicts with the constitution, the architecture or the requirements, the project's file applies, and the conflict is recorded in the decisions record.
- **A missing skill doesn't stop the work.** When a listed skill isn't available in the session, report it, and record it in the state record's history; the work goes on without it.
- **New skills are approved by the human.** A phase that finds a skill would help proposes it through a decision entry; it is added as `approved` once the human agrees. Candidate skills come from the skills the session lists as available, or from the human, never from scanning the machine.
- **Keep it current.** When the stack, the architecture or the constitution changes, check the entries that cover what changed: add, retire, or keep them.

## 9. Branches and commits

Branch names, commit messages and the way work is merged belong to the project, not to the method. They are defined in the constitution's practices, and a skill in the skills catalogue may help apply them.

The method only requires that:

- Feature work happens on a feature branch, and each task on its own branch from it. Nothing is committed to main; the human merges into main.
- A commit made for a task is traceable to its feature and its task, however the convention expresses it.

When the constitution says nothing about version control, follow the convention the repository's history shows, record it as an assumption in the decisions record, and recommend that the human make it a practice.

## 10. The documentation catalogue

Some documents must be kept current because the company, a regulation, a contract or the team requires them: runbooks, support guides, compliance records, API references, the README. The documentation catalogue, `.sdd/documentation.yaml`, lists each one, why it is required, the structure it must keep, and what makes it need an update. Every project has one, established at onboarding and kept current.

- **Document updates what the feature triggers.** In Document, every `active` entry whose `update-when` matches what the feature changed is brought in line with what was built, following its `format`.
- **The required structure wins.** A document that follows a company template, a standard or a skill keeps that structure; it is filled in, never reorganized.
- **Nothing is skipped silently.** When an entry cannot be updated with the information available, it is put to the human through a decision entry, with what is missing.
- **New documents are approved by the human.** A phase that finds a document should be kept proposes it through a decision entry; it is added once the human agrees.
- **Keep it current.** When a document is retired, replaced or moved, its entry is retired or updated, never deleted.

## 11. The roadmap

The roadmap, `.sdd/roadmap.md`, holds the increments the product will grow by. Each item is one future feature. When an item is ready, the signs that it is too large and how it is split are explained in [methodology.md](methodology.md) (section 3). Every project has one, established at onboarding and kept current.

- **Where an item sits says what it is.** The sequence holds the items the human has placed, in priority order, the first being the next feature. The inbox holds candidates not yet placed. Closed holds the items delivered, split or dropped.
- **Two statuses while open.** `candidate`: not yet refined enough to start. `ready`: meets the readiness criteria and can become a feature. The items near the top of the sequence are ready.
- **In progress is not recorded.** An item is in progress while a feature whose state record names it is open. It is not marked in the roadmap, because that change would sit on the feature branch, unseen on main, until the merge.
- **One item, one feature.** A feature delivers exactly one item, named in its state record's `roadmap-item`. A feature that leaves part of its item for later splits it: the original is closed as split, each piece becomes an item, and the feature names the piece it builds.
- **The order is the human's.** Placing an item in the sequence, reordering it and dropping an item are the human's decisions. Refining an item, splitting it with the human's agreement, and adding candidates to the inbox are not.
- **Features change it on their branch.** Define adds the remainder of an item it narrows or splits; Document closes the delivered item, with the feature and the date, and adds the feature's follow-ups to the inbox; Release adds what the human defers while the pull request is open. Those changes reach main with the merge. Outside a feature, the roadmap is changed in the working tree, and the human commits it.
- **Never delete.** A closed item keeps its heading and its ID, with how it closed. IDs are never reused.
- **Point, don't copy.** An item names its capability (`CAP-nn`) and its dependencies (`RM-nn`) by ID. It never restates the product description, a feature's requirements or the design.
- **Keep it aligned.** Every planned capability in the product description has at least one item, or is explicitly deferred there. Every item names a capability that exists, or says it is an enabler. Every delivered item names a merged feature.

