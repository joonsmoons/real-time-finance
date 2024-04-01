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

variable repo_name_stocks {
  type = string
}

variable environment {
  type = string
}

variable aws_region {
  type = string
}

resource "aws_ecr_repository" "news_repository" {
  name                 = "${var.environment}-${var.repo_name_news}"
  image_tag_mutability = "IMMUTABLE"

  tags = {
      environment = var.environment
      deploy_method = local.deploy_method
  }

}

resource "aws_ecr_repository" "stocks_repository" {
  name                 = "${var.environment}-${var.repo_name_stocks}"
  image_tag_mutability = "IMMUTABLE"

  tags = {
      environment = var.environment
      deploy_method = local.deploy_method
  }

}
