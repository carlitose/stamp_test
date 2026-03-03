import logging

from csv_service import download_csv, parse_csv
from email_service import send_result
from file_service import file_exists, move_to_processed
from report_service import save_report
from validator import is_header_row, validate_row

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Lambda entry point. Processes CSV from S3 event."""
    # 1. Extract bucket and key from S3 event
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    logger.info(f"Processing file: s3://{bucket}/{key}")

    # 2. Validate event
    if not key.startswith("uploads/"):
        logger.warning(f"File not in uploads/ prefix: {key}")
        return {"statusCode": 200, "body": "Ignored: not in uploads/"}

    if not key.endswith(".csv"):
        logger.warning(f"File is not a CSV: {key}")
        return {"statusCode": 200, "body": "Ignored: not a CSV"}

    # 3. Idempotency check
    if not file_exists(bucket, key):
        logger.warning(f"File not found (already processed?): {key}")
        return {"statusCode": 200, "body": "Ignored: file not found"}

    # 4. Download and parse CSV
    content = download_csv(bucket, key)
    rows = parse_csv(content)

    # 5. Skip header if present
    if rows and is_header_row(rows[0]):
        logger.info("Header row detected, skipping")
        rows = rows[1:]

    # 6. Process rows
    results = []
    file_name = key.split("/")[-1]

    for i, row in enumerate(rows, start=1):
        validation = validate_row(row, i)

        if not validation["valid"]:
            logger.error(validation["error"])
            results.append({
                "row_number": i,
                "status": "error",
                "recipient_email": row[3] if len(row) > 3 else None,
                "sum": None,
                "error_message": validation["error"],
            })
            continue

        sum_value = sum(validation["values"])
        email = validation["email"]
        email_sent = send_result(email, sum_value)

        results.append({
            "row_number": i,
            "status": "success" if email_sent else "error",
            "recipient_email": email,
            "sum": sum_value,
            "error_message": None if email_sent else f"Failed to send email to {email}",
        })

    # 7. Save report
    save_report(bucket, file_name, results)

    # 8. Move to processed
    move_to_processed(bucket, key)

    # 9. Log summary
    successful = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "error")
    logger.info(f"Processing complete: {len(results)} total, {successful} successful, {failed} failed")

    return {
        "statusCode": 200,
        "body": f"Processed {len(results)} rows: {successful} successful, {failed} failed",
    }
