## ADDED Requirements

### Requirement: Terraform state stored in S3
The system SHALL store Terraform state in an S3 bucket (`csv-processor-tfstate`) in the `eu-west-3` region with versioning enabled.

#### Scenario: State bucket exists with versioning
- **WHEN** the state bucket is checked
- **THEN** `csv-processor-tfstate` EXISTS in `eu-west-3` with versioning set to `Enabled`

#### Scenario: Backend configured in main.tf
- **WHEN** `terraform init` is run (locally or in CI/CD)
- **THEN** Terraform uses the S3 backend at `s3://csv-processor-tfstate/terraform.tfstate`

### Requirement: State is shared between local and CI/CD
The system SHALL allow both local Terraform CLI and GitHub Actions to read and write the same state file.

#### Scenario: Local apply followed by CI/CD plan
- **WHEN** a developer runs `terraform apply` locally
- **AND** GitHub Actions runs `terraform plan`
- **THEN** GitHub Actions SHALL see no changes (state is in sync)

#### Scenario: CI/CD apply followed by local plan
- **WHEN** GitHub Actions runs `terraform apply`
- **AND** a developer runs `terraform plan` locally
- **THEN** local Terraform SHALL see no changes (state is in sync)

### Requirement: Existing state migrated without resource recreation
The system SHALL migrate the existing local state to S3 without destroying or recreating any AWS resources.

#### Scenario: State migration preserves resources
- **WHEN** `terraform init -migrate-state` is executed
- **THEN** all 11 existing resources SHALL appear in `terraform plan` as "No changes"
