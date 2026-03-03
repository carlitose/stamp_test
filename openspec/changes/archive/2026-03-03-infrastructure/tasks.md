## 1. Terraform Base

- [x] 1.1 Create `terraform/main.tf` — AWS provider config (eu-south-1), terraform required version
- [x] 1.2 Create `terraform/variables.tf` — sender_email (required), aws_region (default), project_name (default)

## 2. S3 Bucket

- [x] 2.1 Create `terraform/s3.tf` — S3 bucket with unique name, prefix placeholder objects

## 3. Lambda Function

- [x] 3.1 Create `terraform/lambda.tf` — archive_file data source for packaging src/lambda/
- [x] 3.2 Add IAM role with least-privilege policy (S3, SES, CloudWatch Logs) to lambda.tf
- [x] 3.3 Add Lambda function resource with Python 3.12, 128MB, 60s timeout, SENDER_EMAIL env var
- [x] 3.4 Add aws_lambda_permission for S3 to invoke Lambda

## 4. S3 Event Notification

- [x] 4.1 Create `terraform/s3_notification.tf` — S3 bucket notification on uploads/*.csv triggering Lambda

## 5. SES

- [x] 5.1 Create `terraform/ses.tf` — SES email identity verification for sender_email

## 6. Outputs and Examples

- [x] 6.1 Create `terraform/outputs.tf` — bucket_name, bucket_arn, lambda_function_name, lambda_function_arn, upload_command
- [x] 6.2 Create `terraform/terraform.tfvars.example` — example values with comments

## 7. Verification

- [x] 7.1 Run `terraform init` and verify provider download
- [x] 7.2 Run `terraform validate` and verify no errors
- [x] 7.3 Run `terraform fmt -check` and verify formatting
