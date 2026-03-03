from validator import is_header_row, validate_email, validate_row


def test_validate_row_valid_integers():
    result = validate_row(["100", "200", "300", "user@example.com"], 1)
    assert result["valid"] is True
    assert result["values"] == (100.0, 200.0, 300.0)
    assert result["email"] == "user@example.com"


def test_validate_row_valid_decimals():
    result = validate_row(["10.5", "20.3", "-5.1", "user@example.com"], 1)
    assert result["valid"] is True
    assert result["values"] == (10.5, 20.3, -5.1)


def test_validate_row_negative_values():
    result = validate_row(["-10", "20", "30", "user@example.com"], 1)
    assert result["valid"] is True
    assert result["values"] == (-10.0, 20.0, 30.0)


def test_validate_row_missing_columns():
    result = validate_row(["100", "200"], 1)
    assert result["valid"] is False
    assert "expected 4 columns" in result["error"]


def test_validate_row_non_numeric():
    result = validate_row(["abc", "200", "300", "user@example.com"], 1)
    assert result["valid"] is False
    assert "not numeric" in result["error"]


def test_validate_row_invalid_email():
    result = validate_row(["100", "200", "300", "not-an-email"], 1)
    assert result["valid"] is False
    assert "invalid email" in result["error"]


def test_validate_email_valid():
    assert validate_email("user@example.com") is True
    assert validate_email("a@b.co") is True


def test_validate_email_invalid():
    assert validate_email("not-an-email") is False
    assert validate_email("@missing.com") is False
    assert validate_email("no@dots") is False
    assert validate_email("") is False


def test_is_header_row_true():
    assert is_header_row(["col1", "col2", "col3", "email"]) is True


def test_is_header_row_false():
    assert is_header_row(["100", "200", "300", "user@example.com"]) is False


def test_is_header_row_short():
    assert is_header_row(["a", "b"]) is False
