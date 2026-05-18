import numpy as np
import faiss


class VectorStore:
    def __init__(self):
        self.index = None
        self.embeddings = []
        self.chunks = []

    def add(self, embeddings, chunks):
        self.embeddings = embeddings
        self.chunks = chunks
        self.index = faiss.IndexFlatL2(len(embeddings[0]))
        self.index.add(np.array(embeddings).astype('float32'))

    def search(self, query_embedding, k=2):
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), k)
        return [(self.chunks[i], float(distances[0][j])) for j, i in enumerate(indices[0])]


vector_store = VectorStore()