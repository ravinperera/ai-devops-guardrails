# Changelog

Notable changes to AI DevOps Guardrails are summarised by capability rather than by every commit. This repository provides portable agent instructions, review skills, examples and credential-free checks; the entries below do **not** imply that an AI agent enforces a policy at runtime or that any production environment has been validated.

## Unreleased

No version tag or GitHub release has been published for this repository. The items below are an untagged development summary, not a claimed release.

### Guardrails and review guidance

- Added canonical [DevOps guardrails](AGENTS.md), [Claude Code instructions](CLAUDE.md), Copilot instructions and reusable review skills for Terraform, GitHub Actions, AWS IAM, deployment readiness and secrets.
- Added a [security model](docs/security-model.md) and [limitations guide](docs/limitations-and-verification.md) distinguishing AI review advice from verified evidence and human approval.
- Added [operational stop conditions and rollback guidance](docs/operational-stop-conditions.md) and [multi-agent handoff controls](docs/multi-agent-delegation.md) to keep risky or delegated actions within approved boundaries.
- Added fictional before-and-after [DevOps review examples](examples/reviews/), a [refusal guide](docs/refusal-examples.md) and a [non-enabled GitHub Agentic Workflow example](docs/github-agentic-workflows.md).

### Verification and maintainability

- Added [credential-free checks](docs/validation.md) for text hygiene, selected high-confidence credential patterns, repository-local Markdown links, YAML syntax and Python script compilation, with regression tests.
- Added [adapter-policy consistency checks](docs/validation.md) and a machine-readable [synthetic evaluation corpus](examples/evaluation-corpus.json). Corpus structure validation is **not** evidence of model-specific guardrail pass rates.
- Added [installation guidance](docs/installation.md), [contribution instructions](CONTRIBUTING.md), issue forms and a pull-request template for focused, reviewable changes.

Existing validation checks do not replace security review, independent approval, live-provider testing or deployment verification. See the [repository commit history](https://github.com/ravinperera/ai-devops-guardrails/commits/main) for the exact chronology.
