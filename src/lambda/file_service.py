import logging

import boto3

logger = logging.getLogger()
s3_client = boto3.client("s3")


def move_to_processed(bucket: str, key: str) -> None:
    """Moves file from uploads/ to processed/."""
    new_key = key.replace("uploads/", "processed/", 1)
    s3_client.copy_object(
        Bucket=bucket,
        Key=new_key,
        CopySource={"Bucket": bucket, "Key": key},
    )
    s3_client.delete_object(Bucket=bucket, Key=key)
    logger.info(f"Moved {key} → {new_key}")


def file_exists(bucket: str, key: str) -> bool:
    """Checks if a file exists in S3."""
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except s3_client.exceptions.ClientError:
        return False
