# Example only. Adjust ARNs, ports and CIDR ranges for your environment.

resource "aws_security_group" "app" {
  name        = "example-app"
  description = "Safer example security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "Allow app traffic from the load balancer security group only"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [var.load_balancer_security_group_id]
  }

  egress {
    description = "Allow HTTPS egress for package/API calls"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Application = "example-app"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_iam_policy" "deployment" {
  name = "example-safer-deployment-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowEcsDeploymentForOneService"
        Effect = "Allow"
        Action = [
          "ecs:DescribeServices",
          "ecs:DescribeTaskDefinition",
          "ecs:RegisterTaskDefinition",
          "ecs:UpdateService"
        ]
        Resource = [
          var.ecs_service_arn,
          var.ecs_task_definition_arn
        ]
      },
      {
        Sid    = "AllowPassOnlyDeploymentTaskRole"
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = var.ecs_task_execution_role_arn
        Condition = {
          StringEquals = {
            "iam:PassedToService" = "ecs-tasks.amazonaws.com"
          }
        }
      }
    ]
  })
}
