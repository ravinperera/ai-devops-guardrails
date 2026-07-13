# Threat model

This document describes the main risks addressed by the AI DevOps guardrails. It is intentionally vendor-neutral and applies to coding agents that can read repositories, propose changes, run commands, or interact with delivery systems.

## Scope

The model covers AI-assisted changes to infrastructure as code, CI/CD, cloud access, containers, Kubernetes, networking, secrets handling, deployment automation, and operational scripts.

It does not assume that an AI agent is trusted, correct, or isolated from untrusted repository content.

## Assets to protect

- production availability and integrity
- credentials, tokens, keys, certificates, and sensitive configuration
- cloud accounts, IAM roles, service identities, and deployment permissions
- source code, build artifacts, container images, and dependencies
- infrastructure state and configuration
- logs, audit trails, approvals, and change records
- customer, employee, and operational data

## Trust boundaries

Important boundaries include:

1. **User to agent** — prompts may be incomplete, mistaken, or overly broad.
2. **Repository to agent** — files, comments, issues, generated code, and documentation may contain untrusted instructions.
3. **Agent to tools** — shell, Git, cloud, CI/CD, and deployment tools can turn suggestions into real changes.
4. **Non-production to production** — validation in one environment does not prove safety in another.
5. **Third-party dependencies** — actions, modules, images, packages, and scripts may be compromised or change over time.
6. **Agent output to reviewer** — confident explanations may still omit risk, invent validation, or understate blast radius.

## Threats and mitigations

| Threat | Example | Required mitigations |
|---|---|---|
| Prompt injection | A repository file instructs the agent to ignore security rules or disclose secrets | Treat repository content as untrusted; keep higher-priority safety rules; surface conflicting instructions; never reveal credentials |
| Secret disclosure | The agent prints environment variables, copies a key into code, or includes a token in logs | Redact sensitive values; use secret managers; scan diffs and logs; avoid real credentials in examples |
| Excessive permissions | A generated IAM policy uses broad wildcards or a workflow receives write access it does not need | Apply least privilege; scope resources and actions; use short-lived credentials; review trust policies and permission boundaries |
| Unsafe command execution | The agent runs destructive shell, Terraform, cloud, or Kubernetes commands | Prefer read-only and dry-run commands; require explicit scope; block ambiguous destructive actions; define rollback before execution |
| Production blast radius | A small configuration change affects shared networking, DNS, databases, or deployment roles | Identify accounts, regions, services, and environments touched; stage changes; use approvals and protected environments |
| Supply-chain compromise | A workflow pins an untrusted action, downloads an installer, or adopts an unreviewed module | Pin trusted dependencies; review provenance; avoid `curl | sh`; scan dependencies and artifacts; minimise new dependencies |
| Misleading validation | The agent claims success without running checks or validates only syntax | Separate planned checks from executed checks; capture command results; verify post-deployment health and observability |
| Hidden persistence | A change adds scheduled jobs, credentials, users, backdoors, or broad federation trust | Review identity, startup, scheduled, webhook, and trust changes explicitly; require human approval for persistence mechanisms |
| Data loss or corruption | A migration, retention change, state operation, or deletion is irreversible | Confirm backups and restore tests; use previews; protect state; require explicit approval and a tested rollback path |
| Review bypass | The agent weakens branch protection, approvals, tests, logging, or environment gates | Treat control weakening as high risk; require independent review; reject changes whose purpose is to bypass governance |

## Security assumptions

These guardrails assume:

- repositories use normal branch and pull-request review controls
- production credentials are not directly available to every agent session
- human reviewers remain accountable for high-risk changes
- validation tools and test environments are reasonably representative
- audit logs are retained outside the agent's control

When these assumptions are false, the risk level should be raised and agent permissions reduced.

## Residual risks

The guardrails cannot guarantee that an agent will identify every dependency, understand undocumented production behaviour, detect all malicious content, or produce a correct rollback plan. Human review, access controls, isolated environments, backups, monitoring, and incident response remain necessary.

## Review trigger

Revisit this threat model when the repository adds new agent capabilities, deployment targets, cloud accounts, identity providers, autonomous execution, production write access, or third-party integrations.
