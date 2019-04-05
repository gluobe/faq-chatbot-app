# ---------------------------------------------------------------------------------------------------------------------
# IAM role for task definition
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role" "task-def-iam-role" {
  name = "test_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

# ---------------------------------------------------------------------------------------------------------------------
# task definition
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_ecs_task_definition" "task-def" {
  family = "${var.name}-task-def"
  requires_compatibilities = ["${var.requires_compatibilities}"]
  cpu = "${var.task_cpu}"
  memory = "${var.task_memory}"
  task_role_arn = "${aws_iam_role.task-def-iam-role.arn}"
  execution_role_arn = "arn:aws:iam::292242131230:role/ecsTaskExecutionRole"
  container_definitions = <<DEFINITION
[
  {
    "name": "${var.container_name}",
    "image": "${var.image}",
    "essential": true,
    "cpu": 128,
    "portMappings": [
      {
        "containerPort": ${var.containerPort},
        "hostPort":  ${var.hostPort}
      }]
  }
]
DEFINITION
}
