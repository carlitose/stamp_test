## Why

The Lambda code is complete and tested, but it can't run without AWS infrastructure. We need Terraform to provision the S3 bucket, IAM role, Lambda function, SES configuration, and S3 event notification that ties everything together. Without this, the pipeline exists only as local code.

## What Changes

- Add `terraform/main.tf` — provider configuration and backend
- Add `terraform/variables.tf` — input variables (sender email, region, project name)
- Add `terraform/s3.tf` — S3 bucket with uploads/, processed/, reports/ prefixes
- Add `terraform/lambda.tf` — Lambda function, IAM role with least-privilege policy, Lambda packaging
- Add `terraform/ses.tf` — SES email identity for the sender
- Add `terraform/s3_notification.tf` — S3 event notification triggering Lambda on uploads/*.csv
- Add `terraform/outputs.tf` — useful outputs (bucket name, Lambda ARN, upload command)
- Add `terraform/terraform.tfvars.example` — example values with no secrets

## Capabilities

### New Capabilities
- `terraform-s3`: S3 bucket provisioning with prefix structure for uploads, processed, and reports
- `terraform-lambda`: Lambda function deployment with IAM least-privilege role and S3 event trigger
- `terraform-ses`: SES sender email identity configuration

### Modified Capabilities
<!-- None -->

## Impact

- **Files**: 8 new Terraform files in `terraform/`
- **Dependencies**: Terraform CLI (external), AWS credentials configured
- **Systems**: Creates AWS resources (S3, Lambda, IAM, SES, S3 notification)
- **Downstream**: `cicd-and-docs` change will automate `terraform apply` via GitHub Actions
