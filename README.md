# CSV Processor Pipeline

A serverless AWS pipeline that processes CSV files uploaded to S3, sums the first three column values of each row, and sends the result via email (SES) to the address in the fourth column.

## Architecture

```
                         ┌──────────────────────────────┐
                         │         S3 Bucket             │
                         │  uploads/ │ processed/ │ reports/ │
                         └─────┬─────────────────────────┘
                               │ PutObject event
                               │ (uploads/*.csv)
                               ▼
                         ┌──────────────────────────────┐
                         │        Lambda Function        │
                         │                               │
                         │  1. Download & parse CSV      │
                         │  2. Validate each row         │
                         │  3. Sum columns 1-3           │
                         │  4. Send email via SES        │
                         │  5. Save JSON report          │
                         │  6. Move file to processed/   │
                         └──────────┬───────────────────┘
                                    │
                              ┌─────┴─────┐
                              ▼           ▼
                         ┌────────┐  ┌────────┐
                         │  SES   │  │   S3   │
                         │ Email  │  │ Report │
                         └────────┘  └────────┘
```

## Prerequisites

- Python 3.12
- AWS CLI configured with valid credentials
- Terraform >= 1.5
- An AWS account with SES sender email verified
- Git

## Setup

### 1. Clone and install dependencies

```bash
git clone <repository-url>
cd csv-processor-pipeline

python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Verify SES sender email

Before deploying, verify your sender email in the AWS SES console:

```bash
aws ses verify-email-identity --email-address your-email@example.com --region eu-south-1
```

Check your inbox and click the verification link.

> **Note:** In SES sandbox mode, recipient emails must also be verified.

### 3. Configure Terraform

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your verified sender email:

```hcl
sender_email = "your-email@example.com"
```

## Deployment

### Manual (Terraform CLI)

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

After successful deploy, Terraform outputs the bucket name and a test command:

```
bucket_name = "csv-processor-a1b2c3d4"
upload_command = "aws s3 cp sample.csv s3://csv-processor-a1b2c3d4/uploads/sample.csv"
```

### Automated (GitHub Actions)

1. Add these secrets in your GitHub repository (Settings > Secrets > Actions):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `SENDER_EMAIL`

2. Go to Actions > "Deploy Infrastructure" > "Run workflow"

## Testing

### Unit tests

```bash
source venv/bin/activate
pytest -v
```

All 30 tests use [moto](https://github.com/getmoto/moto) to mock AWS services — no AWS credentials needed.

### Manual end-to-end test

After deployment, upload the sample CSV:

```bash
aws s3 cp sample.csv s3://<bucket-name>/uploads/sample.csv
```

Then check:
- **Email**: Recipients should receive an email with their sum
- **Report**: `aws s3 ls s3://<bucket-name>/reports/`
- **Processed**: `aws s3 ls s3://<bucket-name>/processed/`
- **Logs**: Check CloudWatch Logs for the Lambda function

### Sample CSV format

```csv
100,200,300,recipient@example.com
50,75,25,another@example.com
-10,20.5,30,test@example.com
```

Each row: 3 numeric values + recipient email. The pipeline sums columns 1-3 and emails the result to column 4.

## Project Structure

```
csv-processor-pipeline/
├── README.md                    # This file
├── sample.csv                   # Sample CSV for testing
├── requirements.txt             # Runtime dependency (boto3)
├── requirements-dev.txt         # Dev dependencies (pytest, moto, ruff)
├── pyproject.toml               # Ruff + pytest configuration
├── .python-version              # Python 3.12
│
├── src/lambda/                  # Lambda function code
│   ├── handler.py               # Entry point — orchestrates the flow
│   ├── config.py                # Environment variable loading
│   ├── csv_service.py           # S3 download and CSV parsing
│   ├── validator.py             # Row validation (numeric + email)
│   ├── email_service.py         # SES email sending
│   ├── report_service.py        # JSON report generation
│   └── file_service.py          # S3 file move (idempotency)
│
├── tests/                       # Unit tests (pytest + moto)
│   ├── conftest.py              # Shared test configuration
│   ├── test_handler.py          # Integration tests for full flow
│   ├── test_csv_service.py      # CSV download and parsing tests
│   ├── test_validator.py        # Validation logic tests
│   ├── test_email_service.py    # SES sending tests
│   ├── test_report_service.py   # Report generation tests
│   └── test_file_service.py     # File move tests
│
├── terraform/                   # Infrastructure as Code
│   ├── main.tf                  # Provider configuration
│   ├── variables.tf             # Input variables
│   ├── s3.tf                    # S3 bucket and prefixes
│   ├── lambda.tf                # Lambda + IAM role
│   ├── s3_notification.tf       # S3 event → Lambda trigger
│   ├── ses.tf                   # SES email identity
│   ├── outputs.tf               # Useful outputs
│   └── terraform.tfvars.example # Example variable values
│
├── .github/workflows/
│   └── deploy.yml               # GitHub Actions deployment
│
└── openspec/                    # OpenSpec artifacts and specs
    ├── config.yaml
    ├── specs/                   # Main capability specs
    └── changes/archive/         # Archived change proposals
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Runtime | Python 3.12 (AWS Lambda) |
| Infrastructure | Terraform |
| CI/CD | GitHub Actions |
| Email | Amazon SES |
| Storage | Amazon S3 |
| Testing | pytest + moto |
| Linting | Ruff |

## Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `SENDER_EMAIL` | Verified SES sender email | GitHub Secret → Terraform var → Lambda env |
| `AWS_REGION` | AWS region (default: eu-south-1) | Lambda env |
