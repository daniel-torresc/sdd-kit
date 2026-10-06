---
name: practice-platform
description: How the SDD platform-engineer designs and runs the path from code to production, independent of technology — the delivery pipeline as the enforcer of the methodology's quality gates, reproducible builds and the supply chain, environments and their autonomy rules, infrastructure as code with plan/apply discipline, deployment protection for production, secrets wiring, dev-environment parity, observability as code, dependency and version maintenance, the walking skeleton's platform half, and runbooks. Use for scaffolding, pipeline, infrastructure, environment, observability and maintenance work.
---

# Practice: Platform

The platform is the machinery that turns a commit into a running, observable, recoverable system. Its job in SDD is to make the methodology's rules **automatic**: what the contracts require, the pipeline enforces.

## 1. Principles

1. **Everything as code**: pipelines, infrastructure, environments, dashboards, alerts, dev environments. Nothing important lives only in a console.
2. **Reproducible by default**: the same commit always produces the same artifact. Pin versions of dependencies, tools, base images and pipeline steps, and record what was built from what.
3. **Fast and trustworthy feedback**: the pipeline is the developer's tightest loop. It must be quick, parallel and never flaky, or people (and agents) learn to ignore it.
4. **Least privilege everywhere**: pipeline jobs, deploy identities and runtime identities get only what they need, preferably short-lived.
5. **Plan freely, apply carefully**: previews of change are free; changes with real-world effects follow the autonomy classes.
6. **Production is observable and recoverable before it is live.**

## 2. The pipeline enforces the methodology

Every change to an `sdd/*` branch or pull request runs the gates the contracts define:

| Gate | Enforces | Blocking |
|---|---|---|
| Format, lint, static checks (incl. pipeline and container definitions) | Conventions | Yes |
| Type checks (where the stack has them) | Correctness at boundaries | Yes |
| Full test suite with real dependencies; machine-readable results and coverage | The definition of done; evidence for Verify | Yes |
| Diff coverage vs the base branch | `engineering.diff_coverage_min` | Yes |
| Contract tests against the built system | Contracts are the source of truth | Yes |
| Fitness functions (every `FF-nn`) | The architecture | Yes |
| Supply chain: dependency audit, secret scanning, software bill of materials, artifact scanning | `supply_chain.block_on` | Critical vulnerabilities and any secret block, unless an accepted `RISK-nn` lists the issue |
| Traceability (`sdd.py trace`) | Spec ↔ test ↔ result links | From Verify |

Prove every pipeline change twice: a run that passes, and a deliberately broken commit that fails for the right reason.

## 3. Builds, artifacts and the supply chain

- One build produces one immutable, versioned artifact, which is promoted unchanged through environments. Never rebuild per environment.
- Artifacts are minimal, run as non-privileged users, and contain no secrets or build tooling.
- Every artifact has a bill of materials and a scan result, and its provenance (what source, which pipeline) is recorded.
- Third-party pipeline steps are pinned to immutable references.

## 4. Environments and autonomy

| Environment | Deploy | Changes to existing resources | New resources or spend |
|---|---|---|---|
| dev | Autonomous | Autonomous | D3 |
| staging | Autonomous | Autonomous | D3 |
| production | **G3**, then a protected deployment that requires a human approval in the deployment system itself | G3 | D3 |

The hard stop for production lives **in the deployment system** (a protected environment with a required human reviewer and restricted source branches), not just in instructions. It is configured during scaffolding. Environments are as similar as cost allows: same artifact, same configuration shape, production-like data volume in staging.

## 5. Infrastructure as code

- One state per environment, stored remotely, locked during changes. Modules are reusable; environments compose them.
- **Plan freely**: formatting, validation and previews are autonomous. Attach the preview summary (adds, changes, destroys) and a **monthly cost estimate** to the task.
- **Any preview that adds or destroys resources is D3**, whatever the environment. Replacing a stateful resource counts as a destroy.
- Changes to existing dev/staging resources (no adds, no destroys) apply through the pipeline. Production applies only after G3.
- Never apply from an interactive shell; applies run in the pipeline from the reviewed preview.
- Protect data stores from accidental destruction; use explicit moves for refactors; detect drift on a schedule and treat it as a defect.

## 6. Secrets

Wire **references**, never values. The application reads secrets from a managed store or runtime injection, and the pipeline authenticates to clouds with short-lived federated identities instead of stored keys. A new secret exposed to the application is reviewed by security-engineer (D2). Creating secrets in production accounts is a human action (D3).

## 7. Developer environment parity

Every project gets a reproducible development environment (a dev container or equivalent) with the runtime, tools, scanners and local dependencies (database, message capture) the pipeline uses. It is also the recommended sandbox for autonomous agent sessions. If a check passes locally but fails in the pipeline, that is a parity defect: fix the environment, not the check.

## 8. Observability as code

From the design's failure modes and the SLO catalog, wire:
- instrumentation and collection (logs, metrics, traces, correlation);
- dashboards per service (SLIs, rate/errors/duration, saturation, dependencies);
- **alerts as code** on SLO burn rate and user-visible symptoms, each linked to a runbook section.

Prove each alert fires on a simulated symptom in staging.

## 9. Dependency and version maintenance

Keep the system current so security fixes are cheap:
- automated update proposals, grouped by ecosystem, on a schedule;
- patch-level updates of development tools merge on green;
- runtime updates go through normal review (new runtime packages through dependency review);
- runtimes, base images and major frameworks are tracked against their end-of-life dates, and upgrades are planned as debt items before support ends;
- deprecation warnings from dependencies become debt items, not noise.

## 10. Walking skeleton (scaffold)

The platform half of the first slice of a new project:
- **`.sdd/commands.yaml` first, as its own task**: register the project's commands by purpose for the technologies in `.sdd/stack.yaml` (install, format, lint, typecheck, test with machine-readable output, coverage, migrate, run, build, scan, pipeline-lint, infra-plan, deploy-nonprod, cloud-read, …). Commands only become usable after the architect's review and integration (the guard reads the registry from the feature branch), so this task comes before every task that needs them. The same rule applies later: new tooling is registered in a small task before the tasks that use it. Never register production deploys or infrastructure applies;
- repository layout per the conventions, with formatter, linter, type and test configuration;
- the AC tagging mechanism configured;
- liveness and readiness endpoints;
- ignore rules (including `.claude/worktrees/`);
- the development environment (§7);
- the pipeline with every gate from §2, proven to pass and fail;
- the build artifact;
- the protected production environment;
- the first fitness function;
- a deploy to dev, if a dev environment has been approved.

## 11. Runbooks

`docs/runbooks/<service>.md`:
- what the service is;
- its dashboards;
- for each alert: what it means, first checks, mitigation, rollback;
- how to deploy and roll back;
- whom to involve.

Write the runbook when the service or alert is added, never after the first incident.

## 12. Local verification

Run every check locally before handoff. If a tool isn't available locally or in the dev environment, report that check as **"not run locally"** with what is needed, and never claim it passed. The pipeline runs everything regardless.
