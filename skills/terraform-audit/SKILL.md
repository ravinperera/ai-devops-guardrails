# Terraform Audit

Use this skill when reviewing Terraform or other infrastructure-as-code changes.

## Goal

Find infrastructure risk before it reaches production.

## Check for

- hardcoded secrets, credentials, account IDs or environment-specific values
- unsafe IAM wildcards such as `Action: *`, `Resource: *` or broad trust policies
- public security groups, open ingress or unrestricted egress without justification
- missing encryption for storage, databases, queues or logs
- missing backups, retention or deletion protection
- unsafe lifecycle rules such as `prevent_destroy = false` on critical resources
- remote state exposure or weak backend configuration
- provider version drift or unpinned modules
- production changes mixed with unrelated refactoring
- missing tags, ownership, cost allocation or environment labels
- resources that should use an existing module instead of one-off code

## Required output

```text
Risk level: Low | Medium | High | Critical
Terraform scope: modules/resources/providers affected
State impact: backend/state/remote-state considerations
Production impact: expected impact or unknowns
IAM/network/data risk: key risks found
Destructive risk: create/update/delete/replacement concerns
Validation:
- terraform fmt -check
- terraform validate
- terraform plan
Findings:
- [severity] finding and fix
Recommendation: proceed / proceed after fixes / do not proceed
```

## Safer defaults

Prefer:

- scoped IAM actions and resources
- environment-specific variables outside committed code
- module reuse
- encryption enabled
- deletion protection for stateful production services
- explicit provider versions
- narrow network access
- separate plans for unrelated changes
