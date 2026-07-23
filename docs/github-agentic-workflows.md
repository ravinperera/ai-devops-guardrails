# GitHub Agentic Workflows: Safe Adoption Guide

GitHub Agentic Workflows entered public preview on 11 June 2026. They let maintainers describe a reasoning-based workflow in Markdown and compile it into a standard GitHub Actions workflow.

This repository includes a conservative example for selecting one explicitly approved, low-risk issue and preparing a draft pull request:

- [`examples/github-agentic-workflows/issue-to-draft-pr.md`](../examples/github-agentic-workflows/issue-to-draft-pr.md)

The example is stored outside `.github/workflows/`, so it is **not active** when copied or cloned from this repository.

## Security model

The example uses several independent controls rather than relying on the prompt alone:

| Control | Purpose |
| --- | --- |
| Manual `workflow_dispatch` trigger | Prevent unattended scheduled execution in the starter version |
| Read-only agent permissions | Keep the reasoning step from writing directly to the repository |
| `safe-outputs` | Separate the agent's requested change from the permission-controlled write operation |
| Draft pull request policy | Require a human decision before the work can progress |
| One-PR maximum | Prevent a single run from creating a batch of changes |
| File-count and patch-size limits | Bound the amount of generated change |
| `allowed-files` | Restrict changes to documentation, examples, tests, and Markdown |
| Protected-file fallback | Avoid silently changing repository governance and agent-instruction files |
| `agent-safe` issue label | Require a maintainer to approve the issue category before the agent considers it |
| Explicit high-risk exclusions | Reject IAM, secrets, DNS, production infrastructure, migrations, destructive commands, and broad refactors |
| Required risk summary | Put blast radius, rollback, validation, access impact, and observability in the draft PR body |

GitHub documents that safe outputs run separately from the read-only agent job and that threat detection evaluates proposed output before permitted writes are applied. These platform controls are useful defence in depth, but they do not replace repository review, branch protection, CI, or production change governance.

## Activate the example

Review the current GitHub documentation and the source file before enabling it. The public-preview schema may evolve.

1. Install and initialise the current `gh aw` extension for the target repository.
2. Create an `agent-safe` label. Apply it only after a maintainer confirms that an issue is limited to low-risk documentation, examples, tests, or non-destructive validation.
3. Copy the example into the active workflow directory:

   ```bash
   mkdir -p .github/workflows
   cp examples/github-agentic-workflows/issue-to-draft-pr.md \
     .github/workflows/issue-to-draft-pr.md
   ```

4. Compile the Markdown source:

   ```bash
   gh aw compile
   ```

5. Review both generated files:

   ```text
   .github/workflows/issue-to-draft-pr.md
   .github/workflows/issue-to-draft-pr.lock.yml
   ```

6. Confirm that the generated workflow grants the agent read permissions only and that the write path is confined to the declared safe output.
7. Commit both files. The generated `.lock.yml` is intentionally version controlled.
8. Run the workflow manually after labelling one suitable issue:

   ```bash
   gh aw run issue-to-draft-pr
   ```

For a first test, use a disposable repository or GitHub Agentic Workflows trial mode rather than a production repository.

## Authentication

GitHub announced that Agentic Workflows can use the built-in `GITHUB_TOKEN`, removing the need for a long-lived personal access token for standard same-repository operations. Engine authentication and billing requirements can still vary, so review the current setup wizard and organisation policy before activation.

Do not introduce a PAT solely to bypass the example's restrictions. When a stronger credential is genuinely necessary, prefer a narrowly scoped GitHub App or fine-grained token, document its exact permissions, and set an owner and expiry process.

## Pre-activation review

Confirm all of the following:

- [ ] The workflow remains manually triggered.
- [ ] The agent job has read-only repository permissions.
- [ ] Only `create-pull-request` is enabled as a write-capable safe output.
- [ ] The pull request is always created as a draft.
- [ ] The maximum number of pull requests is one.
- [ ] File-count and patch-size limits remain conservative.
- [ ] Protected files use fallback or blocking rather than unrestricted writes.
- [ ] The `allowed-files` patterns match the intended repository structure.
- [ ] No cloud, production, customer, or secret-bearing credentials are available to the workflow.
- [ ] Branch protection and required human review remain enabled.
- [ ] Required CI checks will run on bot-created pull requests before merge.
- [ ] The repository has a documented way to disable the workflow quickly.

## Review every generated pull request

A maintainer should verify:

- the issue was genuinely eligible and carried the approval label;
- the diff is limited to the issue's acceptance criteria;
- no prompt-injection text from issues or repository files changed the task;
- no secrets, credentials, unsafe commands, or external data were introduced;
- validation actually ran and the reported output is credible;
- the rollback description is sufficient;
- required CI and security checks completed;
- the change remains low risk.

Do not merge solely because the workflow describes its own output as safe.

## Disable or roll back

To stop future runs:

1. Disable the compiled workflow in the repository's Actions settings, or remove both the Markdown source and generated lock file.
2. Close any unreviewed draft pull requests created by the workflow.
3. Revoke any additional engine or GitHub credentials that were configured only for the workflow.
4. Preserve workflow logs and review notes if an unexpected change occurred.
5. Re-enable only after the root cause and policy gap are understood.

## Important limitations

- Public-preview behaviour and schema can change.
- Prompt and repository content can be untrusted input.
- A small diff can still have a large operational effect.
- PRs created with the default Actions token may not automatically trigger every CI workflow; verify repository behaviour before relying on required checks.
- Safe-output and threat-detection controls reduce risk but cannot prove correctness or production safety.
- This example is intentionally unsuitable for unattended infrastructure, IAM, networking, database, secret, or production changes.

## Official references

- [GitHub Agentic Workflows public preview](https://github.blog/changelog/2026-06-11-github-agentic-workflows-is-now-in-public-preview/)
- [Agentic Workflows and the built-in GITHUB_TOKEN](https://github.blog/changelog/2026-06-11-agentic-workflows-no-longer-need-a-personal-access-token/)
- [Creating GitHub Agentic Workflows](https://docs.github.com/en/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows)
- [GitHub Agentic Workflows frontmatter](https://github.github.com/gh-aw/reference/frontmatter/)
- [Safe outputs for pull requests](https://github.github.com/gh-aw/reference/safe-outputs-pull-requests/)
- [Threat detection](https://github.github.com/gh-aw/reference/threat-detection/)
- [Triggering CI](https://github.github.com/gh-aw/reference/triggering-ci/)