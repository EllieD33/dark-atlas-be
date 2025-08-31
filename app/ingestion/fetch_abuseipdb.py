from dotenv import load_dotenv
import os

from app.ingestion.utils import fetch_json

load_dotenv(".env")

key = os.getenv("AIPDB_KEY")
headers = {
    "Accept": "application/json",
    "Key": key
}

async def fetch_aipdb_blacklist(session):
    url = "https://api.abuseipdb.com/api/v2/blacklist"
    return await fetch_json(session, url, headers=headers)

async def fetch_ip(session, ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    return await fetch_json(session, url, headers=headers, params={"ipAddress": ip})
