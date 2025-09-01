from datetime import datetime


def transform_abuseipdb_entry(entry: dict) -> dict:
    """Normalise AbuseIPDB entry into DB-ready dict."""
    return {
        "type": "ip",
        "value": entry["ipAddress"],
        "source": "AbuseIPDB",
        "first_seen": None,
        "last_seen": (
            datetime.fromisoformat(entry["lastReportedAt"].replace("Z", "+00:00"))
            if entry.get("lastReportedAt")
            else None
        ),
        "raw_data": entry,
    }


