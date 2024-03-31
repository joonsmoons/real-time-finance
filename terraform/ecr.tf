terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
}

locals {
  deploy_method = "terraform"
}

variable repo_name_news {
  type = string
}

variable repo_name_indicies {
  type = string
}

variable environment {
  type = string
}

variable aws_region {
  type = string
  default = "ap-northeast-2"
}

resource "aws_ecr_repository" "news_repository" {
  name                 = "${var.environment}-${var.repo_name_news}"
  image_tag_mutability = "IMMUTABLE"

  tags = {
      environment = var.environment
      deploy_method = local.deploy_method
  }

}

resource "aws_ecr_repository" "indicies_repository" {
  name                 = "${var.environment}-${var.repo_name_indicies}"
  image_tag_mutability = "IMMUTABLE"

  tags = {
      environment = var.environment
      deploy_method = local.deploy_method
  }

}
