import os
import uuid
import httpx
from app.core.http_client import get_http_client
from app.core.config import settings


async def download_image(image_url: str):
    if not image_url:
        return None
    os.makedirs("images", exist_ok=True)
    
    # Extract extension from URL
    path_without_query = image_url.split('?')[0]
    ext = os.path.splitext(path_without_query)[1]
    if not ext or len(ext) > 5:
        ext = ".jpg" # Fallback
        
    image_id = str(uuid.uuid4()) + ext
    image_path = f"images/{image_id}"
    
    headers = {
        "User-Agent": settings.USER_AGENT
    }
    
    client = await get_http_client()
    try:
        response = await client.get(image_url, headers=headers)
        if response.status_code != 200:
            return None
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    except Exception as e:
        print(f"Image download error: {e}")
        return None