# Guardrail limitations and required verification

AI-assisted review can improve consistency, but it cannot prove that an infrastructure or deployment change is safe from repository content alone. Treat every review as decision support, not as an approval or a substitute for environment evidence.

## What an agent may not know

An agent reviewing a pull request may not have access to:

- the current deployed state, manual changes, drift, or resources created outside infrastructure as code;
- organization-level service control policies, permission boundaries, identity-provider rules, branch protection, environment protection, or network controls;
- secrets, runtime configuration, feature flags, customer-specific settings, and values injected by external systems;
- the exact versions and behaviour of cloud services, providers, actions, modules, base images, or third-party APIs at deployment time;
- production traffic patterns, quotas, capacity limits, data classifications, legal obligations, maintenance windows, or support coverage;
- dependencies managed in another repository, account, region, cluster, tenant, or vendor platform;
- whether commands shown in documentation were actually executed and whether their output is current.

A confident answer does not remove these unknowns.

## Evidence to request

Before recommending approval for a material change, the review should request or identify relevant evidence such as:

- a current plan, diff, dry-run result, or deployment preview generated from the target environment;
- the exact environment, account, region, cluster, namespace, service, and identities affected;
- current policy validation results and the effective permissions of deployment and workload roles;
- test results from a representative non-production environment;
- rollback steps that have been checked against the current release and data model;
- monitoring queries, dashboards, alerts, and success or stop conditions for the rollout;
- recent dependency, image, and workflow provenance information;
- confirmation from the system owner for assumptions that cannot be verified from code.

The review should label evidence accurately as **provided**, **observed**, **planned**, or **not available**. Planned validation must not be presented as completed validation.

## When to stop and escalate

The agent should stop short of recommending execution and ask for a qualified human decision when:

- the production blast radius cannot be bounded;
- credentials, customer data, regulated data, encryption keys, DNS, identity, or destructive database operations are involved and ownership is unclear;
- the change depends on an unverified assumption about runtime state or effective permissions;
- rollback is impossible, untested, or could cause further data loss;
- the proposed change weakens an existing control without documented risk acceptance;
- validation requires privileged access the reviewer does not have;
- authoritative sources disagree or the relevant platform behaviour may have changed;
- an incident is already in progress and the change could affect containment or evidence preservation.

Escalation is a successful guardrail outcome. It is better to record an unresolved risk than to manufacture certainty.

## Recommended conclusion language

Prefer bounded conclusions:

> The repository-level review found no additional issues within the files examined. Production safety is not yet confirmed because effective IAM permissions and the current deployment plan were not provided. Obtain those items and complete the staging validation before approval.

Avoid absolute statements such as “safe for production” unless the required evidence has been reviewed by the responsible human approver and the conclusion is explicitly scoped to that evidence.
