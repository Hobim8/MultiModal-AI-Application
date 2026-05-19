from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from app.core.transcript import fetch_transcript
from app.core.embeddings import store_embeddings
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
                message="Video already ingested. Ready for querying."
            )
        
        # step 3 - store embeddings
        chunk_count = store_embeddings(video_id, result["transcript"])

        # step 4 - cache video metadata 
        cache_video(
            video_id=video_id,
            title="N/A",
            transcript_lenght=result["transcript_length"]
        )
        return IngestResponse(
            video_id=video_id,
            title="N/A",
            transcript_lenght=result["transcript_length"],
            message="Video ingested and ready for querying."
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="unexpected error occurred Please try again."
        )
    

    
@router.post("/query", response_model=QueryResponse)
def query_video(request: QueryRequest):
    try:
        return QueryResponse(
            video_id = request.video_id,
            question = request.question,
            answer = "Coming soon",
            source_chunks= None
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error please try again."
        )

