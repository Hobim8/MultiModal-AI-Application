from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound 
from urllib.parse import urlparse, parse_qs

def extract_video_id(url: str) -> str:
    """Extract the video ID from the YouTube URL """
    try:
        parsed = urlparse(url)

        #check if it's a youtube url domain
        if parsed.netloc not in ["www.youtube.com", "youtube.com", "youtu.be"]:
            raise ValueError(
                "Invaild YouTube URL. Please provide a valid Youtube URL."
            )
        # Handle standard YouTube URLs
        if parsed.netloc in ["www.youtube.com", "youtube.com", "youtu.be"]:
            video_id = parse_qs(parsed.query).get("v")
            if not video_id:
                raise ValueError(
                    "Please check the link and try again"
                )
            return video_id[0]
        
        # Handle shortened YouTube URLs 
        if parsed.netloc == "youtu.be":
            video_id = parsed.path.lstrip("/")
            if not video_id:
                raise ValueError(
                    "Please check the link and try again"
                )
            return video_id 
        
    except ValueError:
        raise 
    except Exception:
        raise ValueError(
            "An error occurred while extracting the video ID. Please check the link and try again."
        )


            