---
name: sdd-contracts
description: The shared contracts of the SDD (Spec-Driven Development) workflow — artifact layout and ownership, traceability IDs, the agent return envelope, the review findings schema, the autonomy/escalation policy (D0–D3), triage classes, phase state machine, gates and loop caps. Load this whenever you create, edit, review or route any SDD artifact (anything under specs/, docs/adr/ or .sdd/), when acting as any SDD agent, or when deciding whether a decision needs another agent or a human.
---

# SDD Methodology — shared contracts

Every SDD agent and the hub (the main session running `/sdd`) follows these four contracts. They are the rules of the organization; agent definitions only add role-specific behavior on top.

| Contract | Read when | Reference |
|---|---|---|
| 1. Artifacts & traceability | Creating or editing any artifact; assigning or citing an ID | [references/artifacts.md](references/artifacts.md) |
| 2. Communication | Returning results to the hub; writing or answering a review | [references/communication.md](references/communication.md) |
| 3. Autonomy & escalation | Before any decision that is not obviously routine | [references/autonomy.md](references/autonomy.md) |
| 4. Workflow | Acting as the hub; triaging; checking phase exit criteria | [references/workflow.md](references/workflow.md) |

Templates for every artifact are in [templates/](templates/). Always **Read** the template before creating an artifact; the reference files above are the full rules.

## Non-negotiables (summary)

1. **One owner per artifact.** Only the owner edits it. Everyone else files a finding or change request routed to the owner.
2. **Artifacts are the message bus.** Detail goes in files; your final message to the hub is the return envelope (≤10-line summary). Subagents cannot talk to the human; questions go back to the hub.
3. **IDs are never reused.** Removed items are marked `[withdrawn]`, never deleted.
4. **Links point upward.** AC → REQ, task → REQ/AC, test → AC, commit → task.
5. **When unsure of a decision's class, pick the higher class.**
6. **Assumption-first.** Missing information that is not a D3 decision becomes a documented `ASM-nn` with a default; keep working.
7. **Reviewers are independent.** They judge artifacts, not the author's reasoning, and never edit what they review.
8. **Evidence or it's minor.** A major/critical finding without evidence is downgraded.
9. **Traceability is checked, not maintained by hand.** Run the trace script (below); at Verify it writes the traceability report into the evidence pack.

## Trace script

The script lives in this skill's own directory (the base directory shown when the skill loads; `<skill-dir>` below). Always call it with its **absolute path**, as one command with no chaining, redirection or shell variables:

```bash
uv run <skill-dir>/scripts/sdd.py trace specs/<NNN-slug> [--phase specify|design|plan|verify] [--junit report.xml]
uv run <skill-dir>/scripts/sdd.py stale specs/<NNN-slug>
uv run <skill-dir>/scripts/sdd.py expected-failing specs/<NNN-slug>
```

If you cannot determine `<skill-dir>`, use the path given in your dispatch prompt.

`trace` validates IDs and links and exits non-zero on violations for the given phase; with `--report <path>` it also writes the traceability matrix (used at Verify for `evidence/traceability.md`). `stale` reports artifacts whose `upstream:` versions are behind. `expected-failing` lists the AC tests allowed to fail on the current branch under test-first (their implementation task has no `Refs:` commit on it yet); every other test must pass. Parsing conventions the script relies on are in [references/artifacts.md](references/artifacts.md#markup-conventions-machine-readable).
