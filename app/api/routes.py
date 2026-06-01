from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    IngestRequest,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)
from app.core.transcript import fetch_transcript
from app.core.embeddings import store_embeddings
from app.core.retriever import query_video
from app.services.cache import is_video_cached, cache_video, get_cached_video

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest_video(request: IngestRequest):
    try:
        # step 1 - fetch transcript
        result = fetch_transcript(str(request.url))
        video_id = result["video_id"]

        # step 2 - check cache
        if is_video_cached(video_id):
            cached = get_cached_video(video_id)
            return IngestResponse(
                video_id=video_id,
                title=cached["title"],
                transcript_length=int(cached["transcript_length"]),
                message="Video already ingested. Ready for querying.",
            )

        # step 3 - store embeddings
        chunk_count = store_embeddings(video_id, result["transcript"])

        # step 4 - cache video metadata
        cache_video(
            video_id=video_id,
            title="N/A",
            transcript_length=result["transcript_length"],
        )
        return IngestResponse(
            video_id=video_id,
            title="N/A",
            transcript_length=result["transcript_length"],
            message="Video ingested and ready for querying.",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/query", response_model=QueryResponse)
def query_video_endpoint(request: QueryRequest):
    try:
        print(f"QUERY RECEIVED - video_id: {request.video_id}")
        print(f"QUERY RECEIVED - question: {request.question}")

        if not is_video_cached(request.video_id):
            raise HTTPException(
                status_code=404,
                detail="Video not found. Please ingest the video first.",
            )

        print("CACHE CHECK PASSED")
        result = query_video(request.video_id, request.question)
        print(f"QUERY DONE - answer: {result['answer'][:50]}")

        return QueryResponse(
            video_id=request.video_id,
            question=request.question,
            answer=result["answer"],
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
