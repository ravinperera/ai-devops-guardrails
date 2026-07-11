# AWS IAM Review

Use this skill when reviewing AWS IAM policies, roles, permission boundaries, trust policies, service-linked roles or OIDC federation.

## Goal

Reduce access risk while preserving the minimum permissions required for the workload.

## Check for

- wildcard actions such as `*`, `iam:*`, `sts:*`, `s3:*`, `kms:*` or `secretsmanager:*`
- wildcard resources where specific ARNs are possible
- privilege-escalation paths such as `iam:PassRole`, `iam:CreatePolicyVersion`, `iam:AttachRolePolicy`, `lambda:UpdateFunctionCode`, `cloudformation:*`
- broad trust policies or missing conditions
- OIDC trust without strict `aud` and `sub` conditions
- cross-account access without clear purpose
- missing permission boundaries for automation roles
- long-lived access keys where role assumption should be used
- secrets access broader than required
- KMS permissions without key or condition scoping

## Required output

```text
Risk level: Low | Medium | High | Critical
Principal: user/role/service identity affected
Policy scope: actions/resources/conditions reviewed
Trust boundary: who can assume or use this access
Privilege-escalation risk: findings or none observed
Secrets/data access risk: findings or none observed
Least-privilege fixes:
- action item
Recommended policy changes:
- exact narrowing suggestion
Validation: how to test without overgranting
Recommendation: proceed / proceed after fixes / do not proceed
```

## Safer defaults

- Prefer role assumption over long-lived credentials.
- Scope GitHub OIDC roles to repository, branch/environment and audience.
- Scope resources to known ARNs where possible.
- Use conditions for tags, regions, source account, source ARN and external ID where appropriate.
- Separate deployment, read-only and break-glass permissions.
