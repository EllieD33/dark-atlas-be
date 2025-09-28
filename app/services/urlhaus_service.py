from app.utils.datetime_utils import parse_datetime_safe


def transform_urlhaus_entry(entry_id: str, reports: list[dict]) -> list[dict]:
    """Flatten UrlHaus entry and normalise into DB-ready dict(s)."""
    results = []
    for report in reports:
        results.append({
            "type": "url",
            "value": report["url"],
            "source": "UrlHaus",
            "first_seen": parse_datetime_safe(report.get("date_added")),
            "last_seen": parse_datetime_safe(report.get("last_online")),
            "raw_data": {**report, "external_id": entry_id},
        })
    return results
