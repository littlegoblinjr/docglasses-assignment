from pydantic import BaseModel


class VlmModelResponse(BaseModel):
    is_relevant: bool
    confidence_score: float
    synthesis_summary: str