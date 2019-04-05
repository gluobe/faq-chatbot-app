# ---------------------------------------------------------------------------------------------------------------------
# CREATE AN ELB
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_lb" "lb" {
  name       = "${var.name}"
  internal           = false
  subnets            = ["${var.subnet_ids}"]
  security_groups    = ["${aws_security_group.lb_sg.id}"]
  load_balancer_type = "application"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE A SECURITY GROUP THAT CONTROLS WHAT TRAFFIC CAN GO IN AND OUT OF THE ELB
# ---------------------------------------------------------------------------------------------------------------------

resource "aws_security_group" "lb_sg" {
  name        = "${var.name}"
  description = "The security group for the ${var.name} ELB"
  vpc_id      = "${var.vpc_id}"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "80"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
