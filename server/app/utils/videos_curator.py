import os
from urllib.parse import urlparse
import requests
from typing import List, Optional
from app.models.video import Video
from app.utils.logger import setup_logger
from app.utils.similarity_score import compute_similarity_score

logger = setup_logger(__name__)


def _parse_video(
    source: str,
    keyword: str,
    description: Optional[str],
    url: str,
    duration: Optional[float],
    width: Optional[float],
    height: Optional[float],
    thumbnail: Optional[str],
    similarity_score: Optional[float]
) -> Optional[Video]:
    try:
        return Video(
            source=source,
            keyword=keyword,
            description=description,
            url=url,
            duration=duration,
            width=width,
            height=height,
            thumbnail=thumbnail,
            similarity_score=similarity_score
        )
    except Exception as e:
        logger.warning(f"[{source.capitalize()}] Skipping invalid video: {e}")
        return None


def _pixabay(query: str, limit: int = 5) -> List[Video]:
    def get_description(tags: str) -> str:
        return tags.replace(",", "")

    api_key = os.getenv("PIXABAY_API_KEY")
    base_url = os.getenv("PIXABAY_BASE_URL")

    params = {
        "key": api_key,
        "q": query,
        "orientation": "horizontal",
        "page": 1,
        "per_page": limit,
        "safesearch": "true"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(
            f"[Pixabay] {len(data.get('hits', []))} results for '{query}'")
    except Exception as e:
        logger.error(f"[Pixabay] Failed to fetch for '{query}': {e}")
        return []

    videos = []
    for item in data.get("hits", []):
        medium = item.get("videos", {}).get("medium")
        tags = item.get("tags", "")
        description = get_description(tags)
        similarity_score = compute_similarity_score(
            source_text=description,
            reference_text=query
        )

        if medium:
            video = _parse_video(
                source="pixabay",
                keyword=query,
                description=description,
                url=medium.get("url"),
                duration=item.get("duration"),
                width=medium.get("width"),
                height=medium.get("height"),
                thumbnail=medium.get("thumbnail"),
                similarity_score=similarity_score
            )
            if video:
                videos.append(video)

    return videos


def _pexels(query: str, limit: int = 5) -> List[Video]:
    def get_description(url: str) -> str:
        path = urlparse(url).path
        slug = path.strip("/").split("/")[-1]
        words = slug.split("-")[:-1]
        return " ".join(words)

    api_key = os.getenv("PEXELS_API_KEY")
    base_url = os.getenv("PEXELS_BASE_URL")

    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "orientation": "horizontal",
        "page": 1,
        "per_page": limit
    }

    try:
        response = requests.get(base_url + "search",
                                headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(
            f"[Pexels] {len(data.get('videos', []))} results for '{query}'")
    except Exception as e:
        logger.error(f"[Pexels] Failed to fetch for '{query}': {e}")
        return []

    videos = []
    for item in data.get("videos", []):
        files = item.get("video_files", [])
        description = get_description(item.get("url"))
        similarity_score = compute_similarity_score(
            source_text=description,
            reference_text=query
        )

        if files:
            video = _parse_video(
                source="pexels",
                keyword=query,
                description=description,
                url=files[0].get("link"),
                duration=item.get("duration"),
                width=item.get("width"),
                height=item.get("height"),
                thumbnail=item.get("image"),
                similarity_score=similarity_score
            )
            if video:
                videos.append(video)

    return videos


def curate_videos(
    keywords: List[str],
    limit_per_source: int = 5
) -> List[Video]:
    logger.info(f"Starting video curation for keywords: {keywords}")
    videos = []

    for query in keywords:
        videos.extend(_pixabay(query, limit_per_source))
        videos.extend(_pexels(query, limit_per_source))

    videos.sort(
        key=lambda v: (
            -1 * (v.similarity_score or 0.0),  # similarity (desc)
            v.duration or float("inf")         # duration (asc)
        )
    )

    logger.info(f"Total curated videos: {len(videos)}")
    return videos
