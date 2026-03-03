variable "sender_email" {
  description = "Verified SES sender email address"
  type        = string
}

variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "eu-south-1"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "csv-processor"
}
