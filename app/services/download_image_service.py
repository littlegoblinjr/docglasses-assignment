import os
import uuid
from app.core.http_client import get_http_client
from app.core.config import settings


async def download_image(image_url: str):
    if not image_url:
        return None
    os.makedirs("images", exist_ok=True)
    
    image_id = str(uuid.uuid4()) + ".jpg"
    image_path = f"images/{image_id}"
    
    headers = {
        "User-Agent": settings.USER_AGENT
    }
    
    client = await get_http_client()
    response = await client.get(image_url, headers=headers)
    if response.status_code != 200:
        return None
    with open(image_path, "wb") as f:
        f.write(response.content)
    return image_path