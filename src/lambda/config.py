import os


class Config:
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    AWS_REGION = os.environ.get("AWS_REGION", "eu-west-3")
    REPORT_PREFIX = "reports/"
    PROCESSED_PREFIX = "processed/"
    UPLOADS_PREFIX = "uploads/"
