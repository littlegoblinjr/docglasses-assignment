# Dynamic Multimodal-RAG & Fact-Verification Engine

A high-performance, cost-effective FastAPI microservice designed for automated fact-verification. This engine dynamically fetches Wikipedia content and images, performs local vector search (RAG), and uses an open-source vision-language model (VLM) to verify if visual media accurately matches retrieved text facts.

## Key Features
- **Zero-OpEx Architecture**: Uses free APIs and local models to avoid recurring API costs.
- **Asynchronous Pipeline**: Built with FastAPI and `httpx` for efficient I/O and high concurrency.
- **Multimodal RAG**: Combines local vector search with vision-language synthesis for grounded verification.
- **Centralized Configuration**: Easily swap models, change thresholds, or update API endpoints via a single config file.

## System Architecture
The backend is structured into four distinct layers:

1. **Layer 1: Data Ingestion**: Dynamically queries the Wikipedia API to extract raw text and showcase image URLs.
2. **Layer 2: Local RAG**: Segments text into semantic chunks and embeds them using local models indexed in a FAISS store.
3. **Layer 3: Semantic Retrieval**: Executes a local vector search to pull the most relevant context chunks for a given topic.
4. **Layer 4: Synthesis & Verification**: Forwards the retrieved chunks and the image to an open-source VLM for grounded fact-verification.

## Setup Instructions

### Prerequisites
- Python 3.9+
- A VLM endpoint (e.g., LM Studio, Ollama, or an OpenAI-compatible API)

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd <project-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
All system settings, including model names, API endpoints, and retrieval parameters, are managed in `app/core/config.py`. You can modify this file to change:
- `EMBEDDING_MODEL`: The local model used for text vectorization.
- `VLM_MODEL`: The multimodal model used for verification.
- `VLM_BASE_URL`: The endpoint URL for your VLM inference server.
- `CHUNK_SIZE` / `CHUNK_OVERLAP`: Parameters for text segmentation.

### Running the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

### POST `/analyze`
Analyzes a topic by fetching data and verifying relevant images.

**Request Body:**
```json
{
  "topic": "Tesla Model Y",
  "query": "Is the fetched image contextually accurate and relevant to the facts stated in the retrieved text chunks?"
}
```

**Sample cURL Request:**
```bash
curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"topic": "Tesla_Model_Y"}'
```

**Sample Response Payload:**
```json
{
    "topic": "Tesla Model Y",
    "execution_metrics": {
        "time_taken_seconds": 6.654642581939697,
        "chunks_evaluated": 2
    },
    "retrieved_context": [
        "The Tesla Model Y is a battery electric compact crossover SUV produced by Tesla, Inc. since 2020. Presented in March 2019 as the company's fifth production model, the Model Y is the best-selling electric vehicle of all time, having sold more than 2.16 million units worldwide. After its 2019 introduc",
        "r styling. While most Model Y are configured with two-row seating, in the US the Model Y offered optional third-row seats for a seven-passenger seating capacity until the 2025 refresh. In 2023, Tesla delivered 1.2 million Model Ys, making it the world's best-selling vehicle that year, surpassing the"
    ],
    "verification_results": {
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/2022_Tesla_Model_Y_Long_Range_AWD_Front.jpg/330px-2022_Tesla_Model_Y_Long_Range_AWD_Front.jpg",
        "image_is_relevant": true,
        "confidence_score": 0.95,
        "synthesis_summary": "The image depicts a blue Tesla Model Y, which is a battery electric compact crossover SUV produced by Tesla, Inc. The car is shown parked on a street with a brick building in the background."
    }
}
```
