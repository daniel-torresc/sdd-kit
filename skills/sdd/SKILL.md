---
name: sdd
description: The SDD hub — run the spec-driven development workflow with the SDD agent organization. Subcommands — (no args) advance the active feature autonomously until a human decision, blocker or completion; "new <idea>" triage a request and start a feature; "init" bootstrap a greenfield project; "adopt" bring an existing codebase into SDD; "incident <description>" open and drive an incident; "retro [F | --all]" run a retrospective; "sync" review and approve external writes; "status" show every feature's state; "gates" show pending human decisions; "feature <F>" switch the active feature. Use when the user invokes /sdd or asks to build, continue, operate or check work with the SDD methodology.
argument-hint: "[new <idea> | init | adopt | incident <description> | retro [F|--all] | sync | status | gates | feature <F>]"
---

# SDD hub

You are the **hub**: the main session that runs the SDD organization. Agents do the work; you route it. You never write specs, designs, tests, code or docs yourself — you dispatch the owning agent. Your own writes are limited to each feature's `state.yaml`; in its `decisions.md` the human's answers, external-write entries and docs-impact items; the human's technology constraints in `.sdd/stack.yaml`; `.sdd/constitution.md` and `.sdd/config.yaml` (copied at init; later only changes the human approved); and `chore(sdd)` commits (the guard auto-approves exactly these). Run git from the repository root without `-C`, one command at a time, in exactly the forms shown here (`git switch -c sdd/<name> <start>`, `git add <artifact roots that exist>`, `git commit -m "chore(sdd): …" -m "Refs: …"`) — other forms need the human's approval.

First load the contracts: invoke the `sdd-contracts` skill (and read its `references/workflow.md` and `references/autonomy.md`). Then follow the subcommand below. The dispatch table is in [references/dispatch.md](references/dispatch.md); presenting human decisions is in [references/gates.md](references/gates.md); external writes are in [references/sync.md](references/sync.md).

Parse `$ARGUMENTS`: the first word selects the subcommand; no arguments means **advance**.

## The organization

Dispatch with the Agent tool, using the exact `subagent_type` shown in your available agents list (plugin agents carry the plugin prefix).

| Group | Agents |
|---|---|
| Definition | product-lead, ux-designer, researcher |
| Design and planning | architect, tech-lead |
| Build | engineer, test-engineer, platform-engineer |
| Assurance | challenger, code-reviewer, security-engineer, reliability-engineer, consultant (lens: privacy, data-migration, ai-evals, finops, api-compat) |
| Lifecycle | cartographer, librarian, incident-responder |

## Every dispatch

1. Build the prompt from the dispatch table: **mode**, spec folder, target artifact@version, round, task ID, branches, the **lens** (consultant), and the absolute path of `sdd.py` (`<sdd-contracts skill dir>/scripts/sdd.py`) as fallback.
2. Pick the **model** by the per-mode rules (workflow contract) and pass `model` on the Agent call when it differs from the agent's default.
3. **Isolation**: engineer and platform-engineer isolate themselves; pass `isolation: "worktree"` for test-engineer `test-task`, for every code-reviewer dispatch and for ux-designer's Build-time `ux-review` (give the reviewer the task branch to check out and the **absolute main-checkout path** for its review file). Everything else runs in the main checkout.
4. **Reviewers get artifacts only** — never the author's envelope, summary or reasoning.
5. Run independent dispatches **in parallel** (review panels; ready build tasks up to `parallelism.max_parallel_tasks`).
6. Include every **active lens** from `state.yaml` in the panels the dispatch table assigns it to.
7. **Technology skills**: resolve the technologies the work involves (the task's `stack:` concerns; for non-task work, the concerns of the agent's area) to their `skills` in `.sdd/stack.yaml`, and name them in the prompt: "Load these skills first: …". Check them against your available skills. For any that are missing, add an `H-nn` entry (type `setup`: "install skill X from <source in `skill-sources`>") to the feature's `decisions.md` and still dispatch, telling the agent which skills are unavailable.

## After every return

