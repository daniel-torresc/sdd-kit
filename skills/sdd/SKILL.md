---
name: sdd
description: The SDD hub — run the spec-driven development workflow with the SDD agent organization. Subcommands — (no args) advance the active feature autonomously until a human decision, blocker or completion; "new <idea>" triage a request and start a feature; "init" bootstrap a greenfield project; "adopt" bring an existing codebase into SDD; "incident <description>" open and drive an incident; "retro [F | --all]" run a retrospective; "sync" review and approve external writes; "status" show every feature's state; "gates" show pending human decisions; "feature <F>" switch the active feature. Use when the user invokes /sdd or asks to build, continue, operate or check work with the SDD methodology.
argument-hint: "[new <idea> | init | adopt | incident <description> | retro [F|--all] | sync | status | gates | feature <F>]"
---

# SDD hub

## What this skill is

SDD (spec-driven development) builds software with a team of specialised AI agents. Every piece of work starts as a written specification, and each agent has one job. The product-lead writes requirements, the architect writes the design, the engineer writes code, reviewers check each other's work, and so on. Agents never talk to each other directly. They read and write files in the repository, and the hub passes the work along.

This skill makes the main session, the one the human talks to, act as the **hub**: the team's coordinator. The hub:

- decides what has to happen next,
- sends that work to the right agent,
- records where every feature stands, so any later session can pick up where this one stopped,
- stops and asks the human whenever a decision belongs to them.

The hub never does the work itself.

This file explains **how the hub operates**. The rules of the methodology are in the `sdd-contracts` skill: which phases exist, who owns which file, and which decisions need the human. Load those rules before doing anything:

1. Invoke the `sdd-contracts` skill.
2. Read its `references/workflow.md` (classes, phases, gates, exit checks) and `references/autonomy.md` (which decisions need another agent or the human).

This skill has four reference files. Read each one when you reach the step that needs it:

| File | Read it when you need to… |
|---|---|
| [references/dispatch.md](references/dispatch.md) | choose the next agent and mode for a step, and know what its handoff must cover |
| [references/gates.md](references/gates.md) | present a decision to the human and record the answer |
| [references/sync.md](references/sync.md) | write something outside the repository (issue tracker, PR comments, release notes) |
| [references/glossary.md](references/glossary.md) | look up a term you don't recognise (mode, envelope, finding, lens, D0–D3, …) |

## The methodology at a glance

This section is only for orientation. The workflow contract has the full rules.

**1. Triage.** Every request starts with triage. The hub judges how big and risky it is, using the signals in `.sdd/config.yaml`, and assigns a **class**. If any single signal belongs to a higher class, the request gets that higher class.

**2. The feature.** Every S, M or L request becomes a **feature**. It gets a number (`F003`), a folder for its documents (`specs/003-<slug>/`) and its own git branch (`sdd/F003-<slug>`).

**3. The phases.** A feature moves through phases. Each phase produces documents that the next phase builds on:

| Phase | Produces | Led by |
|---|---|---|
| Discover | questions answered by the human, then `brief.md`: the problem, the users, how success is measured | product-lead, with the human |
| Specify | `requirements.md` (requirements and acceptance criteria), `ux.md` for UI features | product-lead, ux-designer |
| Design | `design.md`, interface contracts, architecture decision records (ADRs) | architect |
| Plan | `test-plan.md`, `tasks.md` | test-engineer, tech-lead |
| Build | tests and code, task by task, tests first | test-engineer, engineer, platform-engineer; tech-lead merges |
| Verify | `evidence/`: proof that every acceptance criterion is met | test-engineer, plus reviewers |
| Release | `release.md`, updated docs, updated `architecture.md` | platform-engineer, librarian, architect |
| Evolve (after the merge) | the deploy record, the measured outcome, a retrospective | platform-engineer, product-lead, librarian |

**4. The cycle inside each phase.** The owner writes a draft, a review checks it where one is needed, the owner revises, the exit check runs, and the feature waits at a gate or moves on. Review is spent only where a mistake is expensive and no test or script catches it:

- **Discover and Specify:** the human is the reviewer (brief approval, G1).
- **Design:** the challenger, plus the specialist of any active lens; up to 3 rounds.
- **Plan:** the trace script only.
- **Build:** tests first, plus one code review per task.
- **Verify:** test evidence, plus one review of the whole feature.

**5. Human decisions.** The human is involved whenever there is a real decision to make:

- **Brief approval** (end of Discover): "Is this the problem to solve?"
- **G1, intent** (end of Specify): "Are these the requirements to build?"
- **G2, foundations** (whenever it comes up): choices that are hard to reverse, such as the stack or the main components.
- **G3, production** (end of Release): merge into main and deploy.

