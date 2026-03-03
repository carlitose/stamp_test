## Why

The project scaffolding is in place but there is no application code. The core Lambda function is the heart of the pipeline — it processes CSV files, validates rows, computes sums, sends emails via SES, generates reports, and ensures idempotency. Without this, the pipeline does nothing.

## What Changes

- Implement `handler.py` — Lambda entry point that orchestrates the full processing flow
- Implement `config.py` — centralized environment variable loading
- Implement `csv_service.py` — download CSV from S3 and parse rows
- Implement `validator.py` — validate row structure (4 columns, numeric values, valid email)
- Implement `email_service.py` — send result emails via SES
- Implement `report_service.py` — generate and save JSON processing report to S3
- Implement `file_service.py` — move processed CSV from `uploads/` to `processed/`
- Add unit tests for all modules using pytest + moto

## Capabilities

### New Capabilities
- `csv-parsing`: Download CSV from S3 and parse into structured rows with whitespace trimming
- `row-validation`: Validate each row has 4 columns, numeric values in cols 1-3, valid email in col 4
- `email-sending`: Send sum result email to each recipient via SES
- `report-generation`: Generate JSON processing report with success/error counts and save to S3
- `file-idempotency`: Move processed CSV from `uploads/` to `processed/` to prevent re-processing
- `lambda-handler`: Orchestrate the full flow — event validation, CSV processing, report, file move

### Modified Capabilities
<!-- None — all new capabilities -->

## Impact

- **Files**: 7 new Python modules in `src/lambda/`, test files in `tests/`
- **Dependencies**: Uses boto3 (already in requirements.txt), no new dependencies needed
- **APIs**: S3 (GetObject, PutObject, CopyObject, DeleteObject), SES (SendEmail)
- **Downstream**: `infrastructure` change will deploy this code via Terraform
