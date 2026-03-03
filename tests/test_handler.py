import importlib
import json

import boto3
from moto import mock_aws


def _make_s3_event(bucket: str, key: str) -> dict:
    return {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": bucket},
                    "object": {"key": key},
                }
            }
        ]
    }


def _setup_bucket(s3, bucket="test-bucket"):
    s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={"LocationConstraint": "eu-west-3"},
    )


def _reload_modules():
    """Reload all modules so they pick up moto's mocked boto3 clients."""
    import csv_service
    import email_service
    import file_service
    import handler
    import report_service

    importlib.reload(csv_service)
    importlib.reload(email_service)
    importlib.reload(file_service)
    importlib.reload(report_service)
    importlib.reload(handler)
    return handler


@mock_aws
def test_happy_path():
    s3 = boto3.client("s3", region_name="eu-west-3")
    ses = boto3.client("ses", region_name="eu-west-3")
    _setup_bucket(s3)
    ses.verify_email_identity(EmailAddress="sender@example.com")

    csv_content = "100,200,300,recipient@example.com\n50,75,25,other@example.com\n"
    s3.put_object(Bucket="test-bucket", Key="uploads/data.csv", Body=csv_content.encode())

    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "uploads/data.csv")
    result = handler.lambda_handler(event, None)

    assert result["statusCode"] == 200
    assert "2 rows" in result["body"]

    # CSV moved to processed
    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="processed/")
    assert objects["KeyCount"] == 1

    # Report saved
    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="reports/")
    assert objects["KeyCount"] == 1

    report_key = objects["Contents"][0]["Key"]
    report = json.loads(s3.get_object(Bucket="test-bucket", Key=report_key)["Body"].read().decode())
    assert report["successful_rows"] == 2
    assert report["failed_rows"] == 0


@mock_aws
def test_partial_failures():
    s3 = boto3.client("s3", region_name="eu-west-3")
    ses = boto3.client("ses", region_name="eu-west-3")
    _setup_bucket(s3)
    ses.verify_email_identity(EmailAddress="sender@example.com")

    csv_content = "100,200,300,recipient@example.com\nabc,200,300,other@example.com\n"
    s3.put_object(Bucket="test-bucket", Key="uploads/data.csv", Body=csv_content.encode())

    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "uploads/data.csv")
    result = handler.lambda_handler(event, None)

    assert result["statusCode"] == 200

    # Report should show 1 success, 1 error
    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="reports/")
    report_key = objects["Contents"][0]["Key"]
    report = json.loads(s3.get_object(Bucket="test-bucket", Key=report_key)["Body"].read().decode())
    assert report["successful_rows"] == 1
    assert report["failed_rows"] == 1


@mock_aws
def test_empty_csv():
    s3 = boto3.client("s3", region_name="eu-west-3")
    _setup_bucket(s3)

    s3.put_object(Bucket="test-bucket", Key="uploads/empty.csv", Body=b"")

    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "uploads/empty.csv")
    result = handler.lambda_handler(event, None)

    assert result["statusCode"] == 200

    # Report still generated
    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="reports/")
    assert objects["KeyCount"] == 1


@mock_aws
def test_non_csv_file():
    s3 = boto3.client("s3", region_name="eu-west-3")
    _setup_bucket(s3)

    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "uploads/data.txt")
    result = handler.lambda_handler(event, None)

    assert "Ignored" in result["body"]


@mock_aws
def test_wrong_prefix():
    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "processed/data.csv")
    result = handler.lambda_handler(event, None)

    assert "Ignored" in result["body"]


@mock_aws
def test_idempotency_file_already_moved():
    s3 = boto3.client("s3", region_name="eu-west-3")
    _setup_bucket(s3)
    # Don't put any file — simulate already-moved scenario

    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "uploads/data.csv")
    result = handler.lambda_handler(event, None)

    assert "Ignored" in result["body"]


@mock_aws
def test_header_row_skipped():
    s3 = boto3.client("s3", region_name="eu-west-3")
    ses = boto3.client("ses", region_name="eu-west-3")
    _setup_bucket(s3)
    ses.verify_email_identity(EmailAddress="sender@example.com")

    csv_content = "col1,col2,col3,email\n100,200,300,recipient@example.com\n"
    s3.put_object(Bucket="test-bucket", Key="uploads/data.csv", Body=csv_content.encode())

    handler = _reload_modules()
    event = _make_s3_event("test-bucket", "uploads/data.csv")
    result = handler.lambda_handler(event, None)

    assert "1 rows" in result["body"]

    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="reports/")
    report_key = objects["Contents"][0]["Key"]
    report = json.loads(s3.get_object(Bucket="test-bucket", Key=report_key)["Body"].read().decode())
    assert report["total_rows"] == 1
