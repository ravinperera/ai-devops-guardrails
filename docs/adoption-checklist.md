# Adoption checklist

Use this checklist to introduce the guardrails into an existing repository without overwriting local standards or changing production behaviour unexpectedly.

## 1. Assess the repository

- Identify infrastructure, deployment, CI/CD, IAM, secrets, networking, data, and production-sensitive paths.
- Record the repository's default branch, protected environments, required checks, and deployment owners.
- Find existing agent instruction files such as `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`.
- Review local contribution, security, and change-management requirements before copying anything.

## 2. Choose the smallest useful scope

Start with one instruction surface and one low-risk repository. Do not install every file automatically.

Recommended sequence:

1. Add the vendor-neutral `AGENTS.md` rules.
2. Merge project-specific instructions rather than replacing them.
3. Add only the review skills relevant to the repository.
4. Trial the guardrails on documentation, validation, or non-production changes first.

## 3. Resolve instruction conflicts

- Preserve stricter project-specific security and compliance rules.
- Remove duplicated or contradictory instructions.
- Make repository-specific ownership, environments, commands, and approval gates explicit.
- Never include credentials, internal URLs, account identifiers, or production data in agent instructions.

## 4. Customise safely

Document the repository's:

- approved validation commands
- production and non-production environments
- protected files and directories
- deployment and rollback process
- required reviewers or approvers
- observability checks
- prohibited destructive operations

Keep instructions concise enough that an agent can follow them consistently.

## 5. Validate before rollout

Run at least three representative reviews without allowing automatic deployment:

- a low-risk documentation or configuration change
- an IAM, workflow, or infrastructure change
- a deliberately unsafe example containing excessive permissions or secret exposure

Confirm that the agent identifies blast radius, production impact, secrets risk, IAM impact, rollback, validation, and observability.

## 6. Introduce through normal review

- Create an issue describing the adoption scope and expected benefit.
- Use a dedicated branch and pull request.
- Ask a platform or security owner to review changes affecting production guidance.
- Keep the first rollout reversible and limited to one repository or team.

## 7. Monitor and improve

After adoption, review whether the guardrails:

- prevented unsafe suggestions
- produced actionable rather than generic findings
- caused conflicts with existing tooling
- added excessive review noise
- missed repository-specific risks

Update the instructions when architecture, deployment workflows, ownership, or compliance requirements change.

## Rollback

If the guardrails create conflicting, misleading, or unsafe behaviour:

1. Disable automated use of the affected instruction file.
2. Revert the adoption pull request.
3. Preserve any useful findings in an issue or incident note.
4. Correct the instructions in a new reviewed branch before re-enabling them.
