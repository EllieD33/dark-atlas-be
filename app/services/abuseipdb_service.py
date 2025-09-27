from datetime import datetime

from app.utils.datetime_utils import parse_datetime_safe


def transform_abuseipdb_entry(entry: dict) -> dict:
    """Normalise AbuseIPDB entry into DB-ready dict."""
    return {
        "type": "ip",
        "value": entry["ipAddress"],
        "source": "AbuseIPDB",
        "first_seen": None,
        "last_seen": parse_datetime_safe(entry.get("lastReportedAt")),
        "raw_data": entry,
    }


