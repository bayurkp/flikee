import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/generate-dummy")
def generate_video_dummy(data: GenerateRequest, request: Request):
    return {
        "message": "Video successfully generated.",
        "execution_time": 101.94125,
        "result": {
            "voiceover": {
                "name": "voiceover.wav",
                "url": "http://localhost:8000/storage/20250619_223440/voiceover.wav"
            },
            "subtitle": {
                "name": "subtitle.srt",
                "url": "http://localhost:8000/storage/20250619_223440/subtitle.srt"
            },
            "video": {
                "name": "output.mp4",
                "url": "http://localhost:8000/storage/20250619_223440/output.mp4",
                "clips": [
                    {
                        "name": "0.mp4",
                        "url": "http://localhost:8000/storage/20250619_223440/0.mp4"
                    },
                    {
                        "name": "1.mp4",
                        "url": "http://localhost:8000/storage/20250619_223440/1.mp4"
                    }
                ]
            }
        },
        "keywords": [
            "lush green rice paddies",
            "serene countryside landscape",
            "peaceful village life"
        ],
        "relevant_videos": [
            {
                "source": "pixabay",
                "keyword": "serene countryside landscape",
                "description": "cows countryside golden hour aerial view serene tranquil grazing animals nature landscape drone",
                "url": "https://cdn.pixabay.com/video/2024/09/17/231942_medium.mp4",
                "duration": 16,
                "width": 2560,
                "height": 1440,
                "thumbnail": "https://cdn.pixabay.com/video/2024/09/17/231942_medium.jpg",
                "similarity_score": 0.23076923076923078
            },
            {
                "source": "pixabay",
                "keyword": "peaceful village life",
                "description": "coast sea field ocean peaceful village cornwall island",
                "url": "https://cdn.pixabay.com/video/2024/11/25/243201_medium.mp4",
                "duration": 80,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2024/11/25/243201_medium.jpg",
                "similarity_score": 0.2222222222222222
            },
            {
                "source": "pixabay",
                "keyword": "serene countryside landscape",
                "description": "lamb farm animal sheep wool animals eating nature landscape livestock countryside",
                "url": "https://cdn.pixabay.com/video/2022/06/19/120739-724673230_medium.mp4",
                "duration": 19,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2022/06/19/120739-724673230_medium.jpg",
                "similarity_score": 0.16666666666666666
            },
            {
                "source": "pixabay",
                "keyword": "serene countryside landscape",
                "description": "trees forest snow track winter dji drone sky nature countryside landscape",
                "url": "https://cdn.pixabay.com/video/2023/12/07/192357-892475199_medium.mp4",
                "duration": 35,
                "width": 2560,
                "height": 1440,
                "thumbnail": "https://cdn.pixabay.com/video/2023/12/07/192357-892475199_medium.jpg",
                "similarity_score": 0.16666666666666666
            },
            {
                "source": "pixabay",
                "keyword": "serene countryside landscape",
                "description": "country road scenic road argentine countryside drone aerial view dawn landscape rural argentina sunrise over fields tranquil morning dawn serene nature landscape",
                "url": "https://cdn.pixabay.com/video/2024/04/04/206883_medium.mp4",
                "duration": 15,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://cdn.pixabay.com/video/2024/04/04/206883_medium.jpg",
                "similarity_score": 0.15789473684210525
            },
            {
                "source": "pexels",
                "keyword": "serene countryside landscape",
                "description": "scenic landscape with grazing horses",
                "url": "https://videos.pexels.com/video-files/32608637/13905755_360_640_24fps.mp4",
                "duration": 5,
                "width": 2160,
                "height": 3840,
                "thumbnail": "https://images.pexels.com/videos/32608637/at-ve-yayla-32608637.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=630",
                "similarity_score": 0.14285714285714285
            },
            {
                "source": "pixabay",
                "keyword": "lush green rice paddies",
                "description": "rice paddy burning fire",
                "url": "https://cdn.pixabay.com/video/2020/06/15/42084-431423022_medium.mp4",
                "duration": 15,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2020/06/15/42084-431423022_medium.jpg",
                "similarity_score": 0.14285714285714285
            },
            {
                "source": "pexels",
                "keyword": "serene countryside landscape",
                "description": "breathtaking mountain river landscape view",
                "url": "https://videos.pexels.com/video-files/32628869/13913334_640_360_30fps.mp4",
                "duration": 22,
                "width": 3840,
                "height": 2160,
                "thumbnail": "https://images.pexels.com/videos/32628869/springhouse-32628869.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0.14285714285714285
            },
            {
                "source": "pixabay",
                "keyword": "serene countryside landscape",
                "description": "road train countryside forest daylight sunset netherlands drenthe summer afternoon sun flora peaceful serene scenic drone traffic transport travel nature landscape",
                "url": "https://cdn.pixabay.com/video/2024/08/09/225610_medium.mp4",
                "duration": 28,
                "width": 720,
                "height": 1280,
                "thumbnail": "https://cdn.pixabay.com/video/2024/08/09/225610_medium.jpg",
                "similarity_score": 0.14285714285714285
            },
            {
                "source": "pexels",
                "keyword": "lush green rice paddies",
                "description": "rice ready to be harvested",
                "url": "https://videos.pexels.com/video-files/1557401/1557401-hd_1280_720_30fps.mp4",
                "duration": 8,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://images.pexels.com/videos/1557401/free-video-1557401.jpg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0.125
            },
            {
                "source": "pixabay",
                "keyword": "peaceful village life",
                "description": "river stream water creek village outdoor flow waterbirds ducks geese tranquil peaceful calm idyllic bridge town 139718812",
                "url": "https://cdn.pixabay.com/video/2015/10/08/912-141851660_medium.mp4",
                "duration": 16,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2015/10/08/912-141851660_medium.jpg",
                "similarity_score": 0.1111111111111111
            },
            {
                "source": "pexels",
                "keyword": "lush green rice paddies",
                "description": "rice fields in the mountain valley",
                "url": "https://videos.pexels.com/video-files/5188732/5188732-sd_426_240_30fps.mp4",
                "duration": 35,
                "width": 3840,
                "height": 2160,
                "thumbnail": "https://images.pexels.com/videos/5188732/aerial-agriculture-ancient-architecture-5188732.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0.1111111111111111
            },
            {
                "source": "pexels",
                "keyword": "lush green rice paddies",
                "description": "the growing grains of a rice plant",
                "url": "https://videos.pexels.com/video-files/5301104/5301104-sd_960_540_30fps.mp4",
                "duration": 11,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://images.pexels.com/videos/5301104/pexels-photo-5301104.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0.1
            },
            {
                "source": "pixabay",
                "keyword": "lush green rice paddies",
                "description": "farmers rice field paddy vietnam mekong delta",
                "url": "https://cdn.pixabay.com/video/2020/06/15/42085-431423026_medium.mp4",
                "duration": 15,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2020/06/15/42085-431423026_medium.jpg",
                "similarity_score": 0.1
            },
            {
                "source": "pixabay",
                "keyword": "lush green rice paddies",
                "description": "storks flying birds rice field vietnam paddy peaceful",
                "url": "https://cdn.pixabay.com/video/2020/06/15/42088-431423042_medium.mp4",
                "duration": 16,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2020/06/15/42088-431423042_medium.jpg",
                "similarity_score": 0.09090909090909091
            },
            {
                "source": "pixabay",
                "keyword": "lush green rice paddies",
                "description": "birds paddy rice nature peace vietnam field countryside",
                "url": "https://cdn.pixabay.com/video/2020/06/15/42092-431423052_medium.mp4",
                "duration": 18,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2020/06/15/42092-431423052_medium.jpg",
                "similarity_score": 0.09090909090909091
            },
            {
                "source": "pixabay",
                "keyword": "peaceful village life",
                "description": "turtle ocean tortoise wildlife underwater snorkeling marine life sea life",
                "url": "https://cdn.pixabay.com/video/2024/12/03/244754_medium.mp4",
                "duration": 30,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://cdn.pixabay.com/video/2024/12/03/244754_medium.jpg",
                "similarity_score": 0.09090909090909091
            },
            {
                "source": "pixabay",
                "keyword": "lush green rice paddies",
                "description": "birds storks flying paddy peace countryside rice field sky",
                "url": "https://cdn.pixabay.com/video/2020/07/02/43612-436648506_medium.mp4",
                "duration": 15,
                "width": 2560,
                "height": 1440,
                "thumbnail": "https://cdn.pixabay.com/video/2020/07/02/43612-436648506_medium.jpg",
                "similarity_score": 0.08333333333333333
            },
            {
                "source": "pixabay",
                "keyword": "peaceful village life",
                "description": "rooster chicken village farm polygamy country house family bird natural economy animal husbandry",
                "url": "https://cdn.pixabay.com/video/2017/07/16/10685-226624850_medium.mp4",
                "duration": 14,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2017/07/16/10685-226624850_medium.jpg",
                "similarity_score": 0.06666666666666667
            },
            {
                "source": "pixabay",
                "keyword": "peaceful village life",
                "description": "tree lights stars sky spinning fantasy glowing glow fairy dream tree of life life happy meditation prana spiritual spirituality branches flowers bloom blossom peace",
                "url": "https://cdn.pixabay.com/video/2022/12/28/144562-784867427_medium.mp4",
                "duration": 40,
                "width": 1280,
                "height": 720,
                "thumbnail": "https://cdn.pixabay.com/video/2022/12/28/144562-784867427_medium.jpg",
                "similarity_score": 0.041666666666666664
            },
            {
                "source": "pexels",
                "keyword": "serene countryside landscape",
                "description": "scenic view of horses grazing on lush plateau",
                "url": "https://videos.pexels.com/video-files/32619616/13909618_640_360_50fps.mp4",
                "duration": 9,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://images.pexels.com/videos/32619616/horse-grazing-majestic-mountains-valley--32619616.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "peaceful village life",
                "description": "man carrying a bag while walking",
                "url": "https://videos.pexels.com/video-files/4684807/4684807-sd_640_360_25fps.mp4",
                "duration": 10,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://images.pexels.com/videos/4684807/pexels-photo-4684807.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "serene countryside landscape",
                "description": "vibrant red poppies swaying in spring breeze",
                "url": "https://videos.pexels.com/video-files/32621359/13910451_360_640_25fps.mp4",
                "duration": 14,
                "width": 1080,
                "height": 1920,
                "thumbnail": "https://images.pexels.com/videos/32621359/pexels-photo-32621359.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=630",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "peaceful village life",
                "description": "a red cabin in the snow with pine trees",
                "url": "https://videos.pexels.com/video-files/6507555/6507555-sd_240_426_25fps.mp4",
                "duration": 15,
                "width": 1080,
                "height": 1920,
                "thumbnail": "https://images.pexels.com/videos/6507555/architecture-beautiful-blizzard-branches-6507555.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=630",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "lush green rice paddies",
                "description": "aerial shot of a landscape",
                "url": "https://videos.pexels.com/video-files/6981437/6981437-hd_1920_1080_25fps.mp4",
                "duration": 16,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://images.pexels.com/videos/6981437/pexels-photo-6981437.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "serene countryside landscape",
                "description": "graceful white horses grazing in scenic swedish meadow",
                "url": "https://videos.pexels.com/video-files/32621535/13910525_360_640_25fps.mp4",
                "duration": 17,
                "width": 1080,
                "height": 1920,
                "thumbnail": "https://images.pexels.com/videos/32621535/2025-4k-nature-4k-resolution-4k-vertical-32621535.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=630",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "peaceful village life",
                "description": "a laundry hanging out to dry in a window",
                "url": "https://videos.pexels.com/video-files/4440936/4440936-sd_960_540_25fps.mp4",
                "duration": 17,
                "width": 1920,
                "height": 1080,
                "thumbnail": "https://images.pexels.com/videos/4440936/pexels-photo-4440936.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "lush green rice paddies",
                "description": "drone footage of cropland",
                "url": "https://videos.pexels.com/video-files/4232200/4232200-sd_960_540_24fps.mp4",
                "duration": 19,
                "width": 3840,
                "height": 2160,
                "thumbnail": "https://images.pexels.com/videos/4232200/pexels-photo-4232200.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "peaceful village life",
                "description": "mother and son working in the fields",
                "url": "https://videos.pexels.com/video-files/5674592/5674592-sd_640_360_25fps.mp4",
                "duration": 22,
                "width": 3840,
                "height": 2160,
                "thumbnail": "https://images.pexels.com/videos/5674592/boy-with-mother-farm-indian-village-5674592.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
                "similarity_score": 0
            },
            {
                "source": "pexels",
                "keyword": "peaceful village life",
                "description": "a person reaching up to a tree with a branch",
                "url": "https://videos.pexels.com/video-files/4887910/4887910-sd_338_640_25fps.mp4",
                "duration": 43,
                "width": 2160,
                "height": 4096,
                "thumbnail": "https://images.pexels.com/videos/4887910/pexels-photo-4887910.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=630",
                "similarity_score": 0
            }
        ]
    }
