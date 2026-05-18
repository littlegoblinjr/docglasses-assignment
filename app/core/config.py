import os
from pydantic import BaseModel

class Settings(BaseModel):
    # App Config
    PROJECT_NAME: str = "Multimodal RAG Engine"
    
    # Model Configs
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    VLM_MODEL: str = "qwen2.5-vl-3b-instruct"
    VLM_BASE_URL: str = "http://127.0.0.1:1234/v1"
    VLM_API_KEY: str = "not-needed"
    
    # Retrieval Configs
    CHUNK_SIZE: int = 300
    CHUNK_OVERLAP: int = 50
    TOP_K_CHUNKS: int = 2
    
    # Wikipedia / HTTP Configs
    USER_AGENT: str = "MedicalResearchAssistant/1.0 (https://example.org/medicalresearch)"
    HTTP_TIMEOUT: float = 30.0

settings = Settings()
