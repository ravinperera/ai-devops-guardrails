# Multi-Agent Delegation and Handoff Guardrails

Multi-agent workflows can reduce cognitive load by giving different agents focused roles, but they also create new DevOps risks: authority can expand during delegation, sensitive context can be copied unnecessarily, validation ownership can become unclear, and the connection between a human request and the final change can be lost.

Use these guardrails whenever one agent, subagent, coordinator, reviewer, or automation component hands DevOps work to another.

## Baseline Rules

### 1. Scope each role before delegation

Each agent should receive only the files, tools, environment access, and decision authority required for its assigned task.

A handoff must not silently add:

- broader repository write access;
- cloud, shell, secrets, or production access;
- authority to approve the sender's own work;
- permission to modify infrastructure outside the original request;
- customer, credential, or internal data that the receiver does not need.

If the next step requires broader authority, stop and obtain that authority through the normal human or platform control path.

### 2. Delegation must not increase authority

An agent cannot grant another agent permissions that it did not receive. The receiver's effective authority is the intersection of:

```text
original human/platform authority
AND sender authority
AND receiver role permissions
AND task-specific scope
```

When those boundaries conflict or are unclear, fail closed and escalate rather than guessing.

### 3. Reference state instead of repasting state

Prefer a stable reference such as a commit SHA, pull request, issue, immutable artifact digest, or exact file revision over copying entire files, logs, plans, or chat history into a handoff.

A good handoff says what changed and where the authoritative evidence lives. The receiving agent should verify that reference before acting.

Do not use vague references such as `latest`, `current version`, or `the changes above` for consequential work.

### 4. Keep handoffs small and evidence-focused

Carry only what the receiver needs:

- task and acceptance criteria;
- allowed and prohibited scope;
- authoritative state reference;
- exact validation already performed;
- unresolved risk or question;
- approval still required;
- next safe action.

Do not copy credentials, private keys, access tokens, complete production logs, customer payloads, or unrelated repository context into inter-agent messages.

Use [`templates/agent-handoff.md`](../templates/agent-handoff.md) as a compact starting point.

### 5. Keep implementation, validation, and approval distinct

A second agent can independently validate a change, but agent-to-agent review is not a substitute for required human approval, branch protection, change management, or production controls.

For medium- or high-risk DevOps work, make the responsibility explicit:

```text
implementer -> validator -> required human/platform approval -> execution
```

The validator should evaluate the referenced state, not merely trust the implementer's summary.

### 6. Stop on ambiguous or inconsistent state

Pause delegation and escalate when any of these occurs:

- the requested repository, environment, account, cluster, region, or target is ambiguous;
- the referenced commit, plan, artifact, or file revision cannot be verified;
- working state differs from the handoff's authoritative reference;
- the receiver needs permissions outside the recorded scope;
- validation produces conflicting results or repeatedly fails;
- secrets or unexpectedly sensitive data appear;
- a production, IAM, DNS, database, destructive, or customer-impacting action lacks required approval;
- two agents appear to be making conflicting changes to the same state.

Do not resolve these conditions by broadening permissions or choosing a target based on probability.

## Safe Handoff Sequence

A small, auditable sequence is usually enough:

1. Confirm the task scope and authority boundary.
2. Make the smallest permitted change.
3. Produce a stable state reference, such as a commit SHA.
4. Run the smallest relevant validation and record the result.
5. Create a compact handoff using the template.
6. Have the receiver verify the state reference and scope before continuing.
7. Stop for required human or platform approval before consequential execution.

If there is no useful separation of responsibility or context, prefer one well-scoped agent instead of adding orchestration for its own sake.

## Example

A safe fictional handoff from an implementation agent to a validation agent might state:

```text
Task: Review the Terraform change for staging-only security-group egress.
Authority: Read repository files and run offline Terraform validation only.
Authoritative state: commit <commit-sha>
Changed scope: modules/service/security-group.tf
Validation completed: terraform fmt -check
Open risk: confirm the egress destination is already approved.
Prohibited: apply, cloud login, production changes, IAM changes.
Next action: inspect the referenced diff and run backend-free validation.
```

The receiver should not infer permission to run `terraform apply`, assume production has the same configuration, or request cloud credentials merely because the sender mentioned Terraform.

## Anti-Patterns

Avoid:

- forwarding an entire chat or repository when a commit and short task description are enough;
- allowing a coordinator agent to bypass normal approval because another agent requested it;
- treating an agent's self-review as independent approval;
- passing secrets through natural-language handoffs;
- letting delegated work widen from staging to production without explicit authorization;
- continuing after the authoritative state reference no longer matches the working tree;
- spawning additional agents without a concrete role, verification benefit, or context-reduction reason.

## Relationship to Existing Guardrails

These rules extend the repository's existing least-privilege, rollback, validation, and human-review principles to multi-agent workflows. They do not implement an agent protocol, runtime authorization system, or production orchestration layer. Platform controls must still enforce the actual permissions and approval boundaries.
