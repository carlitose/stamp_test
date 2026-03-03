terraform {
  required_version = ">= 1.5"

  backend "s3" {
    bucket = "csv-processor-tfstate"
    key    = "terraform.tfstate"
    region = "eu-west-3"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
