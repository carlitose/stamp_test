# CSV Processor Pipeline - Specification

## Table of Contents

1. [Overview](#1-overview)
2. [Phase 1: Requirements](#2-phase-1-requirements)
3. [Phase 2: Specifications](#3-phase-2-specifications)
4. [Phase 3: System Design](#4-phase-3-system-design)
5. [Appendix](#appendix)

---

## 1. Overview

### Vision

A serverless AWS pipeline that automatically processes CSV files uploaded to S3, summing the first three column values of each row and sending the result via email (SES) to the address in the fourth column. The project follows an OpenSpec methodology with spec-driven development and a clear commit history.

### Target User

- **Evaluators (STAMP team)**: reviewing code quality, infrastructure, commit history, README clarity, and AI-assisted development practices
- **Operators/Developers**: uploading CSV files and maintaining the pipeline infrastructure

### Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python (AWS Lambda) |
| Infrastructure | Terraform |
| CI/CD | GitHub Actions |
| Email | Amazon SES |
| Trigger | S3 Event Notification → Lambda |
| Storage | Amazon S3 (uploads, processed, reports) |

---

## 2. Phase 1: Requirements

### 2.1 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR01 | Uploading a CSV to S3 (prefix `uploads/`) triggers the Lambda function |
| FR02 | Lambda reads the CSV and sums the first 3 columns for each row |
| FR03 | Lambda sends an email via SES with the sum result to the address in column 4 |
| FR04 | Invalid rows are skipped with error logging, without blocking the batch |
| FR05 | A JSON report is saved to S3 (prefix `reports/`) with results and errors |
| FR06 | Processed CSV is moved to prefix `processed/` for idempotency |
| FR07 | All infrastructure is deployed via Terraform |
| FR08 | CI/CD is handled via GitHub Actions (manual trigger acceptable) |

### 2.2 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR01 | Lambda timeout: 60 seconds |
| NFR02 | Lambda memory: 128MB |
| NFR03 | Structured logging with Python `logging` module (INFO/ERROR levels) |
| NFR04 | IAM least privilege for the Lambda execution role |
| NFR05 | No hardcoded credentials in code or Terraform |
| NFR06 | Sender email as a configurable variable (Terraform var → Lambda env → GitHub secret) |

### 2.3 Constraints

| ID | Constraint |
|----|------------|
| C01 | Zero cost — everything within AWS free tier |
| C02 | OpenSpec methodology: spec → implementation → commit |
| C03 | Estimated timeline: 3–5 hours |
| C04 | SES sender email must be verified before deployment |
| C05 | Mandatory stack: Python, Terraform, GitHub Actions, SES, S3 |

---

## 3. Phase 2: Specifications

### 3.1 User Stories

#### Core Flow

| ID | User Story |
|----|------------|
| US01 | As a pipeline, when a CSV is uploaded to `uploads/`, I want to activate automatically so processing is immediate without manual intervention |
| US02 | As a pipeline, I want to read each CSV row and sum the first 3 column values so I can compute the total for each recipient |
| US03 | As a pipeline, I want to send an email via SES to each address in column 4 with the sum result so every recipient receives their total |
| US04 | As a pipeline, I want to skip invalid rows and continue with the rest so a single error doesn't block the entire batch |

#### Operations

| ID | User Story |
|----|------------|
| US05 | As a pipeline, I want to move processed CSVs to `processed/` so I avoid re-processing the same file |
| US06 | As a pipeline, I want to save a JSON report in `reports/` with a summary (rows processed, errors, results) for traceability |
| US07 | As a pipeline, I want to log every operation with appropriate levels (INFO/ERROR) so debugging is possible via CloudWatch |

#### Infrastructure & Deployment

| ID | User Story |
|----|------------|
| US08 | As a developer, I want to deploy all infrastructure with `terraform apply` so the setup is repeatable and documented |
| US09 | As a developer, I want a GitHub Actions workflow that deploys the infrastructure so CI/CD is automated |
| US10 | As a developer, I want a clear README that allows anyone to set up everything from scratch so the project is self-contained |

### 3.2 Use Cases

#### UC01: CSV Processing (Main Flow)

| Field | Description |
|-------|-------------|
| Actor | S3 Event Notification |
| Preconditions | CSV uploaded in `uploads/`, Lambda deployed, SES sender verified |
| Trigger | S3 `PutObject` event on prefix `uploads/` |
| Main Flow | 1. Lambda receives S3 event with bucket and file key<br>2. Validates the file is in `uploads/` and has `.csv` extension<br>3. Downloads the CSV from S3<br>4. For each row: validate data, sum columns 1-2-3, send email via SES<br>5. Collects results (successes and errors)<br>6. Saves JSON report in `reports/`<br>7. Moves original CSV to `processed/`<br>8. Logs final summary |
| Alternative Flow | 3a. File not found → log error, exit<br>4a. Invalid row (non-numeric values, missing columns) → log error, skip row<br>4b. Invalid email → log error, skip row<br>4c. SES fails for a row → log error, continue with others<br>6a. Report write failure → log error (non-blocking) |
| Postconditions | Emails sent to valid recipients, CSV in `processed/`, report in `reports/` |

#### UC02: Infrastructure Deployment

| Field | Description |
|-------|-------------|
| Actor | Developer |
| Preconditions | AWS credentials configured, Terraform installed, SES sender email verified |
| Trigger | `terraform apply` (manual or via GitHub Actions) |
| Main Flow | 1. Terraform creates S3 bucket with required prefixes<br>2. Creates IAM role with least privilege policy<br>3. Deploys Lambda function with env vars<br>4. Configures S3 event notification → Lambda<br>5. Outputs: bucket name, Lambda ARN, useful commands |
| Alternative Flow | 2a. Insufficient AWS permissions → Terraform fails with clear error |
| Postconditions | Infrastructure ready, pipeline operational |

### 3.3 Data Models

```typescript
// CSV Row (input)
interface CSVRow {
  column1: string;  // numeric value as string from CSV
  column2: string;
  column3: string;
  recipient_email: string;
}

// Single row processing result
interface RowResult {
  row_number: number;
  status: "success" | "error";
  recipient_email: string | null;
  sum: number | null;
  error_message: string | null;
}

// Processing report (saved as JSON to S3)
interface ProcessingReport {
  file_name: string;
  processed_at: string;        // ISO 8601
  total_rows: number;
  successful_rows: number;
  failed_rows: number;
  results: RowResult[];
}

// S3 Event (Lambda input)
interface S3Event {
  bucket: string;
  key: string;                 // e.g. "uploads/data.csv"
}

// S3 Bucket Structure
// uploads/       → incoming CSVs
// processed/     → processed CSVs
// reports/       → JSON reports
```

### 3.4 API Contracts / Interfaces

```typescript
// === Handler (entry point) ===
// Receives S3 event, orchestrates the flow
function lambda_handler(event: S3Event): void

// === CSV Service ===
interface CSVService {
  // Downloads and parses the CSV from S3
  download_csv(bucket: string, key: string): string;
  parse_csv(content: string): CSVRow[];
}

// === Validator ===
interface RowValidator {
  // Validates a single row: 3 numeric values + valid email
  validate_row(row: CSVRow, row_number: number): RowResult | ValidatedRow;
  validate_email(email: string): boolean;
}

interface ValidatedRow {
  row_number: number;
  values: [number, number, number];
  recipient_email: string;
}

// === Email Service ===
interface EmailService {
  // Sends email with the sum result
  send_result(recipient: string, sum: number): boolean;
}

// === Report Service ===
interface ReportService {
  // Generates and saves the JSON report to S3
  save_report(bucket: string, file_name: string, results: RowResult[]): void;
}

// === File Service ===
interface FileService {
  // Moves the CSV from uploads/ to processed/
  move_to_processed(bucket: string, key: string): void;
}
```

### 3.5 Edge Cases

#### Input & Validation

| ID | Case | Expected Behavior |
|----|------|-------------------|
| EC01 | Empty CSV (header only or 0 rows) | Log warning, generate report with 0 rows, move to processed/ |
| EC02 | Non-numeric values in columns 1-3 | Skip row, log error with details |
| EC03 | Missing columns (row with fewer than 4 fields) | Skip row, log error |
| EC04 | Malformed email in column 4 | Skip row, log error |
| EC05 | Values with extra spaces/whitespace | Trim before processing |
| EC06 | CSV with header row | Detect and skip first row if non-numeric |
| EC07 | Decimal/negative values in columns 1-3 | Accept them, sum handles them correctly |

#### S3 & File System

| ID | Case | Expected Behavior |
|----|------|-------------------|
| EC08 | File is not a .csv (e.g. .txt uploaded to uploads/) | Log warning, ignore |
| EC09 | File already moved to processed/ (Lambda retry) | Check existence in uploads/ before processing, exit if not found |
| EC10 | Very large file | Lambda timeout at 60s, log if incomplete |

#### SES & Email

| ID | Case | Expected Behavior |
|----|------|-------------------|
| EC11 | SES rejects send (recipient not verified in sandbox) | Log error, continue with other rows |
| EC12 | SES rate limit reached | Log error, mark row as failed in report |
| EC13 | Same email appears on multiple rows | Send multiple emails, one per row (correct behavior) |

### 3.6 Quality Requirements

#### Usability

| ID | Requirement |
|----|-------------|
| QR01 | README enables complete setup in under 15 minutes |
| QR02 | Sample CSV included in the repository for immediate testing |
| QR03 | Terraform outputs display all useful info (bucket name, Lambda ARN, test commands) |

#### Performance

| ID | Requirement |
|----|-------------|
| QR04 | Lambda processes a 100-row CSV within 30 seconds |
| QR05 | Memory footprint under 128MB for reasonable CSV sizes |

#### Reliability

| ID | Requirement |
|----|-------------|
| QR06 | A single invalid row does not block processing of other rows |
| QR07 | JSON report is always generated, even with partial errors |
| QR08 | Idempotency guaranteed by moving files to processed/ |

#### Maintainability

| ID | Requirement |
|----|-------------|
| QR09 | Code separated into modules with single responsibility (handler, csv, email, report) |
| QR10 | All configuration via environment variables |
| QR11 | Modular Terraform with variables, no hardcoded values |
| QR12 | Structured logging with INFO/ERROR levels for CloudWatch debugging |

---

## 4. Phase 3: System Design

### 4.1 Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    S3 Bucket                         │
│  uploads/  │  processed/  │  reports/               │
└──────┬──────────────────────────────────────────────┘
       │ PutObject event (uploads/*.csv)
       ▼
┌─────────────────────────────────────────────────────┐
│                 Lambda Handler                       │
│  handler.py — orchestrates the flow                 │
│                                                      │
│  ┌─────────────┐ ┌─────────────┐ ┌──────────────┐  │
│  │ csv_service  │ │ email_service│ │ report_service│  │
│  │ download     │ │ send via SES │ │ save JSON     │  │
│  │ parse        │ │              │ │ to S3         │  │
│  │ validate     │ │              │ │               │  │
│  └─────────────┘ └─────────────┘ └──────────────┘  │
│                                                      │
│  ┌─────────────┐ ┌─────────────┐                    │
│  │ file_service │ │  validator   │                    │
│  │ move to      │ │ validate row │                    │
│  │ processed/   │ │ validate email│                   │
│  └─────────────┘ └─────────────┘                    │
└─────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────┐
│   Amazon SES     │
│ send email       │
└─────────────────┘
```

Flat modular architecture with clear separation of responsibilities. No over-engineering (no DDD, no hexagonal) — each module handles one concern.

### 4.2 Project Structure

```
csv-processor-pipeline/
├── README.md
├── sample.csv
│
├── specs/                          # OpenSpec: specs before code
│   ├── 01-csv-parsing.md
│   ├── 02-email-sending.md
│   ├── 03-report-generation.md
│   ├── 04-idempotency.md
│   └── 05-infrastructure.md
│
├── src/
│   └── lambda/
│       ├── handler.py              # Lambda entry point
│       ├── csv_service.py          # Download, parse, validate CSV
│       ├── validator.py            # Single row + email validation
│       ├── email_service.py        # Send email via SES
│       ├── report_service.py       # Generate and save JSON report
│       ├── file_service.py         # Move files on S3
│       └── config.py               # Centralized env vars
│
├── terraform/
│   ├── main.tf                     # Main resources
│   ├── variables.tf                # Input variables
│   ├── outputs.tf                  # Useful outputs
│   ├── lambda.tf                   # Lambda + IAM role
│   ├── s3.tf                       # Bucket + event notification
│   ├── ses.tf                      # SES configuration
│   └── terraform.tfvars.example    # Example values (no secrets)
│
└── .github/
    └── workflows/
        └── deploy.yml              # GitHub Actions workflow
```

### 4.3 Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        handler.py                            │
│                     (orchestrator)                            │
│                                                              │
│  lambda_handler(event, context)                              │
│       │                                                      │
│       ├──→ config.py ──→ loads env vars                     │
│       │                                                      │
│       ├──→ csv_service.py                                   │
│       │       └── download_csv(bucket, key)                 │
│       │       └── parse_csv(content) → List[CSVRow]         │
│       │                                                      │
│       ├──→ validator.py                                     │
│       │       └── validate_row(row, row_num) → ValidatedRow │
│       │       └── validate_email(email) → bool              │
│       │                                                      │
│       ├──→ email_service.py                                 │
│       │       └── send_result(recipient, sum) → bool        │
│       │                                                      │
│       ├──→ report_service.py                                │
│       │       └── save_report(bucket, file, results)        │
│       │                                                      │
│       └──→ file_service.py                                  │
│               └── move_to_processed(bucket, key)            │
└─────────────────────────────────────────────────────────────┘

External Dependencies:
  csv_service.py    → boto3 (S3 GetObject)
  email_service.py  → boto3 (SES SendEmail)
  report_service.py → boto3 (S3 PutObject)
  file_service.py   → boto3 (S3 CopyObject + DeleteObject)
  config.py         → os.environ
  validator.py      → re (regex for email validation)
```

Dependency flow is always **handler → service**, never between services.

### 4.4 Data Flow Diagram

#### UC01: CSV Processing (Main Flow)

```
┌──────┐     ┌──────────┐     ┌────────────┐     ┌───────────┐     ┌─────────────┐     ┌──────────────┐
│  S3  │     │ handler  │     │ csv_service│     │ validator │     │email_service│     │report_service│
└──┬───┘     └────┬─────┘     └─────┬──────┘     └─────┬─────┘     └──────┬──────┘     └──────┬───────┘
   │              │                  │                   │                  │                   │
   │ 1. PutObject │                  │                   │                  │                   │
   │  event       │                  │                   │                  │                   │
   │─────────────>│                  │                   │                  │                   │
   │              │                  │                   │                  │                   │
   │              │ 2. download_csv  │                   │                  │                   │
   │              │─────────────────>│                   │                  │                   │
   │              │                  │──→ S3 GetObject   │                  │                   │
   │              │   raw content    │                   │                  │                   │
   │              │<─────────────────│                   │                  │                   │
   │              │                  │                   │                  │                   │
   │              │ 3. parse_csv     │                   │                  │                   │
   │              │─────────────────>│                   │                  │                   │
   │              │   List[CSVRow]   │                   │                  │                   │
   │              │<─────────────────│                   │                  │                   │
   │              │                  │                   │                  │                   │
   │              │ 4. Per row:      │                   │                  │                   │
   │              │ validate_row     │                   │                  │                   │
   │              │──────────────────────────────────────>│                  │                   │
   │              │   ValidatedRow | Error               │                  │                   │
   │              │<─────────────────────────────────────│                  │                   │
   │              │                  │                   │                  │                   │
   │              │ 5. If valid: send_result              │                  │                   │
   │              │───────────────────────────────────────────────────────>│                   │
   │              │                  │                   │     SES SendEmail│                   │
   │              │   bool (success) │                   │                  │                   │
   │              │<──────────────────────────────────────────────────────│                   │
   │              │                  │                   │                  │                   │
   │              │ 6. save_report   │                   │                  │                   │
   │              │────────────────────────────────────────────────────────────────────────────>│
   │              │                  │                   │                  │  S3 PutObject     │
   │              │                  │                   │                  │  reports/          │
   │              │                  │                   │                  │                   │
   │              │ 7. move_to_processed                 │                  │                   │
   │              │──→ file_service  │                   │                  │                   │
   │              │    S3 Copy + Delete                  │                  │                   │
   │              │    uploads/ → processed/             │                  │                   │
```

### 4.5 State Diagram — Lambda Execution

```
                    ┌───────────┐
                    │  TRIGGER  │
                    │ S3 event  │
                    └─────┬─────┘
                          │
                          ▼
                    ┌───────────┐     file not in uploads/
                    │ VALIDATE  │────────────────────────┐
                    │  EVENT    │     or not .csv         │
                    └─────┬─────┘                         │
                          │ ok                            │
                          ▼                               │
                    ┌───────────┐     file not found      │
                    │ DOWNLOAD  │─────────────────────────┤
                    │   CSV     │                         │
                    └─────┬─────┘                         │
                          │ ok                            │
                          ▼                               │
                    ┌───────────┐                         │
                    │  PARSE    │                         │
                    │   CSV     │                         │
                    └─────┬─────┘                         │
                          │                               │
                          ▼                               │
                ┌─────────────────┐                       │
                │  PROCESS ROWS   │                       │
                │  loop per row:  │                       │
                │  validate → sum │                       │
                │  → send email   │                       │
                │  (skip on error)│                       │
                └────────┬────────┘                       │
                         │                                │
                         ▼                                │
                   ┌───────────┐                          │
                   │   SAVE    │                          │
                   │  REPORT   │                          │
                   └─────┬─────┘                          │
                         │                                │
                         ▼                                │
                   ┌───────────┐                          │
                   │   MOVE    │                          │
                   │   FILE    │                          │
                   └─────┬─────┘                          │
                         │                                │
                         ▼                                │
                   ┌───────────┐                          │
                   │  SUCCESS  │◄─────────────────────────┘
                   │   EXIT    │  (log and exit gracefully)
                   └───────────┘
```

Each state logs its entry/exit. Non-blocking failures (invalid rows, SES errors) stay within PROCESS ROWS. Blocking failures (file not found, invalid event) jump directly to EXIT with appropriate logging.

### 4.6 Implementation Details

#### config.py

```python
import os

class Config:
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    AWS_REGION = os.environ.get("AWS_REGION", "eu-south-1")
    REPORT_PREFIX = "reports/"
    PROCESSED_PREFIX = "processed/"
    UPLOADS_PREFIX = "uploads/"
```

#### handler.py

```python
import logging
from config import Config
from csv_service import download_csv, parse_csv
from validator import validate_row
from email_service import send_result
from report_service import save_report
from file_service import move_to_processed

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # 1. Extract bucket and key from S3 event
    # 2. Validate event (prefix uploads/, .csv extension)
    # 3. Check idempotency (file still exists in uploads/?)
    # 4. Download and parse CSV
    # 5. Loop rows: validate → sum → send email → collect results
    # 6. Save report
    # 7. Move to processed
    # Return summary
```

#### csv_service.py

```python
import csv
import io
import boto3
import logging

logger = logging.getLogger()
s3_client = boto3.client("s3")

def download_csv(bucket: str, key: str) -> str:
    """Downloads the CSV from S3, returns content as string."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")

def parse_csv(content: str) -> list[dict]:
    """Parses the CSV, returns list of stripped field lists per row."""
    reader = csv.reader(io.StringIO(content))
    rows = []
    for row in reader:
        rows.append([field.strip() for field in row])
    return rows
```

#### validator.py

```python
import re
import logging

logger = logging.getLogger()
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def validate_row(row: list, row_number: int) -> dict:
    """
    Validates a CSV row.
    Returns: {"valid": True, "values": (n1, n2, n3), "email": str}
    or:      {"valid": False, "error": str}
    """
    # Check 4 columns present
    # Check numeric values (int/float, including negatives)
    # Check email with regex
    # Return structured result
```

#### email_service.py

```python
import boto3
import logging
from config import Config

logger = logging.getLogger()
ses_client = boto3.client("ses", region_name=Config.AWS_REGION)

def send_result(recipient: str, sum_value: float) -> bool:
    """Sends email with result. Returns True on success."""
    try:
        ses_client.send_email(
            Source=Config.SENDER_EMAIL,
            Destination={"ToAddresses": [recipient]},
            Message={
                "Subject": {"Data": "CSV Processing Result"},
                "Body": {"Text": {"Data": f"The sum of your values is: {sum_value}"}}
            }
        )
        logger.info(f"Email sent to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        return False
```

#### report_service.py

```python
import json
import boto3
from datetime import datetime, timezone
import logging

logger = logging.getLogger()
s3_client = boto3.client("s3")

def save_report(bucket: str, file_name: str, results: list[dict]) -> None:
    """Saves JSON report in reports/ on S3."""
    report = {
        "file_name": file_name,
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "total_rows": len(results),
        "successful_rows": sum(1 for r in results if r["status"] == "success"),
        "failed_rows": sum(1 for r in results if r["status"] == "error"),
        "results": results
    }
    report_key = f"reports/{file_name}_{report['processed_at']}.json"
    s3_client.put_object(
        Bucket=bucket,
        Key=report_key,
        Body=json.dumps(report, indent=2),
        ContentType="application/json"
    )
    logger.info(f"Report saved to {report_key}")
```

#### file_service.py

```python
import boto3
import logging

logger = logging.getLogger()
s3_client = boto3.client("s3")

def move_to_processed(bucket: str, key: str) -> None:
    """Moves file from uploads/ to processed/."""
    new_key = key.replace("uploads/", "processed/", 1)
    s3_client.copy_object(
        Bucket=bucket, Key=new_key,
        CopySource={"Bucket": bucket, "Key": key}
    )
    s3_client.delete_object(Bucket=bucket, Key=key)
    logger.info(f"Moved {key} → {new_key}")
```

---

## Appendix

### A. Sample CSV

```csv
100,200,300,recipient@example.com
50,75,25,another@example.com
-10,20.5,30,test@example.com
```

### B. OpenSpec Commit Strategy

The commit history should follow this pattern for each feature:

```
feat(spec): add CSV parsing specification
feat(csv): implement CSV download and parsing
feat(spec): add email sending specification
feat(email): implement SES email sending
feat(spec): add report generation specification
feat(report): implement JSON report generation
feat(spec): add idempotency specification
feat(idempotency): implement file move to processed/
feat(spec): add infrastructure specification
feat(infra): add Terraform configuration
feat(ci): add GitHub Actions workflow
docs: add README with setup instructions
```

### C. Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| SENDER_EMAIL | Verified SES sender email | GitHub Secret → Terraform var → Lambda env |
| AWS_REGION | AWS region for SES | Lambda env (default: eu-south-1) |

### D. Terraform Outputs (Expected)

| Output | Description |
|--------|-------------|
| bucket_name | Name of the S3 bucket |
| bucket_arn | ARN of the S3 bucket |
| lambda_function_name | Name of the Lambda function |
| lambda_function_arn | ARN of the Lambda function |
| upload_command | Example AWS CLI command to upload a test CSV |

---

*Document generated: 2026-03-03*
*Version: 1.0*
