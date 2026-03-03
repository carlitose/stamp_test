## ADDED Requirements

### Requirement: Generate processing report
The system SHALL generate a JSON report containing processing results for each row.

#### Scenario: Report structure
- **WHEN** processing completes (with or without errors)
- **THEN** the report SHALL contain: `file_name`, `processed_at` (ISO 8601), `total_rows`, `successful_rows`, `failed_rows`, and `results` array

#### Scenario: Each result entry
- **WHEN** a row is processed
- **THEN** its result entry SHALL contain: `row_number`, `status` ("success" or "error"), `recipient_email`, `sum` (or null), `error_message` (or null)

### Requirement: Save report to S3
The system SHALL save the JSON report to S3 under the `reports/` prefix.

#### Scenario: Report saved successfully
- **WHEN** processing completes
- **THEN** the system SHALL save the report as `reports/{filename}_{timestamp}.json` with ContentType `application/json`

#### Scenario: Report always generated
- **WHEN** all rows fail validation
- **THEN** the system SHALL still generate and save a report with `successful_rows: 0`

#### Scenario: Report save failure
- **WHEN** S3 PutObject fails for the report
- **THEN** the system SHALL log the error but NOT block the rest of the flow (non-blocking)
