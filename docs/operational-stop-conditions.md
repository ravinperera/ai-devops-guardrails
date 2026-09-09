# Operational Stop Conditions and Rollback Runbook

This runbook turns the repository's review principles into explicit operational decisions for AI-assisted DevOps work. It is intentionally provider-neutral and should be adapted to an organisation's own incident, change-management, and production runbooks.

The default rule is conservative: **when required evidence is missing or the observed change is larger than the approved change, stop rather than infer approval.**

## Decision outcomes

Use one of four outcomes when a guardrail is triggered:

| Outcome | Use when | Expected next step |
| --- | --- | --- |
| Proceed | Scope, approval, validation, monitoring, and rollback evidence are all adequate | Continue with the smallest approved change |
| Pause and escalate | Required context, approval, ownership, or validation evidence is missing or ambiguous | Preserve evidence and obtain a human decision before continuing |
| Roll back | A reversible change has produced an unhealthy or materially unexpected result | Restore the last known-good state, then verify recovery |
| Abort | Continuing would require destructive, unauthorised, secret-exposing, or otherwise unsafe behaviour | End the operation and record why it was stopped |

A retry is not a substitute for understanding a failure. Do not repeatedly retry production mutations, destructive operations, authentication changes, or data operations merely because a tool reports a transient-looking error.

## 1. Before any change

Pause and escalate if any of the following is true:

- the target account, subscription, cluster, environment, region, repository, database, or service is unclear;
- a production or shared-service change lacks the approval expected by the organisation's process;
- the requested action exceeds the issue, ticket, pull request, or stated task scope;
- the plan or diff contains an unexpected destroy, replacement, privilege expansion, public exposure, route change, DNS change, or data operation;
- the source revision, plan, policy, or configuration being reviewed is stale compared with the revision that would be applied;
- required secrets would need to be copied into prompts, logs, source files, pull requests, or examples;
- there is no credible rollback path for a change that can materially affect availability, access, data, security, or cost;
- required monitoring or health signals are unavailable, making post-change verification impossible.

Abort rather than continue if the requested action explicitly requires bypassing an approval boundary, disclosing a credential, disabling a safety control without authorisation, or performing a destructive production action outside the approved scope.

## 2. During implementation or review

Stop and reassess when implementation evidence diverges from the approved intent. Examples include:

- files, resources, environments, or accounts outside the expected scope begin changing;
- a Terraform/OpenTofu plan changes from additive or in-place to replacement or destruction;
- an IAM or RBAC change grants broader actions, resources, principals, trust relationships, or pass-role capability than expected;
- a workflow gains write permissions, new credentials, deployment capability, or an unreviewed third-party execution step;
- a networking or DNS change expands reachability beyond the approved boundary;
- tests, policy checks, linters, plans, dry runs, or syntax validation fail;
- the branch or base revision changes after evidence was collected in a way that invalidates that evidence;
- a credential scanner, secret detector, or human reviewer identifies possible sensitive data.

When a validation step fails, record the exact failing check and the smallest useful surrounding context. Do not fabricate a passing result, omit the failure from the handoff, or replace required evidence with a statement that the change "looks safe".

## 3. During deployment or application

Pause new mutations and assess rollback if any expected health signal is unavailable or materially unhealthy. Common triggers include:

- deployment or rollout health checks fail or do not converge within the organisation's normal window;
- error rate, latency, saturation, queue depth, availability, or other service indicators move outside the approved change threshold;
- authentication or authorisation failures appear for previously working users, workloads, or automation;
- logging, metrics, tracing, alerting, or audit evidence disappears when it is required to verify the change;
- a migration, schema operation, state operation, or deployment step reports partial completion;
- the applied resource set differs from the approved plan or change set;
- a rollback prerequisite has become unavailable.

Do not start unrelated remediation while the original change is still poorly understood. First establish whether the safest action is to hold, roll back, or escalate.

## 4. Rollback triggers

Rollback is appropriate when a last known-good state is available and the new state has caused a material regression that can be reversed safely.

| Signal | Default response | Evidence to capture before or during rollback |
| --- | --- | --- |
| Failed health or readiness checks | Stop rollout and restore last known-good release/configuration | failing health output, affected scope, previous version |
| Unexpected permission or reachability expansion | Revert the access/network change | before/after policy or route diff, affected principals or paths |
| Error/latency regression attributable to the change | Roll back the change if the rollback is lower risk than continued exposure | monitoring timestamp, baseline, changed revision |
| Partial or inconsistent deployment state | Pause further mutations; use the service-specific recovery procedure | completed steps, failed step, current state, recovery owner |
| Required verification telemetry missing | Pause; roll back if the change cannot be safely verified | missing signal, expected source, last known healthy evidence |

A rollback itself is a production change. Use the organisation's normal approval and safety requirements unless an established incident procedure explicitly authorises emergency rollback.

## 5. Escalation evidence packet

When pausing or handing work to a human reviewer, provide a compact, reproducible packet rather than a long narrative:

```text
Requested change:
Approved scope / ticket:
Target environment and resource:
Revision reviewed:
Last known-good revision/state:
Exact failed check or unexpected observation:
Expected result:
Observed result:
Blast radius currently known:
Changes already applied, if any:
Rollback option and prerequisites:
Monitoring / audit evidence:
Decision needed from human owner:
```

Remove or redact credentials, tokens, customer data, private keys, sensitive request bodies, and other secrets before including evidence. Prefer stable identifiers, timestamps, command names, and short error excerpts over full logs.

## 6. Post-change verification

A change is not complete merely because an apply, deployment, or command returned success. Confirm the evidence that was defined before the change, such as:

- the intended resource, revision, policy, route, workflow, or deployment is the one now active;
- health checks and relevant service indicators are healthy;
- authentication, authorisation, network reachability, and data paths behave as expected;
- logs, metrics, traces, audit events, and alerts needed for the change remain available;
- no unapproved resources or files changed;
- rollback information still points to a valid last known-good state;
- the issue, pull request, change record, or handoff contains the actual validation result rather than an assumed outcome.

If a required verification step cannot be completed, record the change as **unverified** and escalate instead of reporting it as safely completed.

## 7. Closeout checklist

Before declaring the work complete:

- [ ] Approved scope matches the final diff or applied change.
- [ ] Required checks passed against the revision that was actually used.
- [ ] No secrets or sensitive data were exposed in evidence or logs.
- [ ] Production/shared-service approval requirements were satisfied where applicable.
- [ ] Post-change health and security signals were verified.
- [ ] Any rollback or incident action was recorded with the resulting state.
- [ ] Residual risk, deferred verification, or follow-up work is explicit.
- [ ] The final handoff distinguishes observed evidence from assumptions.

## Relationship to other guardrails

Use this runbook together with the [security model](security-model.md), [threat model](threat-model.md), [refusal examples](refusal-examples.md), and [limitations and required verification](limitations-and-verification.md). Those documents define why an agent should stop; this runbook provides a compact operational pattern for what to do next.
