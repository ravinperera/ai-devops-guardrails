# Agent installation examples

This repository provides portable instruction files and reusable review prompts. Start with the instruction file your coding agent already understands, then copy only the review skills your team intends to use.

## Generic `AGENTS.md` workflow

Use this option for agents that read repository-level `AGENTS.md` instructions.

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

Commit the file with the project so every contributor and supported agent receives the same baseline safety rules.

## Claude Code

Claude Code can read project instructions from `CLAUDE.md`.

```bash
cp CLAUDE.md /path/to/your/project/CLAUDE.md
```

Keep the file at the repository root. The current integration is instruction-based: it supplies project guidance but does not install hooks, plugins, or automatic approval controls.

## Codex

Use the vendor-neutral `AGENTS.md` file for Codex-compatible repository instructions.

```bash
cp AGENTS.md /path/to/your/project/AGENTS.md
```

You can then ask Codex to apply a specific review workflow, for example:

```text
Use the DevOps guardrails to review this Terraform change before committing it.
```

This is an instruction-only setup. It does not automatically execute policy checks or replace repository branch protections.

## GitHub Copilot

GitHub Copilot repository instructions live under `.github`.

```bash
mkdir -p /path/to/your/project/.github
cp .github/copilot-instructions.md \
  /path/to/your/project/.github/copilot-instructions.md
```

Review the copied file before adoption and keep organisation-specific requirements in your own repository.

## Cursor

Cursor can use a repository instruction file through its supported rules mechanism. The most portable starting point is to copy the content of `AGENTS.md` into the project-level rules file supported by your installed Cursor version.

Because Cursor rule formats can change, verify the current Cursor documentation before choosing the final filename or metadata format. Do not assume this repository installs a Cursor plugin or enforces the rules automatically.

## Reusable review skills

The folders under `skills/` are prompt-based review workflows. Copy only the workflows relevant to your project, preserving their directory structure where practical.

```bash
mkdir -p /path/to/your/project/skills
cp -R skills/devops-review /path/to/your/project/skills/
cp -R skills/terraform-audit /path/to/your/project/skills/
```

A copied skill is guidance for the agent, not an executable security control. Human review, CI validation, access controls, deployment approvals, and change-management processes still apply.

## Integration tiers

| Tier | What it provides | Current status |
|---|---|---|
| Instruction | Repository-level safety rules such as `AGENTS.md`, `CLAUDE.md`, and Copilot instructions | Available now |
| Skill | Reusable prompt workflows under `skills/` for focused reviews | Available now |
| Plugin or hook | Agent-specific automation, enforcement, or lifecycle integration | Not provided unless a documented adapter is added |

Always treat an integration as instruction-only unless this repository explicitly documents a working adapter for that agent and version.
