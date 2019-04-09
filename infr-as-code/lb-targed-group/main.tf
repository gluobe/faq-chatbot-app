resource "aws_lb_target_group" "elb-tg" {
  name        = "${var.name}"
  port        = "${var.port}"
  protocol    = "${var.protocol}"
  target_type = "${var.targed_type}"
  vpc_id      = "${var.vpc_id}"
}