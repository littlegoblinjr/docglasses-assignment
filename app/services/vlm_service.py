import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from app.models.response_models import VlmModelResponse
from app.core.config import settings


async def call_vlm(image_base64: str, results: list):
    model = ChatOpenAI(
        model=settings.VLM_MODEL, 
        api_key=settings.VLM_API_KEY, 
        base_url=settings.VLM_BASE_URL
    )
    
    context_text = "\n".join([f"Context: {res[0]}" for res in results])
    
    prompt = f"""Based on the following context, analyze the provided image.
    
    Retrieved text chunks:
    {context_text}
    
    Determine if the image correctly represents the topic, 
    provide a confidence score, and a brief synthesis summary 
    Is the fetched image contextually accurate and 
    relevant to the facts stated in the retrieved text chunks?."""

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
        ]
    )
    
    # Use LangChain's structured output feature
    structured_model = model.with_structured_output(VlmModelResponse)
    
    try:
        response = await structured_model.ainvoke([message])
        # response is an instance of VlmModelResponse
        return response.model_dump()
    except Exception as e:
        print(f"Structured output error: {e}")
        return {
            "is_relevant": False,
            "confidence_score": 0.0,
            "synthesis_summary": f"Failed to get structured output: {str(e)}"
        }