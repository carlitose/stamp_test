## ADDED Requirements

### Requirement: Runtime dependencies
The project SHALL include a `requirements.txt` file listing runtime dependencies needed by the Lambda function. It SHALL include `boto3>=1.34,<2.0` as the only runtime dependency.

#### Scenario: Runtime dependencies are installable
- **WHEN** a developer runs `pip install -r requirements.txt`
- **THEN** boto3 SHALL be installed successfully

### Requirement: Development dependencies
The project SHALL include a `requirements-dev.txt` file listing development dependencies. It SHALL include:
- `pytest` for test execution
- `moto[s3,ses]` for AWS service mocking
- `ruff` for linting and formatting
The file SHALL reference `requirements.txt` via `-r requirements.txt` to include runtime deps.

#### Scenario: Dev dependencies are installable
- **WHEN** a developer runs `pip install -r requirements-dev.txt`
- **THEN** pytest, moto (with S3 and SES backends), ruff, and boto3 SHALL all be installed
