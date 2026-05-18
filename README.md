# Dynamic Multimodal-RAG & Fact-Verification Engine

A high-performance, production-ready FastAPI microservice designed for automated fact-verification. This engine dynamically fetches Wikipedia content and images, performs local vector search (RAG), and utilizes an open-source vision-language model (VLM) to verify if visual media accurately matches retrieved text facts.

## 🛠️ Project Philosophy: Zero-OpEx & High Performance
The design of this engine focuses on three core principles:
1. **Zero Operating Expense (Zero-OpEx)**: Leverages only free APIs and high-performance local models to avoid recurring third-party API costs.
2. **Deterministic Outputs**: Uses Pydantic-enforced structured outputs (JSON) to ensure the VLM response integrates seamlessly with downstream industrial pipelines.
3. **Optimized Resource Management**: Implements connection pooling and asynchronous non-blocking I/O to maximize hardware utilization.

---

## 🏗️ Deep-Dive Architecture

The backend implements a sophisticated 4-layer pipeline:

### 1. Dynamic Ingestion Layer
- **Wikipedia REST API**: Custom implementation using asynchronous `httpx` to fetch real-time page summaries and primary showcase images.
- **Smart User-Agents**: Implements unique User-Agent strings to ensure compliance with Wikimedia's API policies and prevent rate limiting.

### 2. Local RAG Pipeline (Vector Layer)
- **Semantic Chunking**: Employs a character-based sliding window strategy (300-char size, 50-char overlap) in `chunking_service.py` to preserve context across boundaries.
- **Local Embeddings**: Utilizes the `all-MiniLM-L6-v2` sentence-transformer. Chosen for its exceptional balance between performance (384-dimensional vectors) and low latency on CPU.
- **FAISS Vector Store**: Uses Facebook AI Similarity Search (`faiss-cpu`) for sub-millisecond similarity search, making it perfectly suited for edge deployment or low-cost server environments.

### 3. Asynchronous Retrieval & Context Matching
- **K-Nearest Neighbors (k=2)**: The system takes the topic's core premise, vectorizes it, and retrieves the top 2 most semantically similar chunks from the local memory store.
- **Parallel Task Readiness**: The engine is built using `asyncio`, allowing it to handle hundreds of concurrent requests without blocking the event loop.

### 4. Multimodal Synthesis & Grounded Verification
- **VLM Integration**: Connects to open-source models (like Qwen2.5-VL) via an OpenAI-compatible local endpoint.
- **Structured Pydantic Validation**: All VLM outputs are validated against a strict `VlmModelResponse` schema, ensuring `image_is_relevant` (bool), `confidence_score` (float), and `synthesis_summary` (string) are always typed correctly.
- **Base64 Encoding Pipeline**: Images are downloaded and encoded on-the-fly to minimize disk I/O and latency.

---

## ⚙️ Configuration & Production Readiness
The project features a **Centralized Configuration System** in `app/core/config.py`. This ensures compliance with "The Twelve-Factor App" principles, allowing you to swap models or update endpoints without modifying any service logic.

| Setting | Purpose |
| :--- | :--- |
| `EMBEDDING_MODEL` | Swap local transformer models (e.g., `all-mpnet-base-v2`). |
| `VLM_BASE_URL` | Redirect inference to local servers or cloud providers. |
| `HTTP_TIMEOUT` | Global control over network request tolerances. |
| `CHUNK_SIZE` | Tune the granularity of the RAG pipeline. |

---

## 🚀 Setup & Execution

### Prerequisites
- Python 3.9+
- A VLM endpoint (e.g., LM Studio, Ollama) running locally.

### Installation & Launch
```bash
# Clone the repository
git clone <repo-url>
cd <project-directory>

# Install optimized dependencies
pip install -r requirements.txt

# Start the high-concurrency server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Documentation

### POST `/analyze`
Performs dynamic data fetching, RAG search, and multimodal fact verification.

**Request Body:**
```json
{
  "topic": "Tesla Model Y"
}
```

**Sample Response:**
The engine provides **Execution Metrics** for observability, including total time taken and chunk counts.

```json
{
    "topic": "Tesla Model Y",
    "execution_metrics": {
        "time_taken_seconds": 6.65,
        "chunks_evaluated": 2
    },
    "retrieved_context": [
        "The Tesla Model Y is a battery electric compact crossover SUV produced by Tesla, Inc. since 2020...",
        "In 2023, Tesla delivered 1.2 million Model Ys, making it the world's best-selling vehicle that year..."
    ],
    "verification_results": {
        "image_url": "https://upload.wikimedia.org/.../Model_Y_Front.jpg",
        "image_is_relevant": true,
        "confidence_score": 0.95,
        "synthesis_summary": "The image depicts a blue Tesla Model Y, which is accurately described in the retrieved chunks."
    }
}
```

---

## 💎 Why This Engine Stands Out
- **Observability**: Built-in execution metrics track RAG and Inference efficiency.
- **Connection Pooling**: Uses a shared `HttpClient` to reuse TCP connections, slashing network latency.
- **Modular Services**: Decoupled `embedding`, `vector`, `chunking`, and `vlm` services allow for easy unit testing and replacement.
- **Type Safety**: End-to-end Pydantic models for both requests and responses.
