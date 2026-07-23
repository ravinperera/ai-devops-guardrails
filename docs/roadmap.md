# Agent Adapter Roadmap

The project currently provides portable instruction files and reusable review skills. These are useful guidance, but they are not enforcement plugins and do not automatically block unsafe operations.

This roadmap describes how the project can grow without overstating support or introducing privileged integrations before they are maintainable.

## Guiding principles

- Keep the core guardrails vendor-neutral and readable as plain Markdown.
- Prefer advisory, review-first behaviour before adding automatic execution.
- Add tool-specific integration only when its permissions, failure modes, and rollback path are understood.
- Never require production credentials to test an adapter.
- Treat hooks, shell execution, network access, secrets, and deployment permissions as explicit security boundaries.
- Document exactly what an integration can and cannot enforce.

## Support tiers

### Tier 1: instruction files — available now

The repository currently ships:

- `AGENTS.md` for portable agent instructions;
- `CLAUDE.md` for Claude-oriented repository guidance; and
- `.github/copilot-instructions.md` for GitHub Copilot repository instructions.

These files can be copied into a project and reviewed like any other source-controlled policy. They depend on the selected agent discovering and following the instructions. They do not provide deterministic policy enforcement.

Near-term work for this tier:

- keep equivalent safety principles aligned across instruction files;
- add realistic, fictional examples for common DevOps risks;
- document precedence and conflict handling for repositories with existing instructions; and
- add release notes when a guardrail changes materially.

### Tier 2: reusable review skills — available now, evolving

The `skills/` directory provides focused review workflows for Terraform, GitHub Actions, AWS IAM, deployment readiness, secrets, and general DevOps changes.

Near-term work for this tier:

- define consistent inputs and review output fields;
- add test fixtures for safe, unsafe, and ambiguous changes;
- distinguish observed evidence from assumptions;
- add machine-readable output only where it improves validation without hiding the human-readable reasoning; and
- document when a skill must stop and escalate to a human owner.

### Tier 3: tool-specific adapters — future

An adapter may package the instruction and skill tiers for a particular agent, CLI, IDE, or automation platform. An adapter is considered supported only when this repository contains its implementation, tests, installation guidance, permission model, and maintenance owner.

Until those elements exist, references to a tool in this roadmap are exploratory and must not be presented as supported plugin functionality.

## Candidate adapters

| Candidate | Possible value | Required safety work before support |
|---|---|---|
| Claude Code | Review command, repository hook, or packaged skill workflow | Confirm supported extension points, command permissions, hook failure behaviour, and safe defaults |
| OpenAI Codex | Reusable review workflow or packaged repository skill | Confirm supported packaging, execution boundaries, approval behaviour, and non-interactive failure handling |
| Cursor | Project-rule packaging and repeatable review prompts | Prevent conflict with existing rules, document rule scope, and test instruction discovery |
| OpenCode | Portable command or agent configuration adapter | Confirm stable configuration format, permission boundaries, and version compatibility |
| GitHub Copilot | Path-specific review instructions or reusable prompt workflow | Track feature support by environment and keep branch protection and required checks independent |

Other adapters may be proposed, but portability and maintenance quality are more important than the number of integrations.

## Adapter maturity labels

Every adapter should use one of these labels in its documentation:

- **Experimental** — incomplete, manually tested, and subject to breaking changes.
- **Preview** — documented and tested against named versions, but not yet broadly validated.
- **Supported** — has automated tests, an identified maintainer, upgrade guidance, and a documented security model.
- **Deprecated** — still present for migration, but no longer recommended for new adoption.

A README badge or directory name alone must not imply support.

## Minimum adapter structure

A future adapter should live under `adapters/<tool-name>/` and include, at minimum:

```text
adapters/<tool-name>/
├── README.md
├── SECURITY.md
├── examples/
├── tests/
└── adapter files required by the tool
```

Its README should state:

- supported tool and version range;
- installation and removal steps;
- files and permissions the adapter can access;
- commands or hooks it may execute;
- whether it can make changes or only review them;
- expected failure behaviour;
- validation and rollback steps; and
- known limitations.

## Contribution path for a new adapter

1. Open an issue describing the user problem and why an instruction file alone is insufficient.
2. Link the tool's official extension or configuration documentation.
3. Document the trust boundaries, permissions, execution paths, data handling, and failure modes.
4. Propose the smallest adapter that adds value without requiring broad credentials or automatic production access.
5. Add fictional test fixtures for safe, unsafe, and ambiguous scenarios.
6. Provide installation, upgrade, removal, validation, and rollback instructions.
7. Mark the adapter experimental until automated checks and a maintenance owner are in place.
8. Request review from both a platform-engineering and security perspective before claiming support.

Proposals that only duplicate `AGENTS.md`, add an unmaintained wrapper, or create hidden execution paths should not be accepted.

## Release criteria for supported status

Before an adapter can move to **Supported**, it should have:

- automated validation that runs without production credentials;
- pinned or reproducible dependencies;
- least-privilege defaults;
- explicit approval points for write or execution actions;
- safe handling of untrusted repository content;
- no secret values in logs, examples, fixtures, or generated output;
- documented behaviour when required context is missing;
- a tested uninstall or rollback path;
- version compatibility documentation; and
- an identified maintainer and issue-response expectation.

## Non-goals

The roadmap does not aim to:

- bypass human review, change management, or security approval;
- create an agent with unrestricted shell, cloud, Kubernetes, or production access;
- promise identical behaviour across different AI tools;
- treat model output as deterministic policy enforcement; or
- add integrations solely to increase repository activity.

The core project should remain useful even when no tool-specific adapter is installed.
