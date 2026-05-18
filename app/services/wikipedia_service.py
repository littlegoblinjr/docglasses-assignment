from urllib.parse import quote
import wikipediaapi
import httpx
from app.core.http_client import get_http_client
from app.core.config import settings


async def fetch_wikipedia_image(topic: str):
    encoded_topic = quote(topic)

    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_topic}"
    headers = {
        "User-Agent": settings.USER_AGENT
    }

    client = await get_http_client()
    response = await client.get(url, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    thumbnail = data.get("thumbnail", {})
    if thumbnail:
        return thumbnail.get("source")
    return None

async def fetch_wikipedia_content(topic:str):
    wiki_wiki = wikipediaapi.AsyncWikipedia(settings.USER_AGENT, 'en')
    page_py =  wiki_wiki.page(topic)
    if not await page_py.exists():
        return None
    return await page_py.text