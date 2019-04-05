variable "name" {
  description = "De naam van de Task definition."
}
variable "requires_compatibilities" {
  description = "A set of launch types required by the task. The valid values are EC2 and FARGATE."
  default = "FARGATE"
}
variable "task_cpu" {
  description = "The number of cpu units used by the task."
  default = "1 vCPU"
}
variable "task_memory" {
  description = "The amount (in MiB) of memory used by the task."
  default = "2"
}
variable "containerPort" {
  description = "The port exposed on the container"
  default = 80
}
variable "hostPort" {
  description = "The port on your host"
  default = 80
}

variable "container_name" {
  description = "The name of the container"
}
variable "image" {
  description = "The image to use (ex: repository-url/image:tag)"
}
