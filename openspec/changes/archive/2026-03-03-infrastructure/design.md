## Context

The Lambda code (`src/lambda/`) is complete with 7 modules and 30 passing tests. Terraform must package this code and deploy it alongside all supporting AWS resources. The master spec defines the target architecture: S3 → event notification → Lambda → SES, all within AWS free tier.

Region: `eu-south-1` (Milan). All resources in a single region, single AWS account.

## Goals / Non-Goals

**Goals:**
- All infrastructure provisioned with a single `terraform apply`
- IAM least-privilege: Lambda role can only access its specific S3 bucket and SES
- No hardcoded credentials or secrets in Terraform files
- Useful outputs for testing (bucket name, upload command)
- Lambda packaging automated via Terraform `archive_file` data source

**Non-Goals:**
- Remote state backend (local state is fine for this project scope)
- Multiple environments (dev/staging/prod)
- Custom domain or Route53 configuration
- VPC or networking (Lambda runs in default VPC-less mode)
- CloudWatch alarms or monitoring dashboards

## Decisions

### 1. Terraform structure: separate files by resource type

**Decision**: One `.tf` file per resource group (`s3.tf`, `lambda.tf`, `ses.tf`, etc.).

**Rationale**: Clear organization matching the master spec's project structure. Easy to find and modify individual resources. Standard Terraform convention.

### 2. Lambda packaging: `archive_file` data source

**Decision**: Use Terraform's `archive_file` to zip `src/lambda/` at plan time.

**Rationale**: No external build step needed. Terraform handles the zip creation. The Lambda code is pure Python with no compiled dependencies (boto3 is provided by the Lambda runtime), so a simple zip of the source files works.

### 3. S3 bucket: single bucket with prefix-based organization

**Decision**: One S3 bucket with `uploads/`, `processed/`, `reports/` prefixes (not separate buckets).

**Rationale**: Simpler to manage, matches the spec. The event notification filters on `uploads/` prefix. Free tier covers a single bucket easily.

### 4. SES: identity verification only, no domain

**Decision**: Verify only the sender email identity, not a full domain.

**Rationale**: Simplest SES setup. The sender email must be verified before deployment (manual step). In sandbox mode, recipients must also be verified — this is documented in the README (cicd-and-docs change).

### 5. S3 event notification: direct Lambda invocation (not SNS/SQS)

**Decision**: S3 → Lambda directly via `aws_s3_bucket_notification`.

**Rationale**: Simplest path. No need for a queue or topic for a single consumer. Lambda handles retries natively.

### 6. Variables: sender_email required, rest with defaults

**Decision**: `sender_email` is the only required variable. Region, project name have defaults.

**Rationale**: Keeps `terraform apply` simple — only one value to provide. The sender email is the only truly environment-specific value.

## Risks / Trade-offs

- **[Local state]** → State file is local, not shared. Acceptable for a single-developer project. If lost, `terraform import` can recover.
- **[SES sandbox]** → New AWS accounts are in SES sandbox mode. Both sender and recipient emails must be verified. This is a manual prerequisite documented in outputs.
- **[Lambda cold start]** → Python 3.12 Lambda with minimal dependencies has fast cold starts (~200ms). Not a concern for this use case.
- **[S3 notification permission]** → Lambda needs `aws_lambda_permission` to allow S3 to invoke it. Easy to forget — included in `lambda.tf`.
