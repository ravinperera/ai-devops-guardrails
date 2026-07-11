# Example only. Do not use in production.

resource "aws_security_group" "app" {
  name        = "example-app"
  description = "Risky example security group"
  vpc_id      = var.vpc_id

  ingress {
    description = "Risky: open SSH to the world"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Risky: unrestricted egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_policy" "deployment" {
  name = "example-risky-deployment-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}
