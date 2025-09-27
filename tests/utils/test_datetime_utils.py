import pytest
from datetime import datetime, timezone
from app.utils.datetime_utils import parse_datetime_safe


@pytest.mark.parametrize("input_str, expected", [
    # Valid ISO with Z suffix (UTC)
    ("2024-01-01T12:00:00Z", datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)),

    # Valid ISO with offset
    ("2024-01-01T12:00:00+02:00", datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc).astimezone(timezone.utc).astimezone()),

    # Naive datetime -> assume UTC
    ("2024-01-01T12:00:00", datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)),

    # Already UTC aware
    ("2024-01-01T12:00:00+00:00", datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)),

    # Empty string
    ("", None),

    # None input
    (None, None),

    # Malformed string
    ("not-a-date", None),

    # Invalid format
    ("2024-13-01T12:00:00Z", None),
])
def test_parse_datetime_safe(input_str, expected):
    result = parse_datetime_safe(input_str)

    if expected is None:
        assert result is None
    else:
        # Compare aware datetimes in UTC for consistency
        assert result is not None
        assert result.astimezone(timezone.utc) == expected.astimezone(timezone.utc)
