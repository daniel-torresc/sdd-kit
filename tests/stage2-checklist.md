# Stage 2 — class T and S on a local-only fixture

Fixture: `~/Documents/brain-harness/sdd-fixture-todo` (no remote; `.sdd/` prepared as if adopted).
Purpose: the first real run of the current system — do the hub and agents follow the workflow when they work on their own?

## How to run

```bash
cd ~/Documents/brain-harness/sdd-fixture-todo
claude --plugin-dir ~/Documents/brain-harness/brain-common
```

1. **Run 1 (T):** `/sdd new Fix the typo in the "task not found" error message`
   Expected stop: the change is on `sdd/T-…` and waits for you to merge it locally. To merge: `! git switch main` then `! git merge --no-ff sdd/T-<slug>`.
2. **Run 2 (S):** `/sdd new Reject empty or whitespace-only task titles with a clear error`
   Expected stops: possibly intent questions (answer briefly); then the G3 decision. Approve, then merge locally the same way; run `/sdd` once more to see the follow-up behavior.

Don't fix anything mid-run. If something blocks, note where and run `/sdd` to see whether it resumes.

## What to observe (I check the transcript and git afterwards)

| # | Check | Run |
|---|---|---|
| 1 | Triage picks T for run 1 and S for run 2, with no lenses | both |
| 2 | T: no spec folder; `sdd/T-<slug>` from `main` (local-only: no fetch, push or PR); engineer on `sdd/T-<slug>-impl`; code review in the envelope; tech-lead merges and stops | T |
| 3 | S: `specs/001-…` with `state.yaml` and `decisions.md`; branch `sdd/F001-…` from `main` | S |
| 4 | Cartographer `investigate` runs for S (existing code) and writes a research note; not for T | both |
| 5 | Specify: REQ + AC only; challenger and test-engineer review; review answers in `*-answers.md` | S |
| 6 | Plan: short `tasks.md` (test task + engineer task), no review panel; `trace --phase plan` clean | S |
| 7 | Build: test task in a worktree, tests fail for the right reason; test-review; integration accepts `expected-failing`; engineer makes them pass; list empty at the end | S |
| 8 | Worktrees and `worktree-agent-*` branches cleaned up after integration | S |
| 9 | Verify: test-engineer only; evidence pack and `evidence/traceability.md` | S |
| 10 | Release lite: G3 entry in `decisions.md` (no `release.md`), presented on one screen with a question | S |
| 11 | Hub commits `chore(sdd)` after every step; `state.yaml` stays truthful | both |
| 12 | Guard denials: every one is a prompt/policy mismatch to fix (list them) | both |
| 13 | Permission prompts you had to answer (each one is an auto-approve gap) | both |
| 14 | Cost: dispatches, wall time, usage per run | both |
