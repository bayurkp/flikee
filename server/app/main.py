import os
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from app.utils.logger import setup_logger
from app.utils.videos_processor import process_video
from app.utils.voiceover_generator import generate_voiceover
from app.utils.subtitle_generator import generate_subtitle
from app.utils.keywords_extractor import extract_keywords
from app.utils.constant import STORAGE_DIR
from app.utils.videos_curator import curate_videos
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

logger = setup_logger(__name__)
app = FastAPI()

app.mount("/storage", StaticFiles(directory="storage"), name="storage")


class GenerateRequest(BaseModel):
    text: str


@app.post("/generate")
def generate_video(data: GenerateRequest, request: Request):
    start_time = datetime.now()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = STORAGE_DIR / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    # Video Script
    text = data.text

    # Generate voiceover dan subtitle
    voiceover_path, duration = generate_voiceover(text, str(output_dir))
    subtitle_path = generate_subtitle(
        str(voiceover_path), text, str(output_dir))

    # Extract keywords
    keywords = extract_keywords(text)

    # Curate videos
    relevant_videos = curate_videos(keywords)

    # Process video
    output_path, clips = process_video(
        relevant_videos,
        str(output_dir),
        str(voiceover_path),
        str(subtitle_path),
        duration
    )

    # Generate URLs
    base_url = str(request.base_url).rstrip("/")
    storage_url = f"{base_url}/storage/{timestamp}"
    voiceover_url = f"{storage_url}/{Path(voiceover_path).name}"
    subtitle_url = f"{storage_url}/{Path(subtitle_path).name}"
    video_url = f"{storage_url}/{Path(output_path).name}"

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()
    logger.info(f"Video generated in {end_time - start_time}")

    return {
        "message": "Video successfully generated.",
        "execution_time": execution_time,
        "result": {
            "voiceover": {
                "name": Path(voiceover_path).name,
                "url": voiceover_url,
            },
            "subtitle": {
                "name": Path(subtitle_path).name,
                "url": subtitle_url,
            },
            "video": {
                "name": Path(output_path).name,
                "url": video_url,
                "clips":  [
                    {
                        "name": Path(clip).name,
                        "url": f"{storage_url}/{Path(clip).name}"
                    }
                    for clip in clips
                ]
            },
        },
        "keywords": keywords,
        "relevant_videos": relevant_videos,
    }
