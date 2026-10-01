# Fallbacks for agents that don't exist yet (Wave 1)

When a finding, escalation or step is routed to an agent that is not in your available agents list, use its fallback, and **log every use** in `specs/<f>/log.md` (`| date | hub | fallback | <agent> → <fallback>: <what> | … |`) so the human can see where a specialist was missing. When the real agent becomes available, it takes over automatically — always check the agents list first.

| Missing agent | Fallback |
|---|---|
| **security-engineer** | **Dependency approvals (D2):** architect adds the dependency to `.sdd/dependencies.yaml` with `status: provisional` after checking license, known vulnerabilities (pip-audit / npm audit) and maintenance; copyleft or unknown licenses → D3. **Threat model / security review:** code-reviewer's security-basics checklist on every task, plus a `RISK-nn` in the brief: "No dedicated security review (Wave 1)". Class L features with auth, money or personal data: add that risk to G3 for explicit acceptance. |
| **reliability-engineer** | Pointers and threshold reviews → architect (NFR budgets); anything unresolved becomes a `RISK-nn`. |
| **platform-engineer** | Skeleton, CI, container and deploy-config tasks → engineer (`.sdd/config.yaml` `fallbacks.engineer_does_platform: true` lets the guard allow CI/infra files). Anything that provisions cloud resources, spends money or deploys → D3 for the human. G3 release plan → hub presents branch, PR and evidence; the human deploys. |
| **researcher** | Technology questions → architect (web search, context7); domain/market questions → product-lead (web search). Record findings in the artifact that asked. |
| **ux-designer** | Features with a UI: product-lead adds a "UX" section to `requirements.md` (flows, screens, all states, copy, accessibility) and the challenger reviews it. |
| **cartographer** | Existing codebases: architect reads the code and cites the current structure in `design.md`. |
| **librarian** | Architecture updates on ship → architect `evolve`; docs → the engineer of the relevant task. |
| **incident-responder** | Out of scope for Wave 1. |
| **consultant (lenses)** | a11y → code-reviewer + test-engineer axe checks; data-migration → architect; AI evals, FinOps, API compatibility → architect, with a `RISK-nn` if unresolved. |