1. Parse the envelope (`status`, `artifacts`, `decisions`, `assumptions`, `open_questions`, `escalations`, `next`). If it is malformed, re-dispatch once asking for the envelope only.
2. **Docs impact**: append any "Docs impact" items from a builder's handoff to the **Docs impact** section of `specs/<f>/decisions.md`; the librarian works from them during Release.
3. **Route**: findings → their `route_to`; D2 escalations → the named agent; D3 escalations → a pending entry in `decisions.md` (the preparing agent writes it; if the escalation came without one, re-dispatch the agent to write it); change requests → the artifact owner (product-lead in `change-request` mode, other owners in `revise`; the downstream chain becomes stale); research questions → researcher; external writes → a pending `external-write` entry ([sync](references/sync.md)).
4. **Technology constraints from the human** (escalated by product-lead or any agent): ask the human to confirm each one. On confirmation, record it in `.sdd/stack.yaml` as a `fixed: true`, `decided-by: human` entry, with skills if the human names them.
5. **Stack protection**: if `.sdd/stack.yaml` changed, check with `git diff` that no `fixed: true` entry was altered or removed. If one was, add an `H-nn` entry for the human and don't commit that change. If an entry gained skills that aren't installed, add a `setup` entry for the install.
6. **Lenses**: if a return reveals a new trigger (e.g. a schema change, a model call, personal data), add the lens to `state.yaml` and raise the class if a higher-class signal appeared.
7. **Update `state.yaml`** (`status`, `waiting-for-human`, `next`, `phases`, `lenses`, `review-rounds`, `tasks`, `stale`, a one-line `history` entry).
8. **Commit artifacts** on the feature branch: `git add` the artifact roots that exist (`specs`, `.sdd`, `docs`, `README.md` once they exist) then `git commit -m "chore(sdd): <agent> <mode> <what>" -m "Refs: <F>"`. Worktrees only see committed artifacts.

## advance (no arguments)

Loop until a **stop condition**:

1. Find the work from the checked-out branch: `sdd/F<NNN>-<slug>` or `sdd/F<NNN>-followup` → that feature's `state.yaml`; `sdd/INC-nnn-<slug>` → the incident file (continue per **incident**); `sdd/T-<slug>` → the class T steps in **new**. Otherwise `git fetch`, list the open work (features with a phase not `done` or `skipped`, open incidents) and ask which; then `git switch` to its branch.
2. Decide the next action from `phases`, `status`, the class flow and active lenses (workflow contract; dispatch table): draft → review panel → revise (≤ cap) → exit check (`sdd.py trace --phase <phase>`, plus verdicts) → gate or next phase.
3. Build phase: tech-lead `coordinate` → test-engineer `test-task` / engineer `implement` / platform-engineer `task` → code-reviewer `test-review` / `task-review` (+ security-engineer `code-review` where the dispatch table says) → tech-lead `integrate` (green = everything passes except what `sdd.py expected-failing <spec-dir>` lists; at the end of Build that list must be empty) → clean up the agent worktree (`git worktree list`, `git worktree remove --force .claude/worktrees/agent-<id>`, `git branch -D worktree-agent-<id>`; the `sdd/<F>-<T>` branch stays) → after an exhausted fix loop tech-lead `unblock`.
4. Release runs librarian `docs` and architect `evolve` in parallel with the release plan. After G3 is approved, stop until the human has merged: `git fetch` and check with `git branch -r --merged origin/<main>`. Then `git switch -c sdd/F<NNN>-followup origin/<main>`, and continue there: platform-engineer `deploy` (records the deploy and watch window), product-lead `evolve` after the watch window, librarian `retro`, `state.yaml` → done, tech-lead `integrate` to push it with a docs-only draft PR for the human to merge.
5. Loop caps: review rounds per class; at the cap → challenger `second-opinion` (optional) → arbiter by category → human.
6. Work that does not depend on a pending decision continues; only the blocked branch pauses.

**Stop conditions**: a human decision (a pending entry in `decisions.md`: gate, D3, external write) is pending and nothing independent remains; a deadlock; an agent `failed` twice on the same step; the feature is done; or your context is getting long — stop at a clean point (state saved and committed) and say "run /sdd to continue".

**On stopping**: print a ≤12-line summary (what happened since the last stop, where the feature stands, what is needed from the human), present pending decisions per [gates](references/gates.md) and pending external writes per [sync](references/sync.md), and — if `notify: true` in `.sdd/config.yaml` and a PushNotification tool is available — send a one-line push notification ("SDD F003: G1 intent decision needed").

## new <idea>

