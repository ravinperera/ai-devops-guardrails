# Before and After: GitHub Actions OIDC Review

This fictional example shows how to review a workflow that requests AWS credentials through GitHub OIDC.

## Request before guardrails

```text
Make this deployment workflow work for every branch and give it enough AWS permissions to deploy anything.
```

## Risky proposed workflow

```yaml
name: Deploy

on:
  push:

permissions:
  contents: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::111122223333:role/github-deployment
          aws-region: eu-west-2
      - run: terraform apply -auto-approve
```

## Problems the review should identify

- Every branch can start a deployment.
- The workflow requests `contents: write` without a demonstrated need.
- The role and trust-policy conditions are not shown.
- Third-party actions are referenced by mutable tags rather than immutable commit SHAs.
- The workflow applies infrastructure automatically without a reviewed plan or protected environment.
- There is no concurrency control, timeout, rollback guidance or post-deployment verification.

## Guardrail review output

```text
Risk level: Critical
Blast radius: Any AWS resource reachable by the deployment role
Production impact: Unreviewed changes may run from any pushed branch
Secrets risk: OIDC avoids static AWS keys, but a broad trust policy or role can still expose temporary credentials to an untrusted workflow context
IAM risk: Deployment-role permissions and OIDC subject conditions are unknown and may be overly broad
Rollback: Cancel the workflow, identify partial changes, restore the last approved revision and use the service-specific rollback runbook
Validation: Review IAM trust conditions and permissions, pin actions to commits, run formatting/validation/plan, require a protected environment, test role assumption from allowed and denied branches, verify CloudTrail and deployment logs
Recommendation: Do not enable deployment until repository, branch or environment claims are restricted and production apply requires human approval.
```

## Safer workflow direction

```yaml
name: Terraform plan

on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  id-token: write

concurrency:
  group: terraform-plan-${{ github.ref }}
  cancel-in-progress: true

jobs:
  plan:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Check out repository
        uses: actions/checkout@<reviewed-commit-sha>
        with:
          persist-credentials: false

      - name: Configure short-lived AWS credentials
        uses: aws-actions/configure-aws-credentials@<reviewed-commit-sha>
        with:
          role-to-assume: arn:aws:iam::111122223333:role/github-plan-read-only
          aws-region: eu-west-2

      - name: Validate and plan
        run: |
          terraform fmt -check
          terraform validate
          terraform plan -input=false -out=tfplan
```

A separate production workflow should use a protected GitHub environment, a narrower deployment role, an approved immutable revision and an explicit review gate.

## Approval evidence to request

- IAM trust-policy conditions for repository, branch, environment and audience
- Least-privilege role policy
- Immutable action references and update process
- Protected-environment configuration
- Plan and apply separation
- CloudTrail and deployment-log locations
- Service-specific rollback instructions

The placeholder account ID and action SHAs are fictional and must be replaced only after review.
