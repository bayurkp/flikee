from typing import Optional
from pydantic import BaseModel, HttpUrl


class Video(BaseModel):
    source: str
    keyword: str
    description: Optional[str]
    url: HttpUrl
    duration: Optional[float]
    width: Optional[float]
    height: Optional[float]
    thumbnail: Optional[HttpUrl]
    similarity_score: Optional[float]
