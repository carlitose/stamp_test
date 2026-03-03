## 1. Create State Bucket

- [x] 1.1 Create S3 bucket `csv-processor-tfstate` in `eu-west-3` via AWS CLI
- [x] 1.2 Enable versioning on the state bucket

## 2. Configure Backend

- [x] 2.1 Add `backend "s3"` block to `terraform/main.tf`
- [x] 2.2 Run `terraform init -migrate-state` to move local state to S3
- [x] 2.3 Verify migration: `terraform plan` shows "No changes"

## 3. Cleanup and Deploy

- [x] 3.1 Delete duplicate bucket `csv-processor-e5dcaed0` created by failed CI run
