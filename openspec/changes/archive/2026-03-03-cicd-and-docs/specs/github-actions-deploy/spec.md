## ADDED Requirements

### Requirement: Manual deploy workflow
The project SHALL include a GitHub Actions workflow triggered manually via `workflow_dispatch`.

#### Scenario: Manual trigger available
- **WHEN** a user navigates to the Actions tab in the GitHub repository
- **THEN** a "Deploy" workflow SHALL be available for manual triggering

### Requirement: Terraform deployment steps
The workflow SHALL execute `terraform init`, `terraform plan`, and `terraform apply -auto-approve` in sequence.

#### Scenario: Successful deployment
- **WHEN** the workflow is triggered with valid AWS credentials
- **THEN** it SHALL initialize Terraform, show the plan, and apply the infrastructure changes

### Requirement: AWS credentials from secrets
The workflow SHALL use GitHub Secrets for AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) and sender email (`SENDER_EMAIL`).

#### Scenario: Secrets configured
- **WHEN** the workflow runs
- **THEN** it SHALL pass AWS credentials as environment variables and `SENDER_EMAIL` as a Terraform variable
