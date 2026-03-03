import logging

import boto3

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
                "Body": {"Text": {"Data": f"The sum of your values is: {sum_value}"}},
            },
        )
        logger.info(f"Email sent to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {recipient}: {e}")
        return False
