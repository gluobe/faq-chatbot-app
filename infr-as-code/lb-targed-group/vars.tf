variable "name" {
  description = "The name of de targed group"
}
variable "vpc_id" {
  description = "The identifier of the VPC in which to create the target group."
}
variable "targed_type" {
  description = "The type of target that you must specify when registering targets with this target group."
  default = "instance"
}
variable "protocol" {
  description = "The protocol to use for routing traffic to the targets. Should be one of \"TCP\", \"TLS\" , \"HTTP \" or \"HTTPS\"."
  default = "HTTP"
}
variable "port" {
  description = "The port on which targets receive traffic, unless overridden when registering a specific target. "
  default = 80
}