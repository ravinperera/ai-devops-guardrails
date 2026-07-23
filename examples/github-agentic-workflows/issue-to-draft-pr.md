---
description: "Select one explicitly approved low-risk issue and prepare a small draft pull request"
on:
  workflow_dispatch:
permissions: read-all
engine: copilot
tools:
  edit:
  github:
    toolsets: [repos, issues, pull_requests]
safe-outputs:
  max-patch-size: 256
  create-pull-request:
    title-prefix: "[agentic-maintenance] "
    labels: [automation]
    draft: true
    max: 1
    max-patch-files: 5
    max-patch-size: 256
    if-no-changes: warn
    protected-files: fallback-to-issue
    allowed-files:
      - "docs/**"
      - "examples/**"
      - "tests/**"
      - "**/*.md"
---

# Safe issue-to-draft-PR maintenance

Act as a careful repository maintainer. Your job is to select **one** small, useful issue and prepare a draft pull request only when every safety condition below is satisfied.

## Eligible issues

Consider only open issues that:

- carry the `agent-safe` label;
- have clear acceptance criteria;
- can be completed through documentation, examples, tests, or non-destructive validation;
- are small enough for no more than five changed files and a 256 KB patch;
- do not already have an open pull request or active assignee;
- do not require external credentials, production access, private data, or undocumented assumptions.

If no issue qualifies, make no repository changes and report why.

## Always refuse autonomous handling

Do not implement an issue that touches or proposes changes to:

- IAM policies, role trust, permission boundaries, authentication, or authorization;
- secrets, tokens, credentials, customer data, or production logs;
- DNS, certificates, networking, firewalls, load balancers, or WAF controls;
- Terraform apply, state mutation, destructive cloud commands, or production resources;
- database schemas, migrations, backups, retention, or deletion;
- deployment approvals, branch protection, CODEOWNERS, workflow permissions, or security configuration;
- dependency upgrades with uncertain compatibility or security impact;
- broad refactors, generated-code rewrites, or changes outside the issue's explicit scope.

If the issue enters one of these areas, stop and recommend human review instead of creating a patch.

## Working method

1. Read the issue and the smallest relevant repository context.
2. Confirm that the expected files match the `allowed-files` policy.
3. State the intended scope before editing.
4. Make the smallest change that satisfies the acceptance criteria.
5. Do not introduce new dependencies unless the issue explicitly requires one and the change remains low risk.
6. Run only local, non-destructive validation available in the repository.
7. Review the final diff for unrelated changes, secrets, unsafe commands, and protected files.
8. Request one draft pull request through the configured safe output.

## Required pull-request content

The draft pull request body must include:

- `Issue`: the issue number and title;
- `Scope`: files and behaviour changed;
- `Risk level`: Low, or stop without creating the pull request;
- `Blast radius`: what could be affected;
- `Production impact`: expected impact or `None`;
- `Secrets and access`: confirmation that no credentials, IAM, or access controls changed;
- `Validation`: exact checks run and their results;
- `Rollback`: how to revert the change;
- `Observability`: what a reviewer should inspect, or `Not applicable`;
- `Human review required`: explicit confirmation that the pull request is draft and must not be auto-merged.

Never merge, approve, or mark the pull request ready for review.