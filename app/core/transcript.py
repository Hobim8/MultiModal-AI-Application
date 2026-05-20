from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)
from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    """Extract the video ID from the YouTube URL"""
    try:
        parsed = urlparse(url)

        # check if it's a youtube url domain
        if parsed.netloc not in ["www.youtube.com", "youtube.com", "youtu.be"]:
            raise ValueError("Invaild YouTube URL. Please provide a valid Youtube URL.")
        # Handle standard YouTube URLs
        if parsed.netloc in ["www.youtube.com", "youtube.com"]:
            video_id = parse_qs(parsed.query).get("v")
            if not video_id:
                raise ValueError("Please check the link and try again")
            return video_id[0]

        # Handle shortened YouTube URLs
        if parsed.netloc == "youtu.be":
            video_id = parsed.path.lstrip("/")
            if not video_id:
                raise ValueError("Please check the link and try again")
            return video_id

    except ValueError:
        raise
    except Exception:
        raise ValueError(
            "An error occurred while extracting the video ID. Please check the link and try again."
        )


def fetch_transcript(url: str) -> dict:
    """Fetch the transcript of the youtube video"""

    video_id = extract_video_id(url)

    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_chunks = ytt_api.fetch(video_id)

        transcript = " ".join(chunk.text for chunk in transcript_chunks).strip()

        return {
            "video_id": video_id,
            "transcript": transcript,
            "transcript_length": len(transcript.split()),
        }

    except TranscriptsDisabled:
        raise ValueError(
            "This video has transcripts disabled. Automatic transcription will be used as a fallback."
        )

    except NoTranscriptFound:
        raise ValueError(
            "No transcript was found for this video. Automatic transcription will be used as a fallback."
        )

    except Exception as e:
        raise ValueError(f"Unable to retrieve the transcript: {str(e)}")
