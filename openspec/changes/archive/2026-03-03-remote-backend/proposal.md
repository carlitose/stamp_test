## Why

The deploy from GitHub Actions fails because the Terraform state is only saved locally. Without a shared state, CI/CD and local development cannot coexist. A remote S3 backend is needed to synchronize the state across all deploy sources.

## What Changes

- Create a dedicated S3 bucket for the Terraform state (outside of Terraform code, via CLI)
- Add the `backend "s3"` configuration in `main.tf`
- Migrate the local state to the remote backend
- Delete the duplicate S3 bucket created by the failed GitHub Actions run (`csv-processor-e5dcaed0`)

## Capabilities

### New Capabilities
- `terraform-remote-state`: S3 backend configuration for Terraform remote state, with versioning enabled to protect against accidental overwrites

### Modified Capabilities
- `github-actions-deploy`: The workflow requires no code changes, but will now work correctly thanks to the shared state

## Impact

- `terraform/main.tf` — added `backend "s3"` block
- Local state migrated to S3 — the local `terraform.tfstate` file becomes empty after migration
- Duplicate bucket `csv-processor-e5dcaed0` deleted from AWS
- GitHub Actions deploy becomes functional