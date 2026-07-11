# Claude Code Instructions

Use the AI DevOps Guardrails in this repository whenever a task touches infrastructure, CI/CD, cloud access, secrets, deployment automation, observability or production operations.

## Working style

Before editing, read the relevant files and identify the real operational path. Do not patch only the visible symptom if the shared module, workflow or script is the safer fix.

Prefer:

- smallest safe change
- existing project patterns
- reversible infrastructure
- least privilege
- dry-run or non-production validation first
- clear rollback notes

Avoid:

- broad rewrites
- new dependencies without clear need
- speculative abstractions
- hardcoded secrets
- widening IAM or workflow permissions for convenience
- destructive commands without clear safety checks

## Required review before edits

For Terraform, IAM, GitHub Actions, Docker, Kubernetes, shell scripts, DNS, networking, databases or production deployment logic, briefly state:

```text
Risk level:
Blast radius:
Secrets/IAM impact:
Rollback path:
Validation plan:
```

Then make the smallest safe change.

## Validation

After non-trivial edits, suggest or run the smallest relevant checks available in the project, such as:

```bash
terraform fmt -check
terraform validate
terraform plan
shellcheck script.sh
docker build .
yamllint .github/workflows/deploy.yml
```

Do not invent successful command results. If a check was not run, say so.
