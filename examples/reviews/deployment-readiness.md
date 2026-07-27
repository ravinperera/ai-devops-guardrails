# Before and After: Deployment Readiness Review

This fictional example shows how to respond when an AI agent is asked to deploy a service without enough operational context.

## Request before guardrails

```text
Deploy the new container to production now. The build passed, so it should be fine.
```

## Missing information

- The image digest and source commit are not identified.
- There is no staging result or production change record.
- Health checks, alarms and log locations are not stated.
- Database compatibility and migration requirements are unknown.
- Capacity, scaling and dependency readiness are not confirmed.
- No rollback owner, previous revision or stop condition is defined.

## Guardrail review output

```text
Risk level: High
Blast radius: Production service, its callers and downstream dependencies
Production impact: Possible outage, failed health checks, elevated errors or incompatible data changes
Secrets risk: Confirm the task uses approved secret references and does not log sensitive environment variables
IAM risk: Confirm the runtime and deployment roles are unchanged or separately reviewed
Rollback: Restore the previous immutable task definition or image digest; do not roll back a database migration until its reversibility is confirmed
Validation: Verify image provenance, staging evidence, health checks, alarms, capacity, dependency status, migration plan, canary behaviour, rollback path and post-deployment metrics
Recommendation: Pause deployment until the readiness evidence is complete and a named operator owns the rollout and rollback.
```

## Safer deployment request

```text
Prepare a production deployment-readiness review only; do not deploy.

Release:
- Commit: 0123456789abcdef0123456789abcdef01234567
- Image digest: sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
- Staging result: passed smoke tests and 30-minute error-rate observation

Scope:
- One stateless API service
- No schema migration
- No IAM, DNS, network or secret changes

Rollout:
- 10% canary for 15 minutes
- Stop if 5xx rate exceeds 1% or p95 latency increases by 20%
- Previous task definition: api-service:42

Evidence:
- Dashboard: fictional-monitoring-link
- Logs: fictional-log-group
- Change owner: platform-on-call
```

## Expected readiness decision

The agent should return one of:

- **Ready:** evidence is complete, risk is understood and approvals are present.
- **Ready with conditions:** specific low-risk gaps must be completed before rollout.
- **Not ready:** a high-risk unknown, missing approval or unsafe rollback path blocks deployment.

It should not deploy, merge or weaken controls unless explicitly authorised through the normal change process.

## Reviewer checklist

- Immutable release identifier recorded
- Staging and test evidence attached
- No hidden infrastructure or permission changes
- Health checks and alarms verified
- Capacity and downstream dependencies confirmed
- Migration and data compatibility reviewed
- Canary or phased rollout defined
- Stop conditions are measurable
- Previous known-good revision available
- Named deployment and rollback owners confirmed
- Post-deployment verification window agreed

All identifiers and links in this example are fictional.
