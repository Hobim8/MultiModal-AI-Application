from pydantic import BaseModel, HttpUrl
from typing import Optional


# ingest schema
class IngestRequest(BaseModel):
    url: HttpUrl


class IngestResponse(BaseModel):
    video_id: str
    title: str
    transcript_lenght: int
    message: str


# query schema
class QueryRequest(BaseModel):
    video_id: str
    question: str


class QueryResponse(BaseModel):
    video_id: str
    question: str
    answer: str
    
