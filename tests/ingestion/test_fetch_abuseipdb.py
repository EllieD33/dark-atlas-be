import aiohttp
import pytest
from unittest.mock import AsyncMock, patch
from app.ingestion.abuseipdb_client import fetch_aipdb_blacklist

@pytest.mark.asyncio
async def test_fetch_blacklist():
    fake_data = [
        {"ipAddress": "1.2.3.4", "confidence": 100},
        {"ipAddress": "5.6.7.8", "confidence": 90},
    ]

    with patch("aiohttp.ClientSession.get") as mock_get:
        mock_response = AsyncMock()
        mock_response.__aenter__.return_value.json.return_value = fake_data
        mock_get.return_value = mock_response

        async with aiohttp.ClientSession() as session:
            result = await fetch_aipdb_blacklist(session)
            assert result == fake_data
