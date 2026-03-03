import importlib

import boto3
from moto import mock_aws


@mock_aws
def test_send_result_success():
    ses = boto3.client("ses", region_name="eu-west-3")
    ses.verify_email_identity(EmailAddress="sender@example.com")

    import email_service

    importlib.reload(email_service)

    result = email_service.send_result("recipient@example.com", 600.0)
    assert result is True


@mock_aws
def test_send_result_failure():
    # Don't verify sender — SES will reject
    import email_service

    importlib.reload(email_service)

    result = email_service.send_result("recipient@example.com", 600.0)
    assert result is False
