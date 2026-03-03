## Context

Terraform state is currently stored locally in `terraform/terraform.tfstate`. This works for single-developer local deploys but breaks CI/CD: GitHub Actions creates fresh infrastructure on every run because it has no knowledge of existing resources. The first CI/CD run already created a duplicate S3 bucket (`csv-processor-e5dcaed0`) before failing on an existing IAM role.

## Goals / Non-Goals

**Goals:**
- Store Terraform state in S3 so both local CLI and GitHub Actions share the same state
- Enable versioning on the state bucket for rollback protection
- Migrate existing local state to S3 without destroying/recreating resources
- Clean up duplicate resources from the failed GitHub Actions run

**Non-Goals:**
- DynamoDB state locking (single-developer project, not needed)
- Terraform workspaces or multi-environment setup
- Changes to the existing infrastructure resources

## Decisions

### 1. State bucket created via AWS CLI, not Terraform
**Rationale:** Chicken-and-egg problem — Terraform cannot manage the bucket that stores its own state. The state bucket is created once via `aws s3api create-bucket` and never changes.

**Alternative considered:** Using a separate Terraform root module for the state bucket. Rejected — adds complexity for a one-time operation.

### 2. S3 backend without DynamoDB locking
**Rationale:** This is a single-developer project. State locking via DynamoDB prevents concurrent writes, which is unnecessary here. S3 versioning provides sufficient protection against accidental overwrites.

**Alternative considered:** Adding a DynamoDB table for locking. Rejected — unnecessary cost and complexity for a solo project.

### 3. State bucket name: `csv-processor-tfstate`
**Rationale:** Follows the existing project naming convention (`csv-processor-*`). Clear purpose from the name.

### 4. Migration via `terraform init -migrate-state`
**Rationale:** Built-in Terraform command that safely copies local state to the new backend. No manual state manipulation needed.

## Risks / Trade-offs

- **[State bucket deletion]** → Mitigated by S3 versioning. Accidental object deletion can be recovered.
- **[IAM permissions]** → The same AWS credentials used for deploy already have S3 access. No additional IAM policy needed for the state bucket.
- **[Migration failure]** → `terraform init -migrate-state` is atomic. If it fails, local state remains intact. Can retry safely.
