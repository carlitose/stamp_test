## ADDED Requirements

### Requirement: Extract S3 event data
The system SHALL extract the bucket name and object key from the S3 PutObject event.

#### Scenario: Valid S3 event
- **WHEN** a standard S3 PutObject event is received
- **THEN** the system SHALL extract bucket and key from `event["Records"][0]["s3"]`

### Requirement: Validate event
The system SHALL validate that the object key starts with `uploads/` and ends with `.csv`.

#### Scenario: Valid CSV in uploads
- **WHEN** the key is `uploads/data.csv`
- **THEN** the system SHALL proceed with processing

#### Scenario: Non-CSV file
- **WHEN** the key does not end with `.csv` (e.g., `uploads/data.txt`)
- **THEN** the system SHALL log a warning and exit without processing

#### Scenario: Wrong prefix
- **WHEN** the key does not start with `uploads/` (e.g., `processed/data.csv`)
- **THEN** the system SHALL log a warning and exit without processing

### Requirement: Orchestrate processing flow
The system SHALL orchestrate the full processing flow: download → parse → validate/sum/email per row → save report → move file.

#### Scenario: Happy path
- **WHEN** a valid CSV is uploaded with valid rows
- **THEN** the system SHALL process all rows, send emails, save report, and move file to processed

#### Scenario: Partial failures
- **WHEN** some rows are invalid or email sending fails
- **THEN** the system SHALL continue processing remaining rows, include all results in the report, and still move the file to processed

#### Scenario: Empty CSV
- **WHEN** the CSV has no data rows (empty or header only)
- **THEN** the system SHALL generate a report with 0 rows and move the file to processed

### Requirement: Structured logging
The system SHALL log all operations with appropriate levels: INFO for normal operations, ERROR for failures.

#### Scenario: Processing summary
- **WHEN** processing completes
- **THEN** the system SHALL log a summary with total, successful, and failed row counts at INFO level

#### Scenario: Error logging
- **WHEN** a row fails validation or email sending fails
- **THEN** the system SHALL log the specific error with row details at ERROR level
