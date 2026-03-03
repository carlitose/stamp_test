## ADDED Requirements

### Requirement: Download CSV from S3
The system SHALL download a CSV file from S3 given a bucket name and object key, returning the file content as a UTF-8 string.

#### Scenario: Successful download
- **WHEN** a valid bucket and key are provided
- **THEN** the system SHALL return the CSV content as a decoded UTF-8 string

#### Scenario: File not found
- **WHEN** the specified key does not exist in the bucket
- **THEN** the system SHALL raise an exception with a descriptive error message

### Requirement: Parse CSV into rows
The system SHALL parse CSV content into a list of rows, where each row is a list of stripped string values.

#### Scenario: Standard CSV parsing
- **WHEN** CSV content with comma-separated values is provided
- **THEN** the system SHALL return a list of rows with each field trimmed of whitespace

#### Scenario: Values with extra whitespace
- **WHEN** CSV fields contain leading or trailing spaces (e.g., `" 100 "`)
- **THEN** the system SHALL strip whitespace from each field before returning

#### Scenario: Empty CSV
- **WHEN** the CSV content is empty or contains no rows
- **THEN** the system SHALL return an empty list
