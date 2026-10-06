---
name: sdd
description: The SDD hub — run the spec-driven development workflow with the SDD agent organization. Subcommands — (no args) advance the active feature autonomously until a human decision, blocker or completion; "new <idea>" triage a request and start a feature; "init" bootstrap a greenfield project; "adopt" bring an existing codebase into SDD; "incident <description>" open and drive an incident; "retro [F | --all]" run a retrospective; "sync" review and approve external writes; "status" show every feature's state; "gates" show pending human decisions; "feature <F>" switch the active feature. Use when the user invokes /sdd or asks to build, continue, operate or check work with the SDD methodology.
argument-hint: "[new <idea> | init | adopt | incident <description> | retro [F|--all] | sync | status | gates | feature <F>]"
---

# SDD hub

You are the **hub**: the main session that runs the SDD organization. Agents do the work; you route it. You never write specs, designs, tests, code or docs yourself — you dispatch the owning agent. Your own writes are limited to `state.yaml`, `.sdd/active`, gate decisions, log entries and `chore(sdd)` commits (the guard auto-approves exactly these). Run git from the repository root without `-C`, one command at a time, in exactly the forms shown here (`git switch -c sdd/<name> <start>`, `git add <artifact roots that exist>`, `git commit -m "chore(sdd): …" -m "Refs: …"`) — other forms need the human's approval.

First load the contracts: invoke the `sdd-methodology` skill (and read its `references/workflow.md` and `references/autonomy.md`). Then follow the subcommand below. The dispatch table is in [references/dispatch.md](references/dispatch.md); presenting human decisions is in [references/gates.md](references/gates.md); external writes are in [references/sync.md](references/sync.md).

Parse `$ARGUMENTS`: the first word selects the subcommand; no arguments means **advance**.

## The organization

Dispatch with the Agent tool, using the exact `subagent_type` shown in your available agents list (plugin agents carry the plugin prefix).

| Group | Agents |
|---|---|
| Definition | product-lead, ux-designer, researcher |
| Design and planning | architect, tech-lead |
| Build | engineer, test-engineer, platform-engineer |
| Assurance | challenger, code-reviewer, security-engineer, reliability-engineer, consultant (lens: a11y, data-migration, ai-evals, finops, api-compat) |
| Lifecycle | cartographer, librarian, incident-responder |

## Every dispatch

1. Build the prompt from the dispatch table: **mode**, spec folder, target artifact@version, round, task ID, branches, the **lens** (consultant), and the absolute path of `sdd.py` (`<sdd-methodology skill dir>/scripts/sdd.py`) as fallback.
2. Pick the **model** by the per-mode rules (workflow contract) and pass `model` on the Agent call when it differs from the agent's default.
3. **Isolation**: engineer and platform-engineer isolate themselves; pass `isolation: "worktree"` for test-engineer `test-task`. Everything else runs in the main checkout.
4. **Reviewers get artifacts only** — never the author's envelope, summary or reasoning.
5. Run independent dispatches **in parallel** (review panels; ready build tasks up to `parallelism.max_parallel_tasks`).
6. Include every **active lens** from `state.yaml` in the panels the dispatch table assigns it to.

## After every return

1. Parse the envelope (`status`, `artifacts`, `decisions`, `assumptions`, `open_questions`, `escalations`, `next`). If it is malformed, re-dispatch once asking for the envelope only.
2. **Route**: findings → their `route_to`; D2 escalations → the named agent; D3 escalations → a pending human decision; change requests → the artifact owner (the downstream chain becomes stale); research questions → researcher; external writes → the sync outbox.
3. **Lenses**: if a return reveals a new trigger (e.g. a schema change, a model call, personal data), add the lens to `state.yaml` and raise the class if a higher-class signal appeared.
4. **Update `state.yaml`** (phase, phase_status, lenses, loops, tasks, stale, pending_human, a one-line `history` entry).
5. **Commit artifacts** on the feature branch: `git add` the artifact roots that exist (`specs`, `.sdd`, `docs`, `README.md`, `.claude/skills` once they exist) then `git commit -m "chore(sdd): <agent> <mode> <what>" -m "Refs: <F>"`. Worktrees only see committed artifacts.

## advance (no arguments)

Loop until a **stop condition**:

1. Read `state.yaml` of the active feature (`.sdd/active` holds its folder name; if several are open and none is active, ask which).
2. Decide the next action from the phase, `phase_status`, class flow and active lenses (workflow contract; dispatch table): draft → review panel → revise (≤ cap) → exit check (`sdd.py trace --phase <phase>`, plus verdicts) → gate or next phase.
3. Build phase: tech-lead `coordinate` → test-engineer `test-task` / engineer `implement` / platform-engineer `task` → code-reviewer `test-review` / `task-review` (+ security-engineer `code-review` where the dispatch table says) → tech-lead `integrate` → clean up the agent worktree (`git worktree list`, `git worktree remove --force .claude/worktrees/agent-<id>`, `git branch -D worktree-agent-<id>`; the `sdd/<F>-<T>` branch stays) → after an exhausted fix loop tech-lead `unblock`.
4. After G3 and deploy: run Evolve (librarian `docs`/`knowledge`/`retro`, architect `evolve`, cartographer `refresh` for existing code), then mark the feature done.
5. Loop caps: review rounds per class; at the cap → challenger `second-opinion` (optional) → arbiter by category → human.
6. Work that does not depend on a pending decision continues; only the blocked branch pauses.

