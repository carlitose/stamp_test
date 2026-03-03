import importlib

import boto3
from moto import mock_aws


@mock_aws
def test_move_to_processed():
    s3 = boto3.client("s3", region_name="eu-west-3")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-3"},
    )
    s3.put_object(Bucket="test-bucket", Key="uploads/data.csv", Body=b"test content")

    import file_service

    importlib.reload(file_service)

    file_service.move_to_processed("test-bucket", "uploads/data.csv")

    # Original should be gone
    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="uploads/")
    assert objects.get("KeyCount", 0) == 0

    # Should exist in processed/
    objects = s3.list_objects_v2(Bucket="test-bucket", Prefix="processed/")
    assert objects["KeyCount"] == 1
    assert objects["Contents"][0]["Key"] == "processed/data.csv"


@mock_aws
def test_file_exists_true():
    s3 = boto3.client("s3", region_name="eu-west-3")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-3"},
    )
    s3.put_object(Bucket="test-bucket", Key="uploads/data.csv", Body=b"content")

    import file_service

    importlib.reload(file_service)

    assert file_service.file_exists("test-bucket", "uploads/data.csv") is True


@mock_aws
def test_file_exists_false():
    s3 = boto3.client("s3", region_name="eu-west-3")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-west-3"},
    )

    import file_service

    importlib.reload(file_service)

    assert file_service.file_exists("test-bucket", "uploads/nonexistent.csv") is False
