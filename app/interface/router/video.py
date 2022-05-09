from fastapi import APIRouter, Depends

from app.infrastructure.base import get_db
from app.infrastructure.video_repository import VideoRepository

router = APIRouter(prefix="/video", tags=["video"])


@router.get("/")
async def read_all_videos(dynamodb=Depends(get_db)):
    repo = VideoRepository(dynamodb=dynamodb)
    return repo.get_all()["Items"]


@router.get("/{key}")
async def read_one_video(key: str, dynamodb=Depends(get_db)):
    repo = VideoRepository(dynamodb=dynamodb)
    return repo.get(key)
