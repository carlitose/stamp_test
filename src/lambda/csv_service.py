import csv
import io
import logging

import boto3

logger = logging.getLogger()
s3_client = boto3.client("s3")


def download_csv(bucket: str, key: str) -> str:
    """Downloads the CSV from S3, returns content as string."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")


def parse_csv(content: str) -> list[list[str]]:
    """Parses the CSV, returns list of stripped field lists per row."""
    reader = csv.reader(io.StringIO(content))
    rows = []
    for row in reader:
        stripped = [field.strip() for field in row]
        if any(field for field in stripped):
            rows.append(stripped)
    return rows
