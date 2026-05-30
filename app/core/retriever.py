import os
import google.genai as genai
from langchain_redis import RedisVectorStore
from app.core.embeddings import get_embedding_model

# Redis connection URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# system prompt
SYSTEM_PROMPT = """
You are an intelligent YouTube video assistant.
Your job is to answer the user's questions based strictly and only on the transcript context provided below.

Rules you must follow:
- Only use information from the provided context to answer
- If the answer is not found in the context, say "I could not find that information in this video" — do not guess or make up an answer
- Keep answers clear, concise and easy to understand
- If the user asks for a summary, summarize only what is in the context
- Never refer to the context as "the transcript" — refer to it as "the video"
"""


def retrieve_relevant_chunks(video_id: str, question: str, top_k: int = 5) -> list[str]:
    """Search Redis for the most relevant transcript chunks for a given question."""

    vector_store = RedisVectorStore(
        embeddings=get_embedding_model(),
        redis_url=REDIS_URL,
        index_name=f"video:{video_id}",
    )

    results = vector_store.similarity_search(question, k=top_k)
    return [doc.page_content for doc in results]


def build_prompt(context_chunks: list[str], question: str) -> str:
    """Build the prompt by combining retrieved context and the user question."""

    context = "\n\n".join(context_chunks)

    prompt = f"""
Context from the video:
{context}

User question:
{question}

Answer the queation only on the context above.
"""
    return prompt


def query_video(video_id: str, question: str) -> dict:
    """Retrieve relevant chunks and query Gemini for an answer."""

    # step 1 check if we have relevant chuncks
    chunks = retrieve_relevant_chunks(video_id, question)

    if not chunks:
        return {
            "answer": "I could not find any relevant information in this video for your question.",
        }

    # step 2 build the prompt
    prompt = build_prompt(chunks, question)

    # initialize the embedding model
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt,
        config={"system_instruction": "SYSTEM_PROMPT"},
    )

    return {"answer": response.text}
