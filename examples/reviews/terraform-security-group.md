# Before and After: Terraform Security Group Review

This fictional example shows how the guardrails should turn a broad infrastructure request into a bounded, reviewable change.

## Request before guardrails

```text
Open the application security group so the new integration can connect. Apply the Terraform change.
```

## Risky proposed change

```hcl
resource "aws_security_group_rule" "integration_ingress" {
  type              = "ingress"
  security_group_id = aws_security_group.application.id
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_blocks       = ["0.0.0.0/0"]
}
```

## Problems the review should identify

- The source network is unrestricted.
- The target environment and integration owner are not stated.
- There is no evidence that inbound access is required instead of a private or outbound-only pattern.
- The proposed action includes `terraform apply` before a reviewed plan.
- Monitoring, expiry and rollback expectations are missing.

## Guardrail review output

```text
Risk level: High
Blast radius: HTTPS ingress to every workload attached to the application security group
Production impact: Potential public exposure of the application endpoint
Secrets risk: No secret is shown, but unrestricted access may expose authenticated or internal endpoints
IAM risk: Not applicable to this change
Rollback: Remove the rule and apply the previously reviewed Terraform configuration
Validation: Confirm the integration source ranges, run terraform fmt/validate, review terraform plan, deploy to non-production, test approved and denied sources, inspect VPC Flow Logs and application access logs
Recommendation: Do not proceed with 0.0.0.0/0. Confirm whether private connectivity, an allowlisted CIDR set, prefix list or security-group reference can meet the requirement.
```

## Safer direction

```hcl
variable "integration_source_cidrs" {
  description = "Approved source CIDRs supplied by the integration owner"
  type        = list(string)

  validation {
    condition = (
      length(var.integration_source_cidrs) > 0 &&
      !contains(var.integration_source_cidrs, "0.0.0.0/0")
    )
    error_message = "Provide at least one approved source CIDR; public ingress is not allowed."
  }
}

resource "aws_security_group_rule" "integration_ingress" {
  type              = "ingress"
  security_group_id = aws_security_group.application.id
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_blocks       = var.integration_source_cidrs
  description       = "Approved integration HTTPS ingress"
}
```

## Approval evidence to request

- Named service and business owner
- Environment and affected workloads
- Approved source ranges or private-connectivity design
- Expiry or periodic review date
- Reviewed Terraform plan
- Non-production connectivity test
- Rollback owner and command sequence

The example is illustrative only. Real network changes require environment-specific architecture and security review.
