# DevOps change review

> Copy this template into an issue, pull request, or change record. Replace every placeholder and mark unknowns explicitly.

## Change summary

- **Change:**
- **Reason:**
- **Owner:**
- **Planned window:**
- **Related issue / change record:**

## Scope

- **Repositories and files:**
- **Services and components:**
- **Accounts / subscriptions / projects:**
- **Regions:**
- **Environments:**
- **Users or customers affected:**

## Risk assessment

- **Risk level:** Low / Medium / High / Critical
- **Blast radius:**
- **Production impact:**
- **Availability risk:**
- **Data-loss or corruption risk:**
- **Security or compliance impact:**
- **Cost impact:**
- **Key assumptions and unknowns:**

## Secrets and identity

- **Secrets exposure risk:**
- **New or changed credentials:**
- **IAM / RBAC changes:**
- **Trust-policy or federation changes:**
- **Least-privilege review:**
- **Credential lifetime and rotation:**

## Dependency and supply-chain review

- **New actions, modules, packages, images, or scripts:**
- **Version or digest pinning:**
- **Source and provenance checked:**
- **Known vulnerabilities reviewed:**

## Planned validation

List checks that must run before deployment. Do not present planned checks as completed evidence.

- [ ] Syntax, formatting, and static validation
- [ ] Unit or policy tests
- [ ] Infrastructure plan or dry run
- [ ] Security and secret scanning
- [ ] Non-production deployment or rehearsal
- [ ] Peer review completed

Additional commands or checks:

```text
<commands and expected results>
```

## Executed evidence

Record only checks that actually ran.

| Check | Environment | Result | Evidence / link | Executed by |
|---|---|---|---|---|
|  |  |  |  |  |

## Deployment plan

1. 
2. 
3. 

- **Approval gate:**
- **Deployment identity:**
- **Expected duration:**
- **Stop conditions:**

## Rollback plan

- **Rollback owner:**
- **Rollback trigger:**
- **Exact rollback steps:**
- **Expected recovery time:**
- **Backup or restore point verified:** Yes / No / Not applicable
- **Rollback tested:** Yes / No; evidence:

## Observability and post-change verification

- **Logs to inspect:**
- **Metrics and dashboards:**
- **Alerts expected or suppressed:**
- **Health checks:**
- **Business or user validation:**
- **Monitoring period:**
- **Success criteria:**

## Approvals

- **Technical reviewer:**
- **Security / platform reviewer:**
- **Service owner:**
- **Change approval:**

## Final recommendation

- **Decision:** Proceed / Proceed after fixes / Do not proceed
- **Required fixes or conditions:**
- **Residual risk accepted by:**
- **Review date:**
