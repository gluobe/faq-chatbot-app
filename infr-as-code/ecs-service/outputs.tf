output "task_arn" {
  value = "${aws_ecs_task_definition.task_def.arn}"
}

output "service_id" {
  value = "${aws_ecs_service.ecs_service.id}"
}

output "iam_role_id" {
  value = "${aws_iam_role.ecs_service_role.id}"
}
