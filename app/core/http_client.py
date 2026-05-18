import httpx
from typing import Optional
from app.core.config import settings

class HttpClient:
    _client: Optional[httpx.AsyncClient] = None

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT, follow_redirects=True)
        return cls._client

    @classmethod
    async def close(cls):
        if cls._client:
            await cls._client.aclose()
            cls._client = None

# Singleton-like access
async def get_http_client() -> httpx.AsyncClient:
    return await HttpClient.get_client()
