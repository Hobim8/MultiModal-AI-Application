from fastapi import APIRouter, HTTPException
from app.models.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from app.core.transcript import fetch_transcript

router = APIRouter()

@router.post("/ingest", response_model=IngestResponse)
def ingest_video(request: IngestRequest):
    try:
        result = fetch_transcript(str(request.url))
        return IngestResponse(
            video_id=result["video_id"],
            title="N/A",
            transcript_lenght=result["transcript_Length"],
            message="Video transcript successfully extracted and ready for querying.",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error please try again Later."
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

