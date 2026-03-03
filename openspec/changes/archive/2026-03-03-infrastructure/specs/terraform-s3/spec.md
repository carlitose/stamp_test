## ADDED Requirements

### Requirement: S3 bucket with prefix structure
Terraform SHALL create an S3 bucket with a unique name derived from the project name variable.

#### Scenario: Bucket created with correct naming
- **WHEN** `terraform apply` is run
- **THEN** an S3 bucket SHALL be created with a name based on the project name variable

### Requirement: S3 prefix objects
Terraform SHALL create placeholder objects to establish the `uploads/`, `processed/`, and `reports/` prefixes.

#### Scenario: Prefixes exist after apply
- **WHEN** the bucket is created
- **THEN** the `uploads/`, `processed/`, and `reports/` prefixes SHALL exist in the bucket

### Requirement: S3 event notification for Lambda
Terraform SHALL configure an S3 event notification that triggers the Lambda function on `PutObject` events in the `uploads/` prefix for `.csv` files.

#### Scenario: CSV upload triggers Lambda
- **WHEN** a `.csv` file is uploaded to `uploads/`
- **THEN** the Lambda function SHALL be invoked via S3 event notification

#### Scenario: Non-CSV files ignored
- **WHEN** a non-CSV file is uploaded to `uploads/`
- **THEN** the Lambda function SHALL NOT be invoked