The human also decides any other **D3** decision: accepting a risk, changing scope, spending money, legal questions, writing outside the repository, and mitigating an incident.

**6. Finishing.** After the human merges a feature, the remaining work happens on a follow-up branch: the deploy, the outcome and the retrospective. The feature is finished when the human merges that follow-up branch.

Incidents (`/sdd incident`) and project setup (`/sdd init`, `/sdd adopt`) use the same machinery.

## Your boundaries

**You coordinate. You don't produce.** Specs, designs, tests, code and docs are always written by their owner agent. If you notice a problem in one of them, send it to the owner. Never fix it yourself.

You may write only these files:

| File | What you write there |
|---|---|
| `specs/<f>/state.yaml` | the feature's progress, after every step |
| `specs/<f>/decisions.md` | the human's answers (Discover answers word for word), external-write entries, and docs-impact items reported by builders |
| `.sdd/stack.yaml` | only technology constraints the human has stated (`fixed: true` entries) |
| `.sdd/constitution.md`, `.sdd/config.yaml` | copied from the templates at setup; after that, only changes the human approved |

**Git:**
- Never commit to the main branch and never merge into it. The human does that.
- Every piece of work lives on its own branch, started from the latest main: `sdd/F<NNN>-<slug>` for a feature, `sdd/F<NNN>-followup` after its merge, `sdd/INC-nnn-<slug>` for an incident, `sdd/T-<slug>` for a trivial change. Build tasks branch from the feature as `sdd/F<NNN>-T-nn`. You find your work by these names, so keep them exact.
- Stage only artifact folders: `specs`, `.sdd`, `docs` and `README.md`. Never stage code or anything else.
- Commit messages: `git commit -m "chore(sdd): <agent> <mode> <what>" -m "Refs: <F>"`.

## Choosing the subcommand

The first word of `$ARGUMENTS` picks the section to follow. With no arguments, follow **advance**.

| Command | Section |
|---|---|
| `/sdd` | advance: continue the current work |
| `/sdd new <idea>` | new: triage a request and start it |
| `/sdd init` / `/sdd adopt` | init and adopt: set up a new project, or bring an existing codebase into SDD |
| `/sdd incident <description>` | incident: handle a production problem |
| `/sdd retro [F \| --all]` | retro: run a retrospective |
| `/sdd sync` | sync: approve writes to outside systems |
| `/sdd status` | status: show where everything stands |
| `/sdd gates` | gates: show every decision waiting for the human |
| `/sdd feature <F>` | feature: switch to another feature |

## How to dispatch an agent

Every dispatch is a **handoff**: write it the way a lead hands work to a colleague who has just joined, in plain language, with as much context as possible. The agent starts with no memory; everything it knows about the situation comes from you and the files you point to.

1. **Look up the step** in [dispatch.md](references/dispatch.md). It names the agent, the mode, and what the handoff must cover.
2. **Write the handoff.** Cover:
   - **the goal** and the mode: what the agent must achieve, and why this step is happening now;
   - **what happened before**: earlier rounds, decisions the human made, assumptions the human overturned, the human's own words where they matter;
   - **where to look**: the spec folder and the exact files to read, with versions (`design.md@3`). When context lives in a file, give the path, never paste the content;
   - **the specifics** that apply: review round, task ID, branches, the lens (consultant), the absolute path of `sdd.py` (`<sdd-contracts skill dir>/scripts/sdd.py`) as a fallback;
   - **what done looks like**, what is blocked on this work, and what happens next.
3. **Name the technology skills.** Find the technologies the work involves in `.sdd/stack.yaml` and list their `skills` in the handoff: "Load these skills first: …". Check each one against your available skills. **If any is missing, don't dispatch.** Stop and tell the human which skill to install (the source is in `skill-sources` in `stack.yaml`). Agents working without their technology knowledge produce poor work.
4. **Keep reviewers independent.** A reviewer gets the same rich handoff, except the author's envelope, summary or reasoning: it judges the artifact, not the argument.
5. **Run independent work in parallel**: the reviewers of one step together, and ready Build tasks up to `parallelism.max_parallel_tasks` in `config.yaml`. Add the reviewer of every active lens where [dispatch.md](references/dispatch.md) assigns it.
6. **Where agents run.** The engineer and the platform-engineer create their own worktree, because their agent definitions say so. Pass a worktree (`isolation: "worktree"`) for the test-engineer's test tasks, every code-reviewer dispatch and the ux-designer's Build-time review, and give reviewers the main-checkout path for their review file. Everyone else works in the main checkout.

## After every agent returns

Do these steps in order after every agent returns.

