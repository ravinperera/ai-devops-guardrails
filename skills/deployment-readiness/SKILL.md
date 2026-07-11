# Deployment Readiness

Use this skill before a production or production-adjacent deployment.

## Goal

Confirm that a change is safe, observable and reversible before deployment.

## Required output

```text
Deployment readiness: Ready / Ready after fixes / Not ready
Risk level: Low | Medium | High | Critical
Change summary: what is being deployed
Environment: dev/staging/production/shared
Blast radius: users/services/accounts affected
Dependencies: upstream/downstream systems
Rollback plan: exact rollback steps
Validation before deployment:
- check
Validation after deployment:
- check
Monitoring:
- logs, metrics, dashboards, alerts
Approval/change control:
- required approvals or tickets
Open risks:
- risk and mitigation
Recommendation: proceed / wait / do not deploy
```

## Readiness checklist

Check whether:

- the change has been tested outside production
- database or state changes are backward compatible
- rollback is realistic and quick
- feature flags or staged rollout are available where useful
- monitoring and logs can confirm success
- alerts exist for failure modes
- deployment has an owner
- support teams know the change window if required
- secrets and IAM changes are reviewed
- customer/client impact is understood

## Do not mark ready if

- rollback is unknown
- production impact is unknown
- secrets are exposed
- IAM is broader than necessary
- validation depends only on manual observation
- destructive changes are mixed with unrelated changes
