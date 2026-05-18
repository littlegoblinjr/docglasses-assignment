from app.core.config import settings

async def chunk_text(text: str):
    clean_text = " ".join(text.replace("\n", " ").split())
    
    chunk_size = settings.CHUNK_SIZE
    chunk_overlap = settings.CHUNK_OVERLAP
    
    chunks = []
    for i in range(0, len(clean_text), chunk_size - chunk_overlap):
        chunk = clean_text[i:i + chunk_size].strip()
        if len(chunk) > 20: 
            chunks.append(chunk)
            
    return chunks[:5]
