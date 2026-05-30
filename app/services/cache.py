import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(REDIS_URL)


def is_video_cached(video_id: str) -> bool:
    """Check if the video has already been ingested"""
    return redis_client.exists(f"cached:video:{video_id}") == 1


def cache_video(video_id: str, title: str, transcript_length: int) -> None:
    """Stores video metadata in redis after successful ingestion"""
    key = f"cached:video:{video_id}"
    redis_client.hset(
        key,
        mapping={
            "video_id": video_id,
            "title": title,
            "transcript_length": transcript_length,
        },
    )
    redis_client.expire(key, 604800)


def get_cached_video(video_id: str) -> dict | None:
    """retrieve cached video metadata"""
    data = redis_client.hgetall(f"cached:video:{video_id}")
    if not data:
        return None
    return {k.decode(): v.decode() for k, v in data.items()}


def delete_cached_video(video_id: str) -> None:
    """Delete a cached video from Redis."""
    redis_client.delete(f"cached:video:{video_id}")
