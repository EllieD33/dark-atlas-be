import aiohttp

async def fetch_json(session: aiohttp.ClientSession, url: str, **kwargs):
    """
    Reusable async helper to GET a URL and return JSON.
    Pass headers, params, etc. via kwargs.
    """
    try:
        async with session.get(url, **kwargs) as resp:
            await resp.raise_for_status()
            return await resp.json()
    except aiohttp.ClientResponseError as e:
        print(f"HTTP error {e.status} for {url}")
    except aiohttp.ClientError as e:
        print(f"Network error for {url}: {e}")
