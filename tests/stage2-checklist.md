# Stage 2 — class T and S on a small fixture

Fixture: `~/Documents/brain-harness/sdd-fixture-todo` (`.sdd/` prepared as if adopted). The hub no longer supports projects without an `origin` remote, so give the fixture a local bare repository as its remote first:

```bash
git init --bare ~/Documents/brain-harness/sdd-fixture-todo-origin.git
cd ~/Documents/brain-harness/sdd-fixture-todo
git remote add origin ~/Documents/brain-harness/sdd-fixture-todo-origin.git
git push -u origin main
```

Pushes then go to that local folder, and `gh` PR commands will fail (there is no GitHub repository): note how the tech-lead handles it.

Purpose: the first real run of the current system — do the hub and agents follow the workflow when they work on their own?

## How to run

```bash
cd ~/Documents/brain-harness/sdd-fixture-todo
claude --plugin-dir ~/Documents/brain-harness/brain-common
```

1. **Run 1 (T):** `/sdd new Fix the typo in the "task not found" error message`
   Expected stop: the change is on `sdd/T-…` and waits for you to merge it. To merge: `! git switch main`, `! git merge --no-ff sdd/T-<slug>`, `! git push origin main`.
2. **Run 2 (S):** `/sdd new Reject empty or whitespace-only task titles with a clear error`
   Expected stops: Discover questions (answer them); the brief approval; G1; then G3. Approve, merge the same way, and run `/sdd` once more to see the follow-up behavior.

Don't fix anything mid-run. If something blocks, note where and run `/sdd` to see whether it resumes.

## What to observe (I check the transcript and git afterwards)

| # | Check | Run |
|---|---|---|
| 1 | Triage picks T for run 1 and S for run 2, with no lenses | both |
| 2 | T: no spec folder; `sdd/T-<slug>` from the latest main; engineer on `sdd/T-<slug>-impl`; code review in the envelope; tech-lead merges and pushes | T |
| 3 | S: `specs/001-…` with `state.yaml` and `decisions.md`; branch `sdd/F001-…` from the latest main | S |
| 4 | Cartographer `investigate` runs for S (existing code) and writes a research note; not for T | both |
| 5 | Discover: questions written to `decisions.md`, passed to you unchanged, answers recorded word for word; a fresh product-lead continues; short brief; brief approval asked | S |
| 6 | Specify: REQ + AC only; no agent review; G1 asked | S |
| 7 | Design: short design; challenger reviews (one or more rounds) | S |
| 8 | Plan: short `tasks.md` (test task + engineer task); `trace --phase plan` violations, if any, routed to tech-lead | S |
| 9 | Build: test task in a worktree, tests fail for the right reason; one test-review; integration accepts `expected-failing`; engineer makes them pass; one task-review; list empty at the end | S |
| 10 | Worktrees and `worktree-agent-*` branches cleaned up after integration | S |
| 11 | Verify: test-engineer `verify` and code-reviewer `feature-review`; evidence pack and `evidence/traceability.md` | S |
| 12 | Release lite: G3 entry in `decisions.md` (no `release.md`), presented on one screen with a question | S |
| 13 | Hub commits `chore(sdd)` after every step, checks changed files; `state.yaml` stays truthful | both |
| 14 | Dispatches are real handoffs (context, file paths, what done looks like) | both |
| 15 | Guard denials (each should be a real boundary) and permission prompts you had to answer | both |
| 16 | Cost: dispatches, wall time, usage per run | both |
