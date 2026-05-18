from sentence_transformers import SentenceTransformer
from app.core.config import settings


embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)


def get_embeddings_for_chunks(chunks:list[str]):
    return embedding_model.encode(chunks)