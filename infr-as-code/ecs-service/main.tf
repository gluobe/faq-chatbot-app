# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN ECS SERVICE TO RUN A LONG-RUNNING ECS TASK
# We also associate the ECS Service with an ELB, which can distribute traffic across the ECS Tasks.
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_ecs_service" "ecs_service" {
  name            = "${var.name}"
  cluster         = "${var.ecs_cluster_id}"
  task_definition = "${var.task_def_arn}"
  desired_count   = "${var.desired_count}"
  iam_role        = "${aws_iam_role.ecs_service_role.arn}"
  launch_type     = "${var.launch_type}"

  deployment_minimum_healthy_percent = "${var.deployment_minimum_healthy_percent}"
  deployment_maximum_percent         = "${var.deployment_maximum_percent}"

  deployment_controller {
    type = "${var.deployment_controller}"
  }

  load_balancer {

    target_group_arn       = "${var.elb_tg_arn}"
    container_name = "${var.name}"
    container_port = "${var.container_port}"
  }

  depends_on = ["aws_iam_role_policy.ecs_service_policy"]

}
/*
# ---------------------------------------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# nieuwe taskdef voorbeeld
# ---------------------------------------------------------------------------------------------------------------------
resource "aws_ecs_service" "ecs_service2" {
  name                = "${var.name}"
  task_definition     = "${var.task_def_arn}"
  desired_count       = 3
  launch_type         = "${var.launch_type}"
  scheduling_strategy = "${var.scheduling_strategy}"
  cluster             = "${var.ecs_cluster_id}"
  iam_role            = "${aws_iam_role.ecs_service_role.arn}"

  deployment_controller {
    type = "${var.deployment_controller}"
  }

  load_balancer {
    elb_name         = ""
    target_group_arn = "$nog in te vullen"
    container_name   = "faq-chat moet van de taskdef komen"
    container_port   = 3000
  }
}
*/
# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN IAM ROLE FOR THE ECS SERVICE
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role" "ecs_service_role" {
  name               = "${var.name}"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_service_role.json}"
}

data "aws_iam_policy_document" "ecs_service_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs.amazonaws.com"]
    }
  }
}

# ---------------------------------------------------------------------------------------------------------------------
# ATTACH IAM PERMISSIONS TO THE IAM ROLE
# This IAM Policy allows the ECS Service to communicate with EC2 Instances.
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_iam_role_policy" "ecs_service_policy" {
  name   = "ecs-service-policy"
  role   = "${aws_iam_role.ecs_service_role.id}"
  policy = "${data.aws_iam_policy_document.ecs_service_policy.json}"
}

data "aws_iam_policy_document" "ecs_service_policy" {
  statement {
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "elasticloadbalancing:Describe*",
      "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
      "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
      "ec2:Describe*",
      "ec2:AuthorizeSecurityGroupIngress",
    ]
  }
}


