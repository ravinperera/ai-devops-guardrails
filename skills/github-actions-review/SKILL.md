# GitHub Actions Review

Use this skill when reviewing GitHub Actions workflows, reusable workflows, deployment jobs or CI/CD automation.

## Goal

Prevent CI/CD from becoming the easiest path to production compromise.

## Check for

- overly broad `permissions`, especially `contents: write`, `id-token: write`, `packages: write` or `actions: write`
- missing top-level `permissions`
- unpinned third-party actions
- actions pinned only to mutable branches such as `main` or `master`
- secrets printed to logs or passed to untrusted actions
- pull request workflows that expose secrets to forked code
- deployment jobs without environment protection or approvals
- direct production deployment from unprotected branches
- unsafe use of `pull_request_target`
- `curl | bash`, `eval`, unquoted shell variables or unchecked script failures
- missing concurrency controls for deployments
- missing artifact integrity or build provenance checks

## Required output

```text
Risk level: Low | Medium | High | Critical
Workflow scope: workflow files and jobs affected
Trigger risk: events that can run the workflow
Permission risk: GitHub token and OIDC scope issues
Secrets risk: exposure or misuse concerns
Deployment risk: environment, approvals, branch protection, rollback
Findings:
- [severity] finding and recommended fix
Recommended workflow hardening:
- action item
Validation: how to test safely
Recommendation: proceed / proceed after fixes / do not proceed
```

## Safer defaults

Prefer:

```yaml
permissions: read-all
```

Then grant only the minimum extra permissions per job.

Prefer OIDC for cloud deployments instead of long-lived cloud credentials.

Use protected environments for production deployments.
