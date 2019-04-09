terraform {
  required_version = "> 0.9.0"
}
# ---------------------------------------------------------------------------------------------------------------------
#                                                          AWS
# ---------------------------------------------------------------------------------------------------------------------
provider "aws" {
  region = "${var.region}"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE THE task definition
# ---------------------------------------------------------------------------------------------------------------------
module "task_faq_chatbot" {
  source = "./task-def"

  name = "faq_chatbot"
  requires_compatibilities = "EC2"
  container_name = "faq_chatbot"
  image = "292242131230.dkr.ecr.eu-west-2.amazonaws.com/faq_chat:latest"
  containerPort = 3000
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE THE vpc
# ---------------------------------------------------------------------------------------------------------------------
module "vpc_faq_chatbot" {
  source = "./network"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE THE codebuild project
# ---------------------------------------------------------------------------------------------------------------------


module "build_project_faq_chatbot" {
  source = "./codebuild"

  name = "faq-chatbot-build-project"
}

# ---------------------------------------------------------------------------------------------------------------------
# CREATE THE ECS CLUSTER
# ---------------------------------------------------------------------------------------------------------------------
module "ecs_cluster_faq_chatbot" {
  source = "./ecs-cluster"

  name          = "faq-chatbot"
  max_size      = 6
  min_size      = 1
  instance_type = "t2.micro"

  vpc_id = "${module.vpc_faq_chatbot.vpc_id}"

  subnet_ids = [
    "${module.vpc_faq_chatbot.prv_subnet_b_id}",
    "${module.vpc_faq_chatbot.prv_subnet_a_id}"
  ]
}
# ---------------------------------------------------------------------------------------------------------------------
# CREATE elb
# ---------------------------------------------------------------------------------------------------------------------

module "fac_chatbot_elb" {
  source = "./elb"
  subnet_ids = ["${module.vpc_faq_chatbot.pbl_subnet_a_id}","${module.vpc_faq_chatbot.pbl_subnet_b_id}"]
  name              = "faq-chatbot-elb"
  vpc_id = "${module.vpc_faq_chatbot.vpc_id}"
  instance_port     = "80"
  health_check_path = "health"
}
# ---------------------------------------------------------------------------------------------------------------------
# CREATE lb target group
# ---------------------------------------------------------------------------------------------------------------------

module "fac_chatbot_lb_tg" {
  source = "./lb-targed-group"

  name              = "faq-chatbot-tg"
  vpc_id = "${module.vpc_faq_chatbot.vpc_id}"
}
# ---------------------------------------------------------------------------------------------------------------------
# CREATE ecs service
# ---------------------------------------------------------------------------------------------------------------------
module "faq_chatbot_service" {
  source = "./ecs-service"

  name = "faq_chatbot"
  ecs_cluster_id = "${module.ecs_cluster_faq_chatbot.ecs_cluster_id}"

  image = "292242131230.dkr.ecr.eu-west-2.amazonaws.com/faq_chat"
  image_version = "latest"
  cpu = 1024
  memory = 768
  desired_count = 2
  
  container_port = "3000"
  host_port = "80"
  elb_tg_arn = "${module.fac_chatbot_lb_tg.target_group_arn}"

  num_env_vars = 1
  env_vars = "${map("RACK_ENV", "production")}"
  task_def_arn = "${module.task_faq_chatbot.task_def_arn}"
}

