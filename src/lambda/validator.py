import logging
import re

logger = logging.getLogger()
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str) -> bool:
    """Validates email format with a simple regex."""
    return bool(EMAIL_REGEX.match(email))


def validate_row(row: list[str], row_number: int) -> dict:
    """
    Validates a CSV row.
    Returns: {"valid": True, "values": (n1, n2, n3), "email": str}
    or:      {"valid": False, "error": str}
    """
    if len(row) < 4:
        return {"valid": False, "error": f"Row {row_number}: expected 4 columns, got {len(row)}"}

    values = []
    for i in range(3):
        try:
            values.append(float(row[i]))
        except ValueError:
            return {"valid": False, "error": f"Row {row_number}: column {i + 1} is not numeric: '{row[i]}'"}

    email = row[3]
    if not validate_email(email):
        return {"valid": False, "error": f"Row {row_number}: invalid email: '{email}'"}

    return {"valid": True, "values": tuple(values), "email": email}


def is_header_row(row: list[str]) -> bool:
    """Detects if a row is a header by checking if the first 3 values are non-numeric."""
    if len(row) < 3:
        return False
    for i in range(3):
        try:
            float(row[i])
        except ValueError:
            return True
    return False
