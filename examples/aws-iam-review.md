# Worked example: AWS IAM review

This example uses synthetic names and account identifiers. It demonstrates the review method only and is not evidence from a real environment.

## Proposed change

An application deployment role is given the following inline policy so a CI workflow can update one ECS service:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ecs:*",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "*"
    }
  ]
}
```

## Guardrail review

**Risk level:** High

**Intended scope:** Update the `payments-api` ECS service in a synthetic staging account.

**Observed blast radius:** The policy can manage every ECS resource visible to the role and pass any IAM role in the account. In combination, these permissions could allow the workflow to launch a task with a more privileged role.

**Key findings:**

1. `ecs:*` includes destructive and unrelated actions that are not required for a service deployment.
2. `Resource: "*"` does not constrain the change to the intended cluster and service.
3. Unrestricted `iam:PassRole` creates a privilege-escalation path.
4. The proposal does not identify the task execution role or task role that the workflow is expected to pass.
5. No environment boundary is shown in the policy.

## Safer direction

Start from the actions observed in the deployment process rather than granting the whole ECS service. A typical service deployment may need a subset such as:

- `ecs:DescribeServices`;
- `ecs:DescribeTaskDefinition`;
- `ecs:RegisterTaskDefinition`;
- `ecs:UpdateService`;
- `iam:PassRole` for the exact task execution role and task role.

Where an ECS action supports resource-level permissions, scope it to the intended cluster, service, and task-definition family. Restrict `iam:PassRole` to the named roles and add the `iam:PassedToService` condition:

```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": [
    "arn:aws:iam::111122223333:role/staging-payments-task-execution",
    "arn:aws:iam::111122223333:role/staging-payments-task"
  ],
  "Condition": {
    "StringEquals": {
      "iam:PassedToService": "ecs-tasks.amazonaws.com"
    }
  }
}
```

The exact ECS resource scoping should be verified against the AWS IAM service authorization reference because support differs by action.

## Validation plan

1. Run the policy through IAM Access Analyzer policy validation.
2. Review the CI workflow to confirm the exact API actions it performs.
3. Test in a non-production account with CloudTrail enabled.
4. Confirm the workflow can register the intended task definition and update only the staging service.
5. Add a negative test showing that it cannot update another service or pass an unrelated role.
6. Review CloudTrail events after the test and remove unused permissions.

## Rollback

Keep the previous working policy version available during the staging test. If the deployment fails because a required permission is missing, restore the previous version temporarily, use CloudTrail to identify the denied action, and add only the narrowly required permission before testing again.

## Recommendation

Do not approve the wildcard policy. Replace it with an action- and resource-scoped policy, restrict `iam:PassRole`, validate it in staging, and use observed API activity to tighten it further.
