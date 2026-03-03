## ADDED Requirements

### Requirement: Send result email via SES
The system SHALL send an email via Amazon SES to the recipient address containing the computed sum value.

#### Scenario: Successful email send
- **WHEN** a valid recipient email and sum value are provided
- **THEN** the system SHALL send an email with subject "CSV Processing Result" and body "The sum of your values is: {sum}" and return True

#### Scenario: SES send failure
- **WHEN** SES rejects the send (e.g., unverified recipient in sandbox)
- **THEN** the system SHALL log the error and return False without raising an exception

#### Scenario: Multiple rows with same email
- **WHEN** multiple rows have the same recipient email
- **THEN** the system SHALL send one email per row (not deduplicate)

### Requirement: Configurable sender email
The system SHALL use the sender email from the `SENDER_EMAIL` environment variable.

#### Scenario: Sender email loaded from environment
- **WHEN** the email service is initialized
- **THEN** it SHALL use the value of `SENDER_EMAIL` environment variable as the sender address
