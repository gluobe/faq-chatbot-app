# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN ELB
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_lb" "elb" {
  name                      = "${var.name}"
  internal           = false
  subnets                   = ["${var.subnet_ids}"]
  security_groups           = ["${aws_security_group.elb_sg.id}"]
  load_balancer_type = "application"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE A SECURITY GROUP THAT CONTROLS WHAT TRAFFIC CAN GO IN AND OUT OF THE ELB
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_security_group" "elb_sg" {
  name        = "${var.name}"
  description = "The security group for the ${var.name} ELB"
  vpc_id      = "${var.vpc_id}"
}

resource "aws_security_group_rule" "all_outbound_all" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.elb_sg.id}"
}

resource "aws_security_group_rule" "all_inbound_all" {
  type              = "ingress"
  from_port         = "${var.lb_port}"
  to_port           = "${var.lb_port}"
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = "${aws_security_group.elb_sg.id}"
}
