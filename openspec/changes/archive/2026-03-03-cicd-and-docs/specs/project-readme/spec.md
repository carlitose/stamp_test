## ADDED Requirements

### Requirement: Complete setup documentation
The README SHALL enable a new developer to set up and deploy the project from scratch in under 15 minutes.

#### Scenario: New developer setup
- **WHEN** a developer reads the README
- **THEN** they SHALL find clear prerequisites, step-by-step setup instructions, and deployment commands

### Requirement: Architecture overview
The README SHALL include a visual architecture diagram showing the data flow from S3 upload through Lambda processing to SES email delivery.

#### Scenario: Architecture understanding
- **WHEN** an evaluator reads the README
- **THEN** they SHALL understand the system architecture from a diagram without reading the code

### Requirement: Testing instructions
The README SHALL include instructions for running the test suite and for manually testing the deployed pipeline.

#### Scenario: Running tests
- **WHEN** a developer wants to verify the code
- **THEN** the README SHALL provide commands for running pytest and for uploading a test CSV to S3
