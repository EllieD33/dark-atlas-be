from app.utils.datetime_utils import parse_datetime_safe


def transform_urlhaus_entry(entry: dict) -> dict:
    """Normalise UrlHaus entry into DB-ready dict."""
    return {
        "type": "url",
        "value": entry["url"],
        "source": "UrlHaus",
        "first_seen": parse_datetime_safe(entry.get("date_added")),
        "last_seen": parse_datetime_safe(entry.get("last_online")),
        "raw_data": entry,
    }