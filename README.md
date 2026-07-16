# AI DevOps Guardrails

Safe DevOps rules and review workflows for AI coding agents.

AI agents are fast. Production is fragile.

This project gives Claude Code, Codex, GitHub Copilot, Cursor, Windsurf, Cline and other coding agents a senior DevOps review layer before they touch Terraform, AWS IAM, GitHub Actions, Docker, Kubernetes, secrets, DNS, networking or deployment scripts.

The rule is simple:

> Make the smallest safe infrastructure change. Know the blast radius. Protect secrets. Prefer rollbackable changes. Never trade production safety for speed.

## Why this exists

AI coding agents can generate infrastructure changes quickly, but DevOps work has different risk from normal application code. A small-looking change can affect production access, data, networking, deployments, compliance, cost, observability or incident response.

These guardrails help an agent slow down at the right moments and ask the senior-platform-engineer questions first:

- Is this change actually required?
- Can an existing module, workflow or runbook already solve it?
- What is the production blast radius?
- Could this expose secrets or widen access?
- Is the change reversible?
- How will we validate it before and after deployment?
- What monitoring, logs or alerts prove it worked?

## Core ladder

Before changing infrastructure, CI/CD or operational code, the agent should stop at the first safe option:

```text
1. Does this need to change at all?
2. Can existing configuration, modules, scripts or workflows already do it?
3. Can this be solved with a smaller config change instead of new infrastructure?
4. Can the change be made read-only, dry-run or non-production first?
5. Is the blast radius understood?
6. Are secrets, IAM, DNS, networking, data and production paths protected?
7. Is there a rollback and validation plan?
8. Only then: make the smallest safe change.
```

## Included guardrails

| Guardrail | Purpose |
|---|---|
| `AGENTS.md` | Vendor-neutral always-on rules for AI coding agents |
| `CLAUDE.md` | Claude Code-friendly project instructions |
| `.github/copilot-instructions.md` | GitHub Copilot repository instructions |
| `skills/devops-review` | General DevOps change review |
| `skills/terraform-audit` | Terraform and IaC risk review |
| `skills/github-actions-review` | GitHub Actions workflow safety review |
| `skills/aws-iam-review` | AWS IAM least-privilege review |
| `skills/deployment-readiness` | Production deployment readiness checklist |
| `skills/secrets-check` | Secrets and sensitive-data exposure review |

## Quick start

Copy the instruction file that your agent supports into your project:

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
cp CLAUDE.md /path/to/your/project/CLAUDE.md
mkdir -p /path/to/your/project/.github
cp .github/copilot-instructions.md /path/to/your/project/.github/copilot-instructions.md
```

Then ask your agent to use one of the review workflows:

```text
Use the DevOps guardrails to review this Terraform change before committing it.
```

```text
Run a GitHub Actions safety review on this workflow.
```

```text
Check this IAM policy for least-privilege and privilege-escalation risk.
```

```text
Create a deployment-readiness review for this production change.
```

## Example review output

A good AI-agent review should return something like this:

```text
Risk level: Medium
Blast radius: ECS service deployment role and staging workload only
Production impact: None expected, staging first
Secrets risk: No secrets found, but environment variables should be loaded from Secrets Manager
IAM risk: Role uses wildcard logs permissions; narrow to specific log group ARN
Rollback: Revert workflow change and redeploy previous task definition
Validation: terraform validate, terraform plan, workflow dry run, staging deployment, CloudWatch log check
Recommendation: Safe to proceed after IAM scope reduction
```

For a complete walkthrough, see the [worked AWS IAM review](examples/aws-iam-review.md), which identifies wildcard permissions, explains the privilege-escalation path, proposes a safer direction, and records validation and rollback steps.

## What this project is not

This project is not a replacement for human review, security approval, change management or production governance.

It is a practical instruction layer for AI coding agents so they behave more like careful platform engineers and less like fast code generators.

## Safety principles

- Read before changing.
- Prefer existing patterns over new infrastructure.
- Use least privilege by default.
- Never expose secrets in code, logs, pull requests or examples.
- Treat IAM, DNS, networking, databases and production deploys as high-risk.
- Make changes reversible.
- Validate before deployment and verify after deployment.
- Document known trade-offs.

## Repository status

This is an early version. The first goal is to provide portable DevOps guardrails through plain instruction files and reusable skill prompts. Agent-specific plugin manifests and hooks can be added later.

## License

MIT
