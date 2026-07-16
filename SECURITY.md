# Security Policy

## Reporting a security or safety concern

Please report security-sensitive findings privately rather than opening a public issue when the report includes any of the following:

- a guardrail bypass that could cause an AI agent to expose secrets, widen access, or execute unsafe infrastructure changes;
- prompt-injection or instruction-conflict behaviour that defeats the repository's safety rules;
- credentials, tokens, customer data, internal hostnames, or other sensitive information committed to the repository or included in an example;
- a workflow, script, or configuration that could create an exploitable permission or supply-chain weakness.

Use GitHub's **Report a vulnerability** option in the repository Security tab when it is available. If private vulnerability reporting is unavailable, contact the repository owner privately through a verified channel listed on their GitHub profile. Do not include live credentials or working exploit details in a public issue.

## What to include

A useful report should contain:

- the affected file, instruction, workflow, or example;
- the conditions required to reproduce the problem;
- the expected safe behaviour and the observed unsafe behaviour;
- the likely impact and blast radius;
- a minimal reproduction using redacted or synthetic data;
- any suggested mitigation or safer wording.

## Accidental secret exposure

If a credential or secret has been exposed, revoke or rotate it immediately before investigating repository history. Removing a secret from the latest commit is not sufficient because it may remain accessible in earlier commits, caches, forks, logs, or workflow artifacts.

When reporting the incident, identify the type of secret and affected system, but replace the value with a redacted placeholder. Avoid copying the secret into issues, pull requests, screenshots, chat messages, or logs.

## Scope and response

This project contains guidance and templates rather than a hosted service. Reports are assessed based on whether they could materially weaken the safety of AI-assisted DevOps work or expose users who adopt the repository's instructions.

Good-faith reports will be reviewed, and confirmed problems will be addressed through the normal issue and pull-request workflow after sensitive details have been removed. No response-time guarantee is currently offered.
