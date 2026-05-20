import json
import mimetypes
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.models.response_models import VlmModelResponse
from app.core.config import settings
from app.services.encode_image_service import encode_image


async def call_vlm(image_path: str, results: list):
    """
    Calls the VLM with the image at image_path and the retrieved context chunks.
    Automatically detects the MIME type and encodes the image to Base64.
    """
    model = ChatOpenAI(
        model=settings.VLM_MODEL, 
        api_key=settings.VLM_API_KEY, 
        base_url=settings.VLM_BASE_URL
    )
    
    # Encode image and detect MIME type
    image_base64 = encode_image(image_path)
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg" # Fallback
        
    context_text = "\n".join([f"Context: {res[0]}" for res in results])
    
    prompt = f"""Based on the following context, analyze the provided image.
    
    Retrieved text chunks:
    {context_text}
    
    Determine if the image correctly represents the topic, 
    provide a confidence score, and a brief synthesis summary which tells
    if the fetched image is contextually accurate and 
    relevant to the facts stated in the retrieved text chunks?"""

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {
                "type": "image_url", 
                "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}
            }
        ]
    )
    
    # Use LangChain's structured output feature
    structured_model = model.with_structured_output(VlmModelResponse)
    
    try:
        response = await structured_model.ainvoke([message])
        return response.model_dump()
    except Exception as e:
        print(f"Structured output error: {e}")
        return {
            "is_relevant": False,
            "confidence_score": 0.0,
            "synthesis_summary": f"Failed to get structured output: {str(e)}"
        }