## ADDED Requirements

### Requirement: SES email identity
Terraform SHALL create an SES email identity verification for the sender email address.

#### Scenario: Sender email identity created
- **WHEN** `terraform apply` is run
- **THEN** an SES email identity verification SHALL be initiated for the `sender_email` variable value

### Requirement: SES region configuration
The SES resource SHALL be created in the same region as all other resources.

#### Scenario: SES in configured region
- **WHEN** `terraform apply` is run
- **THEN** the SES email identity SHALL be created in the region specified by the `aws_region` variable
