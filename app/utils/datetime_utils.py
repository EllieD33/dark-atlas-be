from datetime import datetime, timezone
from typing import Optional

def parse_datetime_safe(value: Optional[str]) -> Optional[datetime]:
    """
    Parse a datetime string into a timezone-aware datetime object.
    Returns None if parsing fails or value is None.

    Handles common cases like:
    - ISO format with 'Z' suffix
    - naive datetime (assumed UTC)
    """
    if not value:
        return None

    try:
        cleaned = value.replace("Z", "+00:00")
        dt = datetime.fromisoformat(cleaned)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt


    except (ValueError, TypeError):
        return None
