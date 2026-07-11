# GitHub Copilot Instructions

This repository uses AI DevOps Guardrails.

When suggesting changes to infrastructure, deployment, CI/CD, cloud access, secrets, observability or operational scripts, prioritise safety and reversibility over speed.

## Before suggesting a change

Check whether:

- an existing module, workflow, script or pattern already solves the problem
- the change affects production, IAM, DNS, networking, databases, secrets or shared infrastructure
- the permission scope can be reduced
- the change can be tested in dry-run or non-production first
- rollback is clear

## Preferred suggestions

- small diffs
- least-privilege permissions
- secret-free examples
- existing patterns
- explicit validation commands
- rollback notes for deployment-impacting changes

## Avoid suggestions that

- hardcode tokens, keys, passwords or account IDs
- widen IAM, GitHub Actions or Kubernetes permissions unnecessarily
- disable security checks
- remove logging, monitoring, backup or approval gates
- introduce broad rewrites when a small fix is safer
