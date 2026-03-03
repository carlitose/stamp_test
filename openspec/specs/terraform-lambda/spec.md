## ADDED Requirements

### Requirement: Lambda function deployment
Terraform SHALL deploy the Lambda function with Python 3.12 runtime, packaging the code from `src/lambda/`.

#### Scenario: Lambda created with correct configuration
- **WHEN** `terraform apply` is run
- **THEN** a Lambda function SHALL be created with Python 3.12 runtime, 128MB memory, 60s timeout, and the SENDER_EMAIL environment variable

### Requirement: Lambda code packaging
Terraform SHALL automatically package `src/lambda/` into a zip file using the `archive_file` data source.

#### Scenario: Code packaged at plan time
- **WHEN** `terraform plan` is run
- **THEN** the Lambda source code SHALL be zipped from `src/lambda/` directory

### Requirement: IAM least-privilege role
Terraform SHALL create an IAM role for the Lambda with least-privilege permissions.

#### Scenario: Lambda can access only its S3 bucket
- **WHEN** the IAM role is created
- **THEN** it SHALL grant s3:GetObject, s3:PutObject, s3:DeleteObject, s3:CopyObject permissions only on the specific bucket ARN

#### Scenario: Lambda can send emails via SES
- **WHEN** the IAM role is created
- **THEN** it SHALL grant ses:SendEmail permission

#### Scenario: Lambda can write CloudWatch logs
- **WHEN** the IAM role is created
- **THEN** it SHALL grant logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents permissions

### Requirement: S3 invocation permission
Terraform SHALL grant S3 permission to invoke the Lambda function.

#### Scenario: Lambda permission for S3
- **WHEN** `terraform apply` is run
- **THEN** an `aws_lambda_permission` resource SHALL allow the S3 bucket to invoke the Lambda function
