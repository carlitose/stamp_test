## 1. Configuration

- [x] 1.1 Implement `src/lambda/config.py` — load SENDER_EMAIL and AWS_REGION from env vars

## 2. CSV Parsing

- [x] 2.1 Implement `src/lambda/csv_service.py` — `download_csv()` and `parse_csv()`
- [x] 2.2 Add `tests/test_csv_service.py` — test download from moto S3, parsing, whitespace trimming, empty CSV

## 3. Row Validation

- [x] 3.1 Implement `src/lambda/validator.py` — `validate_row()` and `validate_email()`
- [x] 3.2 Add `tests/test_validator.py` — test valid rows, missing columns, non-numeric, invalid email, header detection

## 4. Email Sending

- [x] 4.1 Implement `src/lambda/email_service.py` — `send_result()` via SES
- [x] 4.2 Add `tests/test_email_service.py` — test successful send and failure handling with moto SES

## 5. Report Generation

- [x] 5.1 Implement `src/lambda/report_service.py` — `save_report()` to S3
- [x] 5.2 Add `tests/test_report_service.py` — test report structure, S3 save, empty results

## 6. File Idempotency

- [x] 6.1 Implement `src/lambda/file_service.py` — `move_to_processed()`
- [x] 6.2 Add `tests/test_file_service.py` — test copy+delete, key transformation

## 7. Lambda Handler

- [x] 7.1 Implement `src/lambda/handler.py` — `lambda_handler()` orchestrating full flow
- [x] 7.2 Add `tests/test_handler.py` — test happy path, partial failures, empty CSV, invalid event, idempotency check

## 8. Final Verification

- [x] 8.1 Run `ruff check .` and fix any linting issues
- [x] 8.2 Run `pytest -v` and verify all tests pass