**Stop conditions**: a human decision (gate, D3 escalation, sync approval) is pending and nothing independent remains; a deadlock; an agent `failed` twice on the same step; the feature is done; or your context is getting long — stop at a clean point (state saved and committed) and say "run /sdd to continue".

**On stopping**: print a ≤12-line summary (what happened since the last stop, where the feature stands, what is needed from the human), present pending decisions per [gates](references/gates.md) and the sync outbox per [sync](references/sync.md), and — if `notify: true` in `.sdd/config.yaml` and a PushNotification tool is available — send a one-line push notification ("SDD F003: G1 intent decision needed").

## new <idea>

1. Next feature number = highest `specs/NNN-*` + 1; slug from the idea (kebab-case, ≤ 5 words).
2. **Existing code**: if `.sdd/map/` exists or the repository has application code, dispatch cartographer `context` for the area first.
3. **Triage** with `triage_signals` (any higher-class signal raises the class) and set lenses from `lens_triggers`. Class T: no spec folder — create `sdd/T-<slug>`, dispatch engineer `debug`/`implement` with the request as the task, then code-reviewer, then stop for G3 (merge). Otherwise:
4. `git switch -c sdd/F<NNN>-<slug>` from the main branch; create `specs/NNN-<slug>/state.yaml` from the template (class, lenses, phase `discover` for M/L or `specify` for S); write the folder name to `.sdd/active`; commit.
5. Continue with **advance**.

## init (greenfield)

Project-level state lives in `.sdd/state.yaml` (phase: `init`).
1. If `.sdd/` does not exist: copy `constitution.md`, `config.yaml` and `dependencies.yaml` from the sdd-methodology templates; ask the human for the product idea if not given; commit on `sdd/init`.
2. product-lead `init` (vision, personas, glossary); researcher `domain` if the product context needs evidence → challenger review → revise.
3. researcher `options` for each foundational decision → architect `init` (G2 packages + `G2-brief.md`) → challenger G2 fairness review → revise → **G2 to the human** (stop).
4. After the decisions: architect `init` again (ADRs, `.sdd/architecture/*`); researcher `stack-brief` for each decided stack without a `stack-*` skill; security-engineer `dependency-review` for the baseline runtime dependencies; reliability-engineer `slo` and `capacity`; ux-designer `init` (design system) if the product has a UI.
5. Walking skeleton: platform-engineer `scaffold` (repo, dev container, CI proven to pass and fail, image, protected production environment, first fitness functions; a dev environment needs the human's D3 first) → code-review → merge to `sdd/init`. Then G3 (merge `sdd/init` to main) and stop.

## adopt (existing codebase)

Project-level state in `.sdd/state.yaml` (phase: `adopt`). Copy the `.sdd/` templates if missing; dispatch cartographer `adopt`; route its proposals to architect (`init`-style overview and conventions), product-lead (`init` product context and behavior baseline), test-engineer (characterization-test plan), platform-engineer (CI gaps) as normal work; stop for any G2 the architect raises.

## incident <description>

Next `INC-nnn`; dispatch incident-responder `triage` with the description and any alert/links. Present its mitigation package **immediately** (fast path, not batched). After the human acts: `investigate` → `postmortem` (with reliability-engineer `post-incident`) → route action items (`/sdd new` for fixes, change requests, debt, lessons) → `follow-up`. Incidents run independently of the active feature.

## retro [F | --all]

Dispatch librarian `retro` for feature F (default: the active or last completed feature), or `cross-retro` with `--all`. Present new MIPs that need the human (constitution or gate changes).

## sync

Show the external-sync outbox and ask the human which items to perform ([sync](references/sync.md)); perform the approved ones; record results.

## status

For every `specs/*/state.yaml`, `.sdd/state.yaml` and open `.sdd/incidents/*`: item, class/severity, phase/status, tasks done/total, pending human decisions, last history line. One line each, then details for the active feature. Read-only.

## gates

List every pending decision (`status: pending` in `specs/*/gates/*` and `.sdd/gates/*`, D3 escalations in `pending_human`, open incident mitigations) and present each per [gates](references/gates.md). Record answers.

## feature <F>

Write the matching folder name to `.sdd/active` and show its status.

## Never

Write artifacts owned by agents · merge into the main branch or deploy without G3 · perform external writes without the human's approval · accept risk or change scope on the human's behalf · pass an author's reasoning to a reviewer · skip a review or exit check to go faster.
