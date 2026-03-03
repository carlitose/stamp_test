import importlib
import json

import boto3
from moto import mock_aws


@mock_aws
def test_save_report_structure():
    s3 = boto3.client("s3", region_name="eu-south-1")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-south-1"},
    )

    import report_service

    importlib.reload(report_service)

    results = [
        {"row_number": 1, "status": "success", "recipient_email": "a@b.com", "sum": 600.0, "error_message": None},
        {"row_number": 2, "status": "error", "recipient_email": None, "sum": None, "error_message": "invalid"},
    ]

    report_service.save_report("test-bucket", "data.csv", results)

    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="reports/")
    assert objects["KeyCount"] == 1

    key = objects["Contents"][0]["Key"]
    body = s3.get_object(Bucket="test-bucket", Key=key)["Body"].read().decode()
    report = json.loads(body)

    assert report["file_name"] == "data.csv"
    assert report["total_rows"] == 2
    assert report["successful_rows"] == 1
    assert report["failed_rows"] == 1
    assert "processed_at" in report
    assert len(report["results"]) == 2


@mock_aws
def test_save_report_empty_results():
    s3 = boto3.client("s3", region_name="eu-south-1")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-south-1"},
    )

    import report_service

    importlib.reload(report_service)

    report_service.save_report("test-bucket", "empty.csv", [])

    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="reports/")
    assert objects["KeyCount"] == 1

    key = objects["Contents"][0]["Key"]
    body = s3.get_object(Bucket="test-bucket", Key=key)["Body"].read().decode()
    report = json.loads(body)

    assert report["total_rows"] == 0
    assert report["successful_rows"] == 0
    assert report["failed_rows"] == 0
