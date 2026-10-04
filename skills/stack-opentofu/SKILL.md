---
name: stack-opentofu
description: Infrastructure-as-code expertise for SDD with OpenTofu/Terraform — module and environment layout, remote state with locking, provider and module pinning, variables and outputs, plan review (add/change/destroy), cost estimation, drift detection, safe changes (lifecycle rules, moved blocks), secrets handling, and policy checks. Use when writing or reviewing infra/ code or environment plans.
---

# Stack: OpenTofu / Terraform

> Verify provider resources and arguments in current docs (context7 / provider registry) before use.

## Layout

```
infra/
  modules/<component>/     # reusable, no provider config, typed variables, documented outputs
  envs/dev|staging|production/
    main.tf  backend.tf  versions.tf  variables.tf  terraform.tfvars (no secrets)
```

- **Remote state** with locking, one state per environment; state contains sensitive data — restrict access.
- **Pin** `required_version`, providers (`~>` minor) and modules (exact version or commit).
- Tag/label every resource with project, environment, feature.

## Safe changes

- Read every plan: **adds**, **changes**, **destroys/replacements**. Any add or destroy → D3 decision package (with cost); replacements of stateful resources are destroys.
- `prevent_destroy` on data stores; `moved {}` blocks for refactors instead of destroy/create; `create_before_destroy` where downtime matters.
- No secrets in `.tf` or `.tfvars`; reference secret-store entries; mark sensitive outputs.
- Drift: scheduled `plan` in CI; drift is a finding, fixed in code.

## Checks

`tofu fmt -check`, `tofu validate`, `tofu plan` (saved and summarized), a linter (tflint) and a policy/security scanner (trivy config or checkov) in CI. Cost estimate (e.g. infracost or provider pricing) attached to plans that add resources.
