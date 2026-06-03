# YouTube Query AI 🎬

A multimodal AI application that allows users to query YouTube videos in natural language without watching them. Submit a YouTube URL, ask questions, and get accurate answers grounded strictly in the video content.

## Features

- Submit any YouTube video URL and extract its transcript automatically
- Ask natural language questions about the video content
- Answers are grounded strictly in the video content using RAG (Retrieval Augmented Generation)
- Redis vector store for fast semantic search across transcript chunks
- Caching layer to avoid re-ingesting the same video twice
- Clean dark themed web UI built with HTML, CSS and JavaScript
- Whisper fallback for videos without available transcripts

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python 3.13 |
| LLM | Google Gemini Flash |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Store | Redis Stack |
| Transcript Extraction | youtube-transcript-api, yt-dlp |
| Chunking | tiktoken |
| Package Manager | UV |
| Containerization | Docker, Docker Compose |

## Project Structure

    youtube-query-ai/
    ├── app/
    │   ├── main.py                  
    │   ├── api/
    │   │   └── routes.py            
    │   ├── core/
    │   │   ├── transcript.py        
    │   │   ├── embeddings.py        
    │   │   └── retriever.py         
    │   ├── services/
    │   │   └── cache.py             
    │   └── models/
    │       └── schemas.py           
    ├── static/
    │   ├── index.html               
    │   ├── style.css                
    │   └── app.js                   
    ├── Dockerfile
    ├── docker-compose.yml
    └── pyproject.toml

## How It Works

1. User submits a YouTube URL through the web interface
2. The system extracts the transcript using youtube-transcript-api
3. The transcript is chunked into 500 token overlapping segments using tiktoken
4. Each chunk is embedded using Sentence Transformers and stored in Redis vector store
5. When a question is asked, it is converted to an embedding and Redis performs similarity search
6. The most relevant chunks are retrieved and passed to Gemini as context
7. Gemini answers strictly based on the provided context — no hallucination

## Getting Started

### Prerequisites

- Python 3.13
- Docker Desktop
- UV package manager
- Google Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikeys)

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/youtube-query-ai.git
cd youtube-query-ai
```

2. Install dependencies

```bash
uv sync
```

3. Create a `.env` file in the project root
4. Start Redis Stack

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```

5. Run the application

```bash
uv run uvicorn app.main:app --reload
```

6. Open your browser and go to `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/ingest` | Submit a YouTube URL for ingestion |
| POST | `/query` | Ask a question about an ingested video |
| GET | `/docs` | Interactive API documentation |

## Docker Compose

To run the entire stack with one command:

```bash
docker compose up --build
```

> **Note:** The Docker build requires CPU-only PyTorch. If you experience large CUDA package downloads during the build, ensure your environment is configured for CPU only usage.

## Environment Variables

| Variable | Description |
|----------|-------------|
| GEMINI_API_KEY | Your Google Gemini API key |
| REDIS_URL | Redis connection URL (default: redis://localhost:6379) |

## Future Improvements

- Whisper transcription fallback for videos without captions
- Multimodal frame analysis for visual questions
- Video history and session management
- RAGAS evaluation metrics for RAG quality assessment
- User authentication
