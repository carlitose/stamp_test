## ADDED Requirements

### Requirement: Move processed file
The system SHALL move the CSV file from `uploads/` to `processed/` after processing completes.

#### Scenario: Successful move
- **WHEN** processing is complete (report saved)
- **THEN** the system SHALL copy the file to `processed/{filename}` and delete the original from `uploads/`

#### Scenario: File key transformation
- **WHEN** the source key is `uploads/data.csv`
- **THEN** the target key SHALL be `processed/data.csv` (first occurrence of `uploads/` replaced with `processed/`)

### Requirement: Idempotency check
The system SHALL verify the file still exists in `uploads/` before processing to handle Lambda retries.

#### Scenario: File already moved (retry scenario)
- **WHEN** the Lambda is triggered but the file no longer exists in `uploads/`
- **THEN** the system SHALL log a warning and exit gracefully without processing
