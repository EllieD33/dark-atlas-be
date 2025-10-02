import pytest, pytest_asyncio, gzip, json
from io import BytesIO
from aiohttp import ClientSession, ClientResponseError, ClientError
from unittest.mock import AsyncMock, Mock, patch
from app.ingestion.utils import fetch_json, fetch_gzipped_json


@pytest_asyncio.fixture
async def aiohttp_session():
    """Provides a reusable aiohttp.ClientSession for tests."""
    async with ClientSession() as session:
        yield session


# --- Tests for fetch_json ---

@pytest.mark.asyncio
async def test_fetch_json_success(aiohttp_session):
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(return_value=None)
    mock_response.json = AsyncMock(return_value={"data": [1, 2, 3]})

    mock_cm = AsyncMock()
    mock_cm.__aenter__.return_value = mock_response

    with patch("aiohttp.ClientSession.get", return_value=mock_cm):
        result = await fetch_json(aiohttp_session, "http://fake.url")
        assert result == {"data": [1, 2, 3]}


@pytest.mark.asyncio
async def test_fetch_json_http_error(aiohttp_session):
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(
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


# --- Tests for fetch_gzipped_json ---

@pytest.mark.asyncio
async def test_fetch_gzipped_json_success(aiohttp_session):
    data = {"foo": "bar", "nums": [1, 2, 3]}
    compressed = BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode="w") as f:
        f.write(json.dumps(data).encode("utf-8"))

    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(return_value=None)
    mock_response.read = AsyncMock(return_value=compressed.getvalue())

    mock_cm = AsyncMock()
    mock_cm.__aenter__.return_value = mock_response

    with patch("aiohttp.ClientSession.get", return_value=mock_cm):
        result = await fetch_gzipped_json(aiohttp_session, "http://fake.url")
        assert result == data


@pytest.mark.asyncio
async def test_fetch_gzipped_json_bad_gzip(aiohttp_session):
    bad_bytes = b"not-a-valid-gzip-file"

    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(return_value=None)
    mock_response.read = AsyncMock(return_value=bad_bytes)

    mock_cm = AsyncMock()
    mock_cm.__aenter__.return_value = mock_response

    with patch("aiohttp.ClientSession.get", return_value=mock_cm):
        result = await fetch_gzipped_json(aiohttp_session, "http://fake.url")
        assert result is None


@pytest.mark.asyncio
async def test_fetch_gzipped_json_http_error(aiohttp_session):
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(
        side_effect=ClientResponseError(
            request_info=None, history=(), status=500
        )
    )
    mock_response.read = AsyncMock(return_value=b"")

    mock_cm = AsyncMock()
    mock_cm.__aenter__.return_value = mock_response

    with patch("aiohttp.ClientSession.get", return_value=mock_cm):
        result = await fetch_gzipped_json(aiohttp_session, "http://fake.url")
        assert result is None


@pytest.mark.asyncio
async def test_fetch_gzipped_json_network_error(aiohttp_session):
    with patch("aiohttp.ClientSession.get", side_effect=ClientError("Boom")):
        result = await fetch_gzipped_json(aiohttp_session, "http://fake.url")
        assert result is None
