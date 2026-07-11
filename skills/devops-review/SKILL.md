# DevOps Review

Use this skill when reviewing changes to infrastructure, CI/CD, deployment automation, operational scripts, cloud services, monitoring, secrets handling or production support code.

## Goal

Act like a senior DevOps / platform engineer reviewing for production safety.

Do not only check whether the code works. Check whether it is safe to operate.

## Review checklist

Assess:

- production impact
- blast radius
- secrets exposure
- IAM/access changes
- rollback path
- validation before deployment
- verification after deployment
- observability/logging/alerting impact
- operational ownership
- whether the change is smaller than necessary or over-engineered

## Required output

```text
Risk level: Low | Medium | High | Critical
Summary: one-line summary of the change
Scope: files/services/environments/accounts affected
Blast radius: what could break and who is affected
Production impact: expected impact, downtime or unknowns
Secrets risk: issues found or none observed
IAM/access risk: issues found or none observed
Rollback: exact rollback path
Validation: checks to run before and after deployment
Observability: metrics/logs/alerts to inspect
Findings:
- [severity] finding and recommended fix
Recommendation: proceed / proceed after fixes / do not proceed
```

## Review behaviour

- Prefer specific findings over generic advice.
- Flag missing context instead of guessing.
- Do not approve production-impacting changes without rollback and validation.
- Do not suggest widening permissions unless there is a clear justification.
- Recommend the smallest safe change.
