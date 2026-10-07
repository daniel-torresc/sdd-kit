# Contract 3 — Autonomy & escalation

The organization runs autonomously. Humans are interrupted only for decisions that genuinely need human intent, judgment or accountability. **If you are unsure of a decision's class, pick the higher class.**

## Decision classes

| Class | Covers | Action |
|---|---|---|
| **D0 Routine** | Reversible, in approved scope: implementation detail, test design, refactor, review fixes | Act. The commit is the record. |
| **D1 Notable** | Choice within constraints: library inside the chosen stack, internal API shape, trade-off inside an NFR budget | Act, then record it in `decisions.md` ("Decided by agents") with the reason. Write an ADR if architecturally significant. |
| **D2 Peer-gated** | Changing an approved artifact; adding a runtime dependency; changing a public contract, schema or event; touching another owner's artifact | Get sign-off from the owner or arbiter agent (new dependency → security-engineer checks license, CVEs, maintenance health). No human. |
| **D3 Human** | The list below | The hub pauses only that branch, continues independent work, and writes a decision package. |

## D3 — the only reasons to interrupt the human

1. **Intent** — confirming the spec (gate G1).
2. **Hard-to-reverse foundations** — greenfield stack, primary datastore, hosting platform, anything whose reversal would mean a rewrite (gate G2).
3. **Irreversible or external actions** — production deploy (G3), merging into the main or release branch, force-pushing or deleting remote branches, destructive data operations, spending money or provisioning paid resources, publishing, sending anything outside the project. *Not D3:* pushing `sdd/*` branches and opening or updating **draft** PRs — these are autonomous so CI can run.
4. **Risk acceptance** — deferring a critical/major finding; security exceptions.
5. **Scope change** beyond the approved spec.
6. **Legal** — copyleft or unknown licenses; regulated data (PII, health, financial).
7. **Deadlock** — loop cap exhausted, or no neutral arbiter.
8. **Constitution changes.**

## Execution permissions

The plugin's guard (`hooks/ownership.json`) is both a fence and a grant: each agent may write only the artifacts it owns and run only its allowlisted commands, and those in-policy actions are **approved without prompting** so work proceeds autonomously. Everything outside an agent's policy is denied; the main session keeps normal permission prompts. Allowlisted commands include tests and spikes, which execute project code with the user's rights — run autonomous sessions in Claude Code's sandbox or a dev container. `permissions.auto_approve: false` in `.sdd/config.yaml` restores prompts.

## Fast path

Incident mitigation decisions (from incident-responder `triage`) are presented to the human **immediately**, never batched with other gates. Everything else that waits for the human is batched at the hub's next stop.

## Assumption-first

When information is missing and the decision is not D3: record `ASM-nn` in the artifact with the default you chose and why, and continue. The hub batches all open assumptions into the next human gate, where the human can overturn any of them. Overturned assumptions reopen the affected artifacts.

## Decision packages

Every D3 item is an entry under "Waiting for the human" in the feature's `decisions.md` (project-level decisions live in the foundation feature, `specs/000-foundation/decisions.md`). The **preparing agent** writes it (G1 product-lead, G2 architect, G3 platform-engineer, risk entries the deferring owner, mitigations incident-responder); the hub only records the human's answer (status and the Decision line). A package contains:

- the decision, in one sentence;
- context — one screen maximum;
- options, each with pros, cons, and fit against the relevant REQ/NFRs;
- the recommending agent's view, clearly marked as a recommendation, not a decision;
- what is blocked until the human answers;
- open assumptions awaiting confirmation.

### G2 — foundational decisions

For G2 the architect must present **every viable option** (not just a preferred one), each with pros, cons, a fit matrix against the requirements, reversal cost, and operational cost. The `decisions.md` entry stays one screen; the full option analysis lives in a research note it links to. **The human decides.** The architect records the human's choice and reasons as an ADR with `decided-by: human` and updates `stack.yaml`.

## Escalation ladder

```
agent ──► artifact owner ──► arbiter (product-lead / architect / tech-lead) ──► human
```

Each step is taken only when the previous one cannot resolve the issue within the loop cap.
