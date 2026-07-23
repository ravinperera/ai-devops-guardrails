# Agent Installation Guide

This project is designed to be copied into another repository as a lightweight instruction layer. The current integrations are instruction-based: they guide an agent's behaviour, but they do not grant permissions, enforce approvals, or replace CI and human review.

## Choose the instruction file

| Agent or workflow | Recommended file | Destination |
|---|---|---|
| Generic agent workflow | `AGENTS.md` | Repository root |
| OpenAI Codex | `AGENTS.md` | Repository root |
| Claude Code | `CLAUDE.md` | Repository root |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/copilot-instructions.md` |
| Cursor | `AGENTS.md` | Repository root |

Keep one authoritative copy where possible. If a repository needs several agent-specific files, review them together whenever the guardrails change so that they do not drift or conflict.

## Generic `AGENTS.md` workflow

Copy the vendor-neutral instructions into the target repository:

```bash
cp AGENTS.md /path/to/project/AGENTS.md
```

Start the agent in that repository and explicitly request a guardrail review before allowing edits:

```text
Read AGENTS.md, review the proposed infrastructure change, and stop if the blast radius, rollback, validation, or required approval is unclear.
```

For a monorepo, add narrower `AGENTS.md` files only when a subdirectory genuinely needs different rules. Avoid duplicating the same instructions at several levels.

## OpenAI Codex

Use the repository-root `AGENTS.md` file:

```bash
cp AGENTS.md /path/to/project/AGENTS.md
cd /path/to/project
```

Then ask Codex to review before implementation:

```text
Use the repository guardrails to review this change first. Do not modify files until you have identified the blast radius, validation steps, rollback path, and any human approval required.
```

This is an instruction-file integration. Treat tool permissions, execution approvals, network access, and deployment credentials as separate controls.

## Claude Code

Copy the Claude-oriented instructions into the repository root:

```bash
cp CLAUDE.md /path/to/project/CLAUDE.md
cd /path/to/project
```

Use a review-first prompt:

```text
Review this Terraform or deployment change against CLAUDE.md. Return risks, missing evidence, validation, rollback, and a proceed-or-escalate recommendation before editing.
```

If the project already has a `CLAUDE.md`, merge the guardrails carefully instead of overwriting project-specific build, test, or architecture instructions.

## GitHub Copilot

Copy the repository instructions into `.github`:

```bash
mkdir -p /path/to/project/.github
cp .github/copilot-instructions.md /path/to/project/.github/copilot-instructions.md
```

Check the file into version control so reviewers can see changes to the instructions. Keep the guidance concise and repository-specific, and continue to enforce branch protection, required checks, environment approvals, and least-privilege credentials independently.

Suggested review request:

```text
Review this workflow for OIDC trust, permissions, secret exposure, untrusted input, environment protection, rollback, and post-deployment verification.
```

## Cursor

Cursor can use a repository-root `AGENTS.md`, which keeps the setup portable:

```bash
cp AGENTS.md /path/to/project/AGENTS.md
```

If the repository already uses project rules under `.cursor/rules`, keep those rules focused and reference the same safety principles rather than maintaining conflicting copies. Do not use the legacy `.cursorrules` format for a new setup.

Suggested prompt:

```text
Apply AGENTS.md before changing infrastructure. Explain the smallest safe change and stop if production access, secrets, data, networking, or rollback are not adequately controlled.
```

## Verify the installation

Run a harmless review exercise before relying on the instructions for real work. For example, ask the agent to review a fictional IAM policy with `Action: "*"` and `Resource: "*"`.

A useful response should:

- identify the excessive permissions;
- explain the potential blast radius;
- recommend narrower actions and resources;
- avoid inventing account IDs or production context;
- include validation and rollback steps;
- state when human security or platform approval is required.

If the agent immediately edits files, claims unsupported certainty, or suggests bypassing approvals, tighten the local instructions and tool permissions before using it on production-related work.

## Integration levels

### Instruction tier — available now

Plain Markdown files provide persistent repository guidance. They are portable and reviewable, but they are advisory and depend on the agent loading and following them.

### Skill tier — available now

The `skills/` directory contains focused review workflows for Terraform, GitHub Actions, AWS IAM, deployment readiness, secrets, and general DevOps changes. An agent can be asked to apply the relevant workflow explicitly.

### Plugin or hook tier — future work

Tool-specific adapters may later add commands, hooks, policy checks, or structured outputs. Until a tested adapter exists in this repository, do not assume that copying an instruction file enables enforcement, automatic blocking, or privileged integrations.

## Safe adoption checklist

- Review the copied instructions with the repository owners.
- Remove rules that conflict with approved engineering standards.
- Keep secrets, credentials, customer data, and production logs out of instruction files.
- Test the instructions using fictional or non-production examples.
- Combine instructions with protected branches, CI checks, approvals, and least-privilege access.
- Re-review the files whenever the agent, repository structure, or deployment process changes.
