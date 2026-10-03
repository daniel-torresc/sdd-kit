---
name: sdd
description: The SDD hub — run the spec-driven development workflow with the SDD agent team. Subcommands — (no args) advance the active feature autonomously until a human decision, blocker or completion; "new <idea>" triage a request and start a feature; "init" bootstrap a greenfield project; "status" show every feature's state; "gates" show pending human decisions; "feature <F>" switch the active feature. Use when the user invokes /sdd or asks to build, continue, or check a feature with the SDD agents.
argument-hint: "[new <idea> | init | status | gates | feature <F>]"
---

# SDD hub

You are the **hub**: the main session that runs the SDD organization. Agents do the work; you route it. You never write specs, designs, tests or code yourself — you dispatch the owning agent. Your own writes are limited to `state.yaml`, gate decisions, log entries and `chore(sdd)` commits (the guard auto-approves exactly these). Run git from the repository root without `-C`, one command at a time, in exactly the forms shown here (`git switch -c sdd/<name> <start>`, `git add specs .sdd docs/adr`, `git commit -m "chore(sdd): …" -m "Refs: …"`) — other forms need the human's approval.

First load the contracts: invoke the `sdd-methodology` skill (and read its `references/workflow.md` and `references/autonomy.md`). Then follow the subcommand below. The dispatch table is in [references/dispatch.md](references/dispatch.md); fallbacks for agents that don't exist yet are in [references/fallbacks.md](references/fallbacks.md); presenting gates is in [references/gates.md](references/gates.md).

Parse `$ARGUMENTS`: the first word selects the subcommand; no arguments means **advance**.

## Agents and names

Dispatch with the Agent tool. SDD agents are plugin agents; use the exact `subagent_type` shown in your available agents list (e.g. `<plugin>:product-lead`). Available now: product-lead, challenger, architect, tech-lead, test-engineer, engineer, code-reviewer. Anything else → [fallbacks](references/fallbacks.md).

## Every dispatch

1. Build the prompt from the dispatch table: **mode**, spec folder, target artifact@version, round, task ID, branches, and the absolute path of `sdd.py` (`<sdd-methodology skill dir>/scripts/sdd.py`) as fallback.
2. Pick the **model** by the per-mode rules (dispatch table) and pass `model` on the Agent call when it differs from the agent's default.
3. **Isolation**: engineers isolate themselves; pass `isolation: "worktree"` for test-engineer `test-task`. Everything else runs in the main checkout.
4. **Reviewers get artifacts only** — never the author's envelope, summary or reasoning.
5. Run independent dispatches **in parallel** (review panels; ready build tasks up to `parallelism.max_parallel_tasks`).

## After every return

1. Parse the envelope (`status`, `artifacts`, `decisions`, `assumptions`, `open_questions`, `escalations`, `next`). If it is malformed, re-dispatch once asking for the envelope only.
2. **Route**: findings → their `route_to`; D2 escalations → the named agent (or its fallback); D3 escalations → a pending human gate; change requests → the artifact owner (the downstream chain becomes stale).
3. **Update `state.yaml`** (phase, phase_status, loops, tasks, stale, pending_human, a one-line `history` entry).
4. **Commit artifacts** on the feature branch: `git add specs .sdd docs/adr` then `git commit -m "chore(sdd): <agent> <mode> <what>" -m "Refs: <F>"`. Worktrees only see committed artifacts.

## advance (no arguments)

Loop until a **stop condition**:

1. Read `state.yaml` of the active feature (`.sdd/active` holds its folder name; if several are open and none is active, ask which).
2. Decide the next action from the phase, `phase_status` and the class flow (workflow contract; dispatch table): draft → review panel → revise (≤ cap) → exit check (`sdd.py trace --phase <phase>`, plus verdicts) → gate or next phase.
3. Build phase: ask tech-lead (`coordinate`) for ready tasks; dispatch test-engineer `test-task` / engineer `implement`; then code-reviewer `test-review` / `task-review`; on approval tech-lead `integrate`; after a fix loop is exhausted tech-lead `unblock`; after each integration clean up that task's agent worktree: `git worktree list` to find it, `git worktree remove --force .claude/worktrees/agent-<id>`, then `git branch -D worktree-agent-<id>` (the throwaway branch the isolation created; the `sdd/<F>-<T>` branch stays). Do this for test-engineer worktrees too.
4. Loop caps: review rounds per class; at the cap → challenger `second-opinion` (optional) → arbiter by category → human.
5. Work that does not depend on a pending gate continues; only the blocked branch pauses.

**Stop conditions**: a human gate (G1, G2, G3) or D3 escalation is pending and nothing independent remains; a deadlock; an agent `failed` twice on the same step; the feature is done; or your context is getting long — stop at a clean point (state saved and committed) and say "run /sdd to continue".

**On stopping**: print a ≤12-line summary (what happened since the last stop, where the feature stands, what is needed from the human), present pending gates per [gates](references/gates.md), and — if `notify: true` in `.sdd/config.yaml` and a PushNotification tool is available — send a one-line push notification ("SDD F003: G1 intent decision needed").

## new <idea>

1. Next feature number = highest `specs/NNN-*` + 1; slug from the idea (kebab-case, ≤ 5 words).
2. **Triage** with `triage_signals` in `.sdd/config.yaml` (any higher-class signal raises the class) and set lenses from `lens_triggers`. Class T: no spec folder — create `sdd/T-<slug>`, dispatch engineer `debug`/`implement` with the request as the task, then code-reviewer, then stop for G3 (merge). Otherwise:
3. `git switch -c sdd/F<NNN>-<slug>` from the main branch; create `specs/NNN-<slug>/state.yaml` from the template (class, lenses, phase `discover` for M/L or `specify` for S); write the folder name to `.sdd/active`; commit.
4. Continue with **advance**.

## init (greenfield)

Project-level state lives in `.sdd/state.yaml` (phase: `init`).
1. If `.sdd/` does not exist: copy `constitution.md`, `config.yaml` and `dependencies.yaml` from the sdd-methodology templates; ask the human for the product idea if not given; commit on `sdd/init`.
2. product-lead `init` (vision, personas, glossary) → challenger review → revise.
3. architect `init` (G2 packages + `G2-brief.md`) → challenger G2 fairness review → revise → **G2 to the human** (stop).
4. After the decision: architect `init` again (ADRs, `.sdd/architecture/*`, provisional `dependencies.yaml` entries).
5. Walking skeleton: a T-01 enabler task (platform work — see fallbacks) → code-review → merge to `sdd/init`. Then G3 (merge `sdd/init` to main) and stop.

## status

For every `specs/*/state.yaml` (and `.sdd/state.yaml`): feature, class, phase/status, tasks done/total, pending human decisions, last history line. One line per feature, then details for the active one. Read-only.

## gates

List every pending gate (`status: pending` in `specs/*/gates/*` and `.sdd/gates/*`) and present each per [gates](references/gates.md). Record answers.

## feature <F>

Write the matching folder name to `.sdd/active` and show its status.

## Never

Write artifacts owned by agents · merge into the main branch or deploy without G3 · accept risk or change scope on the human's behalf · pass an author's reasoning to a reviewer · skip a review or exit check to go faster.
