import tiktoken
from google import genai
from langchain_redis import RedisVectorStore
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")


class GeminiEmbeddings(Embeddings):
    """Custom embedding class using native Google genai SDK directly."""

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            result = self.client.models.embed_content(
                model="text-embedding-004", contents=text
            )
            embeddings.append(result.embeddings[0].values)
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model="text-embedding-004", contents=text
        )
        return result.embeddings[0].values


def get_embedding_model():
    return GeminiEmbeddings()


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
        Document(page_content=chunk, metadata={"video_id": video_id, "chunk_index": i})
        for i, chunk in enumerate(chunks)
    ]

    RedisVectorStore.from_documents(
        documents=documents,
        embedding=get_embedding_model(),
        redis_url=REDIS_URL,
        index_name=f"video:{video_id}",
    )

    return len(chunks)
