import json
import logging
from datetime import UTC, datetime

import boto3

logger = logging.getLogger()
s3_client = boto3.client("s3")


def save_report(bucket: str, file_name: str, results: list[dict]) -> None:
    """Saves JSON report in reports/ on S3."""
    report = {
        "file_name": file_name,
        "processed_at": datetime.now(UTC).isoformat(),
        "total_rows": len(results),
        "successful_rows": sum(1 for r in results if r["status"] == "success"),
        "failed_rows": sum(1 for r in results if r["status"] == "error"),
        "results": results,
    }
    report_key = f"reports/{file_name}_{report['processed_at']}.json"
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=report_key,
            Body=json.dumps(report, indent=2),
            ContentType="application/json",
        )
        logger.info(f"Report saved to {report_key}")
    except Exception as e:
        logger.error(f"Failed to save report: {e}")
