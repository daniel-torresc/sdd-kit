# SDD glossary

The terms the hub skill and the contracts use, in plain words. Consult it when a term is unclear.

- **Agent**: a specialised subagent defined in the plugin's `agents/` folder. You start one with the Agent tool. That call is a **dispatch**.
- **Mode**: the particular job you ask an agent to do. Every agent has several. The architect, for example, has `design`, `revise`, `consult` and `evolve`. Always name the mode in the dispatch.
- **Artifact**: any file the methodology produces, such as a brief, requirements, a design, tasks, tests or a review file. Each artifact has exactly one **owner** agent, and only the owner edits it. Everyone else reports problems to the owner.
- **Spec folder**: `specs/NNN-<slug>/`, which holds one feature's artifacts.
- **artifact@version**: artifacts carry a version number in their header. Tell a reviewer exactly which version to review, for example `design.md@3`. When an upstream artifact changes, the artifacts built on it become **stale** and must be checked again.
- **Review, round**: a second agent checking an artifact from a fresh context. Reviews happen only in Design (challenger plus active lens specialists), Build (one code review per task) and Verify (one review of the whole feature); in Discover and Specify the human is the reviewer. One cycle of "review, then revise" is a round: up to 3 in Design, one elsewhere (`loop_caps` in `config.yaml`).
- **Finding**: one problem a reviewer raises, with a severity and a `route_to`, the owner who must answer it.
- **Envelope**: the structured summary an agent returns when it finishes. Its fields are status, artifacts changed, decisions taken, assumptions, open questions, escalations and the suggested next step. The details live in files. The envelope tells you what happened.
- **D0–D3**: decision levels from the autonomy contract. D0: just do it. D1: do it and record it. D2: needs another agent's sign-off. D3: needs the human. Passing a decision up a level is an **escalation**.
- **Lens**: an extra specialist review that switches on when a feature touches a sensitive area: security, reliability, ux, privacy, data-migration, ai-evals, finops or api-compat. The triggers are in `config.yaml`. An active lens adds its specialist to the Design, Build and Verify reviews.
- **`state.yaml`**: the feature's progress file. You rewrite it after every step. It is the only thing a new session needs to resume.
- **`decisions.md`**: the feature's decision log. It holds what agents decided, what is waiting for the human, and what the human answered.
- **`.sdd/`**: the project-level files.
  - `constitution.md`: principles and non-negotiables.
  - `config.yaml`: settings such as triage signals, lens triggers, caps, parallelism and notifications.
  - `stack.yaml`: the technologies, the skills to load for each one, and the project's commands.
  - `product.md`: the product overview.
  - `architecture.md`: the system overview.
- **Exit check**: what a phase must satisfy before it ends: its reviewers approve, and the script `sdd.py trace --phase <phase>` checks every ID and link between artifacts. The script is advisory: each violation becomes a finding for the artifact's owner.
- **Guard**: a hook (`scripts/guard.py`) that approves agents' actions automatically and denies only what is irreversible or the human's to decide: pushing or merging to main, force-pushes, production deploys, infrastructure applies, destructive deletes, writes to outside systems. It also approves the hub's bookkeeping. File ownership is not enforced by the guard; the hub checks the changed files after every step.
- **Worktree**: a second checkout of the repository in its own folder. An agent can work on a branch there without disturbing the main checkout.
