import tiktoken
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_redis import RedisVectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def chunk_transcript(
    transcript: str, chunk_size: int = 500, overlap: int = 50
) -> list[str]:
    """Split transcript into overlapping chunks using tiktoken."""
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(transcript)
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = encoder.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += chunk_size - overlap

    return chunks


def store_embeddings(video_id: str, transcript: str) -> int:
    """Chunk transcript, embed each chunk and store in Redis."""

    chunks = chunk_transcript(transcript)

    documents = [
        Document(
            page_content=chunk,
            metadata={"video_id": str(video_id), "chunk_index": str(i)},
        )
        for i, chunk in enumerate(chunks)
    ]

    RedisVectorStore.from_documents(
        documents=documents,
        embedding=get_embedding_model(),
        redis_url=REDIS_URL,
        index_name=f"video_{video_id}",
    )

    return len(chunks)
