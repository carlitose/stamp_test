## ADDED Requirements

### Requirement: Validate row structure
The system SHALL validate that each CSV row contains exactly 4 fields.

#### Scenario: Row with fewer than 4 columns
- **WHEN** a row has fewer than 4 fields
- **THEN** the system SHALL return an error result indicating missing columns

#### Scenario: Row with exactly 4 columns
- **WHEN** a row has exactly 4 fields
- **THEN** the system SHALL proceed to validate field values

### Requirement: Validate numeric values
The system SHALL validate that the first 3 columns contain numeric values (integer or float, including negative numbers).

#### Scenario: Valid integer values
- **WHEN** columns 1-3 contain integer strings (e.g., "100", "200", "300")
- **THEN** the system SHALL accept and parse them as numbers

#### Scenario: Valid decimal values
- **WHEN** columns 1-3 contain decimal strings (e.g., "20.5", "-10.3")
- **THEN** the system SHALL accept and parse them as float numbers

#### Scenario: Negative values
- **WHEN** columns 1-3 contain negative values (e.g., "-10")
- **THEN** the system SHALL accept and parse them correctly

#### Scenario: Non-numeric values
- **WHEN** any of columns 1-3 contains a non-numeric string (e.g., "abc")
- **THEN** the system SHALL return an error result indicating the invalid value

### Requirement: Validate email format
The system SHALL validate that column 4 contains a valid email address matching the pattern `^[^@\s]+@[^@\s]+\.[^@\s]+$`.

#### Scenario: Valid email
- **WHEN** column 4 contains a valid email (e.g., "user@example.com")
- **THEN** the system SHALL accept it

#### Scenario: Invalid email format
- **WHEN** column 4 contains an invalid email (e.g., "not-an-email", "@missing.com", "no@dots")
- **THEN** the system SHALL return an error result indicating the invalid email

### Requirement: Header row detection
The system SHALL detect and skip header rows where the first 3 values are not all numeric.

#### Scenario: First row is a header
- **WHEN** the first row's first 3 fields are not all parseable as numbers
- **THEN** the system SHALL skip the first row and not process it as data
