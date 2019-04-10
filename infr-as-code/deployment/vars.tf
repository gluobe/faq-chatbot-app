variable "name" {
  description = "The name of the application."
}
variable "compute_platform" {
  description = "The compute platform can either be ECS, Lambda, or Server. Default is ECS."
  default = "ECS"
}