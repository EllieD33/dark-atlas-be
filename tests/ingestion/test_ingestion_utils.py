import pytest_asyncio
import pytest
from aiohttp import ClientSession, ClientResponseError, ClientError
from unittest.mock import AsyncMock, patch
from app.ingestion.utils import fetch_json


@pytest_asyncio.fixture
async def aiohttp_session():
    """Provides a reusable aiohttp.ClientSession for tests."""
    async with ClientSession() as session:
        yield session


@pytest.mark.asyncio
async def test_fetch_json_success(aiohttp_session):
    mock_response = AsyncMock()
    mock_response.raise_for_status = AsyncMock(return_value=None)
    mock_response.json = AsyncMock(return_value={"data": [1, 2, 3]})

    mock_cm = AsyncMock()
    mock_cm.__aenter__.return_value = mock_response

    with patch("aiohttp.ClientSession.get", return_value=mock_cm):
        result = await fetch_json(aiohttp_session, "http://fake.url")
        assert result == {"data": [1, 2, 3]}


@pytest.mark.asyncio
async def test_fetch_json_http_error(aiohttp_session):
    mock_response = AsyncMock()
    mock_response.raise_for_status = AsyncMock(
        side_effect=ClientResponseError(
            request_info=None, history=(), status=404
        )
    )
    mock_response.json = AsyncMock(return_value=None)

    mock_cm = AsyncMock()
    mock_cm.__aenter__.return_value = mock_response

    with patch("aiohttp.ClientSession.get", return_value=mock_cm):
        result = await fetch_json(aiohttp_session, "http://fake.url")
        assert result is None


@pytest.mark.asyncio
async def test_fetch_json_network_error(aiohttp_session):
    with patch("aiohttp.ClientSession.get", side_effect=ClientError("Network fail")):
        result = await fetch_json(aiohttp_session, "http://fake.url")
        assert result is None
