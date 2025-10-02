import aiohttp, gzip, json
from io import BytesIO
from typing import Optional, Any


async def fetch_json(session: aiohttp.ClientSession, url: str, **kwargs):
    """
    Reusable async helper to GET a URL and return JSON.
    Pass headers, params, etc. via kwargs.
    """
    try:
        async with session.get(url, **kwargs) as resp:
            resp.raise_for_status()
            return await resp.json()
    except aiohttp.ClientResponseError as e:
        print(f"HTTP error {e.status} for {url}")
    except aiohttp.ClientError as e:
        print(f"Network error for {url}: {e}")


async def fetch_gzipped_json(session: aiohttp.ClientSession, url: str) -> Optional[Any]:
    """
    Async helper to GET a gzipped JSON resource and return parsed data.
    Returns None if request, decompression, or JSON parsing fails.
    """
    try:
        async with session.get(url) as resp:
            resp.raise_for_status()
            raw_bytes = await resp.read()
            with gzip.GzipFile(fileobj=BytesIO(raw_bytes)) as f:
                data = json.load(f)
            return data
    except aiohttp.ClientResponseError as e:
        print(f"HTTP error {e.status} for {url}")
        return None
    except aiohttp.ClientError as e:
        print(f"Network error for {url}: {e}")
        return None
    except (OSError, json.JSONDecodeError) as e:
        print(f"Failed to decompress or parse JSON from {url}: {e}")
        return None
