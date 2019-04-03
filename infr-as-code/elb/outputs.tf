output "elb_naam" {
  value = "${aws_lb.elb.name}"
}

output "elb_dns_name" {
  value = "${aws_lb.elb.dns_name}"
}

output "security_group_id" {
  value = "${aws_security_group.elb_sg.id}"
}
