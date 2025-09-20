import pytest
from datetime import datetime, timezone
from app.services.abuseipdb_service import transform_abuseipdb_entry


@pytest.mark.parametrize(
    "entry, expected_last_seen",
    [
        ({"ipAddress": "1.2.3.4", "lastReportedAt": "2025-09-20T12:00:00Z"},
        datetime(2025, 9, 20, 12, 0, 0, tzinfo=timezone.utc)),
        ({"ipAddress": "5.6.7.8"}, None),
    ]
)
def test_transform_abuseipdb_entry(entry, expected_last_seen):
    transformed = transform_abuseipdb_entry(entry)
    assert transformed["type"] == "ip"
    assert transformed["value"] == entry["ipAddress"]
    assert transformed["source"] == "AbuseIPDB"
    assert transformed["last_seen"] == expected_last_seen
    assert transformed["raw_data"] == entry
