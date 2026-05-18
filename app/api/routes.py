from fastapi import APIRouter, Depends, HTTPException
from app.services.wikipedia_service import fetch_wikipedia_content, fetch_wikipedia_image
from app.services.chunking_service import chunk_text
import asyncio
import time
from app.models.request_models import QueryRequest
from app.services.embedding_service import get_embeddings_for_chunks
from app.services.vector_store_service import vector_store
from app.services.download_image_service import download_image
from app.services.encode_image_service import encode_image
from app.services.vlm_service import call_vlm
from app.core.config import settings

router = APIRouter()

@router.post("/analyze")
async def analyze_document(payload: QueryRequest):
    start_time = time.time()


    wiki_data = await fetch_wikipedia_content(payload.topic)
    wiki_image = await fetch_wikipedia_image(payload.topic)

    if not wiki_data:
        raise HTTPException(status_code=404, detail="Topic not found")

    chunks = await chunk_text(wiki_data)
    embeddings = get_embeddings_for_chunks(chunks)
    vector_store.add(embeddings, chunks)
    
    query_topic = payload.topic.replace("_", " ")
    query_embedding = get_embeddings_for_chunks([query_topic])[0]
    results = vector_store.search(query_embedding, k=settings.TOP_K_CHUNKS)

    encoded_image = None
    if wiki_image:
        image_path = await download_image(wiki_image)
        encoded_image = encode_image(image_path)

    vlm_response = "No image available for analysis."
    if encoded_image:
        vlm_response = await call_vlm(encoded_image, results)
                
                
    return {
        "topic": payload.topic,
        "execution_metrics":{
            "time_taken_seconds": time.time() - start_time,
            "chunks_evaluated": len(results),
            },
        "retrieved_context":[
            result[0] for result in results
        ],

        "verification_results":{
            "image_url": wiki_image,

            "image_is_relevant": vlm_response.get("is_relevant"),

            "confidence_score": vlm_response.get("confidence_score"),

            "synthesis_summary": vlm_response.get("synthesis_summary")
        }
        
    }