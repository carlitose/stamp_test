import boto3
import pytest
from moto import mock_aws


@mock_aws
def test_download_csv():
    s3 = boto3.client("s3", region_name="eu-south-1")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-south-1"},
    )
    s3.put_object(Bucket="test-bucket", Key="uploads/data.csv", Body=b"1,2,3,a@b.com\n")

    from csv_service import download_csv

    content = download_csv("test-bucket", "uploads/data.csv")
    assert content == "1,2,3,a@b.com\n"


@mock_aws
def test_download_csv_file_not_found():
    s3 = boto3.client("s3", region_name="eu-south-1")
    s3.create_bucket(
        Bucket="test-bucket",
        CreateBucketConfiguration={"LocationConstraint": "eu-south-1"},
    )

    from csv_service import download_csv

    with pytest.raises(Exception):
        download_csv("test-bucket", "uploads/nonexistent.csv")


def test_parse_csv_standard():
    from csv_service import parse_csv

    content = "100,200,300,user@example.com\n50,75,25,other@example.com\n"
    rows = parse_csv(content)
    assert len(rows) == 2
    assert rows[0] == ["100", "200", "300", "user@example.com"]
    assert rows[1] == ["50", "75", "25", "other@example.com"]


def test_parse_csv_whitespace_trimming():
    from csv_service import parse_csv

    content = " 100 , 200 , 300 , user@example.com \n"
    rows = parse_csv(content)
    assert rows[0] == ["100", "200", "300", "user@example.com"]


def test_parse_csv_empty():
    from csv_service import parse_csv

    rows = parse_csv("")
    assert rows == []