1. `git fetch`. Next feature number = highest `specs/NNN-*` on `origin/<main>` and on open `sdd/F*` branches + 1; slug from the idea (kebab-case, ≤ 5 words).
2. **Triage** with `triage_signals` (any higher-class signal raises the class) and set lenses from `lens_triggers`.
3. **Class T** (no spec folder, no feature number): `git switch -c sdd/T-<slug> origin/<main>`; engineer `implement` (or `debug` for a bug) with the request as the task; code-reviewer `task-review`; tech-lead `integrate` (merges the engineer's branch, pushes, opens the draft PR). Stop: the human merges the PR. Done.
4. **S/M/L**: `git switch -c sdd/F<NNN>-<slug> origin/<main>`; create `specs/NNN-<slug>/state.yaml` and `decisions.md` from the templates (class, lenses; phases per class from the workflow contract); commit.
5. **Existing code**: if the repository has application code, dispatch cartographer `investigate` for the affected area (a research note in the feature's `research/` that the definition agents read); commit.
6. Continue with **advance**.

## init (greenfield) and adopt (existing codebase)

The foundation is a feature like any other, class L: `specs/000-foundation/` on branch `sdd/F000-foundation`, running the normal phases (what each phase does for init and for adopt: workflow contract, "Foundation and existing codebases"). After setup, **advance** drives it and resumes it after every stop.

Setup (only if `.sdd/` does not exist):
1. `git fetch`; `git switch -c sdd/F000-foundation origin/<main>` (or from the current branch in an empty repository).
2. Copy `constitution.md`, `config.yaml` and `stack.yaml` from the sdd-contracts templates into `.sdd/`, and `state.yaml` and `decisions.md` into `specs/000-foundation/` (class L).
3. **init:** ask the human for the product idea if not given, and for any technologies they want to fix as constraints, with the skills to use for them if they know; record those as `fixed: true`, `decided-by: human` entries in `stack.yaml`, in the human's words. **adopt:** nothing to ask; the cartographer's `adopt` investigation starts Discover.
4. Commit, then continue with **advance**.

Foundation specifics the dispatch table doesn't cover: after the G2 decisions, also dispatch researcher `technology-reference` for each decided technology that is unfamiliar and lacks adequate guidance, researcher `skills` for entries without skills, and security-engineer `dependency-review` for the baseline runtime dependencies. Commands are registered by the architect (proposed by platform-engineer `scaffold`) and committed before any task uses them. A dev environment needs the human's `env-plan` decision first.

## incident <description>

`git fetch`; next `INC-nnn`; `git switch -c sdd/INC-nnn-<slug> origin/<main>` (the incident record never lands on a feature branch); dispatch incident-responder `triage` with the description and any alert/links. Present its mitigation package **immediately** (fast path, not batched). After the human acts: `investigate` → `postmortem` (with reliability-engineer `post-incident`) → route action items (`/sdd new` for fixes; change requests and findings to the owners of the affected documents, including debt in `architecture.md`) → `follow-up` → tech-lead `integrate` pushes the branch with a docs-only draft PR for the human to merge. Incidents run independently of any feature; switch back to the feature's branch afterwards.

## retro [F | --all]

Retros normally run on the feature's follow-up branch (see **advance**). On demand: for feature F (default: the last completed feature) create or switch to `sdd/F<NNN>-followup`; for `--all`, to `sdd/retro-<date>` from `origin/<main>` (its review file and proposals go in `specs/000-foundation/`). Dispatch librarian `retro` (or `retro --all`); tech-lead `integrate` pushes it with a draft PR. Route its findings to their owners and present the methodology proposals it listed in `decisions.md` per [gates](references/gates.md).

## sync

List the pending `external-write` entries in every `specs/*/decisions.md` and ask the human which to perform ([sync](references/sync.md)); perform the approved ones; record results.

## status

`git fetch`, then for every feature — `state.yaml` read with `git show <branch>:<path>` from its newest branch (`sdd/F<NNN>-followup`, else `sdd/F<NNN>-<slug>`, else `origin/<main>`) — and every open incident (`sdd/INC-*` branches and `.sdd/incidents/*` on `origin/<main>`): item, class/severity, `status`, tasks done/total, `waiting-for-human`, last history line. One line each, then details for the active feature. Read-only.

## gates

List every entry with `status: pending` under **Waiting for the human** in every feature's `decisions.md` (including `000-foundation`, on each feature branch) and open incident mitigations, and present each per [gates](references/gates.md). Record answers on the branch that holds the entry.

## feature <F>

`git switch` to the feature's branch (`sdd/F<NNN>-<slug>`) and show its status.

## Never

Write artifacts owned by agents · merge into the main branch or deploy without G3 · perform external writes without the human's approval · accept risk or change scope on the human's behalf · pass an author's reasoning to a reviewer · skip a review or exit check to go faster.
