import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver"
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "DarkAtlas Threat API"
    assert "version" in data
    assert "docs_url" in data
