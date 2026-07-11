# Security Model

AI DevOps Guardrails is an instruction-layer project. It does not grant access, run deployments or enforce security controls by itself.

Its purpose is to make AI coding agents review DevOps changes with a production-safety mindset before suggesting or applying changes.

## Threats considered

- accidental secret exposure
- overly broad IAM permissions
- unsafe GitHub Actions workflows
- unreviewed production deployments
- destructive Terraform or shell changes
- missing rollback paths
- missing validation and observability
- over-engineered infrastructure changes
- unsafe examples copied into real systems

## Trust assumptions

The guardrails assume:

- a human remains responsible for final approval
- production changes still follow the organisation's change-management process
- credentials are stored in approved secret managers
- destructive actions require explicit human approval
- CI/CD and cloud permissions are independently controlled

## Non-goals

This project does not:

- replace security review
- replace SAST, IaC scanning or secret scanning tools
- replace cloud IAM controls
- replace production approvals
- guarantee that an AI agent will behave safely in every situation

## Recommended companion controls

Use these guardrails alongside:

- branch protection
- required reviews
- secret scanning
- dependency scanning
- IaC scanning such as Checkov, tfsec or Terrascan
- GitHub Actions environment protection
- OIDC instead of long-lived cloud keys
- AWS IAM Access Analyzer
- least-privilege deployment roles
- audit logging and alerting

## Safe adoption path

1. Start with read-only review prompts.
2. Use the guardrails in non-production repositories first.
3. Add validation commands to pull requests.
4. Add secret scanning and IaC scanning.
5. Add production deployment approvals.
6. Only allow write-capable agents in tightly scoped repositories.