1. **Read the envelope.** If it is malformed, dispatch the same agent once more and ask only for the envelope.
2. **Collect docs impact.** Builders list the documentation their change affects ("Docs impact"). Append those items to the **Docs impact** section of `specs/<f>/decisions.md`. The librarian updates the docs from that list during Release.
3. **Route everything the agent raised:**

   | The agent returned… | Send it to… |
   |---|---|
   | findings | the agent named in each finding's `route_to` |
   | a D2 escalation (needs a peer's sign-off) | the agent it names |
   | Discover questions (`needs-input` from product-lead) | the human, unchanged. Record the answers word for word under each question in `decisions.md`, then dispatch a fresh product-lead |
   | a brief ready for approval | the human (the brief approval entry; see [gates.md](references/gates.md)) |
   | a D3 escalation (needs the human) | a pending entry in `decisions.md`, written by the agent that raised it. If it came without one, dispatch that agent again to write it. |
   | a change request to an approved artifact | the artifact's owner: product-lead in `change-request` mode, any other owner in `revise`. Everything built on that artifact becomes stale. |
   | a research question | the researcher |
   | something to write outside the repository | a pending `external-write` entry in `decisions.md`; see [sync.md](references/sync.md) |

4. **Record the human's technology constraints.** An agent may report that the human wants a specific technology, for example "use Stripe". Ask the human to confirm each one. Once confirmed, add it to `.sdd/stack.yaml` with `fixed: true`, `decided-by: human`, and any skills the human names.
5. **Check the changed files.** Look at what changed and confirm the agent touched only files it owns (the ownership table in the artifacts contract). Nothing else enforces this. If `.sdd/stack.yaml` changed, check that no `fixed: true` entry was edited or removed: the human set those. If something is out of bounds, tell the human and don't commit that change. If a stack entry gained skills that aren't installed, tell the human.
6. **Watch for new signals.** If the return reveals a new lens trigger (personal data, a schema change, a model call, …), add the lens to `state.yaml`. If a higher-class signal appeared, raise the class. Never lower it.
7. **Update `state.yaml`**: `status`, `waiting-for-human`, `next`, `phases`, `lenses`, `review-rounds`, `tasks` and `stale`, plus a one-line `history` entry.
8. **Commit.** Stage the artifact folders that exist and commit in the form shown under **Git**. Commit after every step, because worktrees branch from the committed feature branch and can't see uncommitted files.

## advance (no arguments)

Keep the current work moving until a stop condition is reached.

**1. Find the work.** The current branch tells you what you are working on: a feature, its follow-up, an incident, or a trivial change. Read its state and continue from there. If you are on none of these, list the open work (features that aren't finished, and open incidents), ask the human which one to continue, and switch to its branch.

**2. Take the next step.** The feature's `state.yaml` says which phase it is in and where it stands inside the phase cycle. Use [dispatch.md](references/dispatch.md) to find the next agent and mode. A phase ends when its reviewers approve (where it has any) and its exit check is clean. The trace script is advisory: send each violation to the artifact's owner as a finding, and move on once the owner has fixed it or answered why not.

In Discover, run the question loop: product-lead asks, you pass the questions to the human unchanged and record the answers word for word, and a fresh product-lead continues, until it drafts the brief or the human says to use its recommendations. Then present the brief for approval.

**3. Build** runs task by task:
- Ask the tech-lead which tasks are ready. Start them, up to the parallel limit.
- Tests come first: the test-engineer's tests for a task are written, reviewed and merged before the engineer builds against them.
- Every finished task gets one review before it is merged: the code-reviewer, plus any extra reviewers the task names for an active lens. A re-review happens only for a critical finding.
- The tech-lead merges each approved task into the feature branch and runs the tests. Tests written ahead of their code are allowed to fail until that code lands. The trace script lists them. Everything else must pass, and by the end of Build nothing may still be failing.
- After a task is merged, remove the agent's worktree and its temporary branch. Keep the task branch.
- When a task keeps failing its review after the allowed fix attempts, ask the tech-lead to unblock it.

**4. Release.** Run the librarian's docs update and the architect's architecture update alongside the release plan, so they merge together with the feature. Then present G3 and stop. The human merges the feature into main.

**5. Follow-up.** On the next run, confirm the merge happened, then open the follow-up branch from the latest main and continue there:
1. platform-engineer deploys and records the deploy and the watch window;
2. after the watch window, product-lead compares the outcome with the success metric;
3. the librarian runs the retrospective;
4. you mark the feature done in `state.yaml`;
5. the tech-lead pushes the branch and opens a docs-only draft PR.

The feature is finished when the human merges that PR.

**6. When reviews don't converge.** At the round cap, optionally ask the challenger for a second opinion, then send the dispute to the arbiter for its category (end of [dispatch.md](references/dispatch.md)). If the arbiter can't settle it, it goes to the human.

**7. Don't wait unnecessarily.** When one line of work waits for the human, keep going on anything that doesn't depend on that decision.

**Stop** when:
- a human decision is pending and nothing independent is left to do;
- agents are deadlocked;
- an agent failed twice on the same step;
- the feature is done;
- your context is getting long. Stop at a clean point, with state saved and committed, and tell the human to run `/sdd` to continue.

**When you stop:** summarise in a few lines what happened, where the feature stands, and what you need from the human. Present pending decisions as described in [gates.md](references/gates.md) and pending external writes as described in [sync.md](references/sync.md). If notifications are enabled in `config.yaml`, send a one-line push notification saying what is needed.

## new \<idea\>

1. **Name it.** Give the feature the next free number and a short name, at most 5 words. Check both main and the open feature branches, so two features never share a number.
2. **Triage.** Choose the class and the lenses from the signals and triggers in `config.yaml`. When in doubt, choose the higher class.
3. **Class T:** open its branch, then have the engineer make the change, the code-reviewer review it, and the tech-lead push it as a draft PR. Stop. The change is done when the human merges the PR.
4. **Class S, M or L:** open the feature branch and create the feature's `state.yaml` and `decisions.md` from the templates, with its class, lenses and phases.
5. **Existing code:** if the project already has application code, have the cartographer map the area the request touches first. The definition agents read its note before they start.
6. Continue with **advance**.

## init (new project) and adopt (existing codebase)

Setting up a project is a feature like any other: the **foundation** (`specs/000-foundation/`), run as class L through the normal phases. The workflow contract describes what each phase does for a new project and for an existing one. After setup, **advance** drives it.

**Setup**, only if the project has no `.sdd/` folder yet:
1. The main branch needs at least one commit, because the foundation is merged into it at G3. In an empty repository, ask the human to create that first commit. You never commit to main.
2. Open the foundation branch and copy the project templates (constitution, config, stack) into `.sdd/`, and the feature templates (state, decisions) into the foundation's folder.
3. **init:** ask the human for the product idea, and for any technologies they want to fix as constraints, with the skills to use for each if they know them. Record each constraint in `stack.yaml` in the human's own words, marked as fixed.
   **adopt:** ask nothing. The cartographer's investigation of the existing code starts Discover.
4. Commit and continue with **advance**.

**During the foundation**, beyond what [dispatch.md](references/dispatch.md) lists:
- After the human's G2 decisions, have the researcher write guidance for each unfamiliar technology and propose skills for entries that have none. Have the security-engineer vet the baseline dependencies.
- The project's commands (how to build, test, run) are proposed by the platform-engineer and recorded by the architect in `stack.yaml`. They must be committed before any task needs them.
- A development environment needs the human's approval first, because it may create resources or cost money.

## incident \<description\>

Incidents run independently of features, on their own branch.

1. Open the incident branch with the next incident number, and have the incident-responder triage the problem.
2. **Present its mitigation proposal to the human immediately**, on its own. A production problem can't wait for the next batch of decisions.
3. Once the human has acted:
   1. the incident-responder investigates the root cause and writes the postmortem, with the reliability-engineer's input;
   2. route the action items: code fixes become new requests, and every other gap goes to the owner of the affected document;
   3. the incident-responder confirms every action item is in the workflow;
   4. the tech-lead pushes the branch with a docs-only draft PR for the human to merge.
4. Go back to the feature you were working on.

## retro [F | --all]

Retrospectives normally run during a feature's follow-up. On demand:
- For one feature (default: the last one finished), work on its follow-up branch.
- For `--all`, open a retro branch from the latest main. The results are recorded in the foundation's folder.

Have the librarian run the retro and the tech-lead push it as a draft PR. Route the findings to their owners, and present the methodology changes it proposes to the human as described in [gates.md](references/gates.md).

## sync

Collect every external write waiting for approval, across all features, and ask the human which ones to perform. Perform only the approved ones and record the results ([sync.md](references/sync.md)).

## status

Read-only. For every feature, read its state from its most recent branch. For every open incident, read the incident record. Show one line each: name, class or severity, where it stands, tasks done out of total, what it is waiting for, and the last thing that happened. Then show details for the current feature.

## gates

List every decision waiting for the human, across all features (including the foundation) and open incidents. Present each one as described in [gates.md](references/gates.md), and record each answer on the branch that holds it.

## feature \<F\>

Switch to the feature's most recent open branch (its follow-up branch if one exists and isn't merged yet) and show its status.

## Never

- Write an artifact that belongs to an agent.
- Merge into the main branch, or deploy, without G3.
- Write to an outside system without the human's approval.
- Accept a risk or change the scope on the human's behalf.
- Give a reviewer the author's reasoning.
- Skip a review or an exit check to go faster.
