## Context

The project scaffolding is in place (Python 3.12, boto3, pytest+moto, ruff). The master spec (`csv-processor-pipeline-spec.md`) defines the full architecture with a flat modular design: `handler.py` orchestrates independent services (`csv_service`, `validator`, `email_service`, `report_service`, `file_service`), each with a single responsibility.

The Lambda receives S3 PutObject events, processes CSV rows, and interacts with S3 and SES. All modules live in `src/lambda/`.

## Goals / Non-Goals

**Goals:**
- Implement all 7 Python modules as defined in the master spec
- Full unit test coverage using moto for S3 and SES mocking
- Resilient row-by-row processing: invalid rows are skipped, never block the batch
- Structured logging (INFO/ERROR) for CloudWatch debugging
- Clean separation: handler only orchestrates, services do the work

**Non-Goals:**
- Terraform or infrastructure (that's `infrastructure` change)
- CI/CD pipeline (that's `cicd-and-docs` change)
- Integration testing against real AWS
- Performance optimization beyond the 60s timeout constraint
- Retry logic for SES failures (log and continue)

## Decisions

### 1. Module structure: flat modules, no classes

**Decision**: Each service is a Python module with top-level functions, not a class.

**Rationale**: The master spec defines functions like `download_csv(bucket, key)`, `send_result(recipient, sum)`. Simple functions are easier to test, mock, and read. No state to manage between calls — the handler passes data explicitly.

**Alternatives**: Class-based services with dependency injection — overkill for a Lambda with 1 entry point.

### 2. boto3 clients: module-level singletons

**Decision**: Each module creates its boto3 client at module level (e.g., `s3_client = boto3.client("s3")`).

**Rationale**: Lambda reuses the execution environment across invocations. Module-level clients benefit from connection reuse. This is the standard Lambda pattern.

**Testing implication**: moto decorators intercept boto3 at import time, so module-level clients work correctly in tests.

### 3. CSV parsing: Python csv module, no pandas

**Decision**: Use `csv.reader` from the standard library.

**Rationale**: Lambda has 128MB memory and we want fast cold starts. pandas would add ~50MB to the deployment package. `csv.reader` handles all our cases (commas, whitespace, decimals, negatives).

### 4. Email validation: regex, not external library

**Decision**: Simple regex pattern `^[^@\s]+@[^@\s]+\.[^@\s]+$` as defined in the master spec.

**Rationale**: Good enough for this use case. SES will reject truly invalid addresses anyway. No need for a dependency like `email-validator`.

### 5. Header row detection: skip first row if non-numeric

**Decision**: If the first row's first 3 values are not all numeric, treat it as a header and skip it.

**Rationale**: Defined in edge case EC06. Simple heuristic that avoids requiring the user to declare header presence.

### 6. Testing strategy: one test module per service module

**Decision**: Mirror the `src/lambda/` structure in `tests/`:
- `tests/test_csv_service.py`
- `tests/test_validator.py`
- `tests/test_email_service.py`
- `tests/test_report_service.py`
- `tests/test_file_service.py`
- `tests/test_handler.py`

**Rationale**: Easy to find tests, clear ownership, parallel with source.

## Risks / Trade-offs

- **[moto SES sandbox behavior]** → moto doesn't simulate SES sandbox restrictions (unverified recipients). Tests verify the happy path; sandbox behavior is tested at integration time.
- **[Module-level imports in Lambda]** → If `config.py` reads env vars at import time, tests must set env vars before importing. Mitigated by using `os.environ.get` with defaults or setting env vars in test fixtures.
- **[Large CSV files]** → Lambda has 60s timeout. A CSV with many rows where each row triggers an SES API call could timeout. Accepted trade-off per spec constraint C01 (free tier, simple architecture).
- **[No retry on SES failure]** → A failed email is logged and marked as error in the report. No retry queue. Acceptable per spec — the report captures the failure for manual follow-up.
