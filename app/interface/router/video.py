from typing import List, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.infrastructure.base import COMMAND, get_db
from app.infrastructure.now import get_now
from app.infrastructure.redis_producer import RedisProducer, get_queue, get_rabbit_queue
from app.infrastructure.video_repository import VideoData, VideoRepository
from app.interface.router.auth import get_current_user

router = APIRouter(prefix="/video", tags=["video"])


@router.get("/")
async def read_all_videos(dynamodb=Depends(get_db)):
    repo = VideoRepository(dynamodb=dynamodb)
    return repo.get_all()["Items"]


@router.get("/{key}")
async def read_one_video(key: str, dynamodb=Depends(get_db)):
    repo = VideoRepository(dynamodb=dynamodb)
    return repo.get(key)


@router.delete("/{key}")
async def delete_video(
    key: str, dynamodb=Depends(get_db), username=Depends(get_current_user)
):
    repo = VideoRepository(dynamodb=dynamodb)
    res = repo.delete(key=key, username=username)
    if res:
        return {"deleted": key}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"there is no element with {key}"
    )


class UploadVideo(BaseModel):
    key: str


@router.post("/upload")
async def upload_video(
    request: UploadVideo, dynamodb=Depends(get_db), username=Depends(get_current_user)
):
    repo = VideoRepository(dynamodb=dynamodb)
    current_time = get_now()
    ret = repo.put(
        user_name=username["user"], current_time=current_time, key=request.key
    )
    if ret:
        return {"uploaded": request.key}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"db error"
    )


class ExtractFeature(COMMAND):
    type: Literal["ExtractFeature"]
    key: str


@router.post("/extract")
async def extract_feature(
    request: ExtractFeature,
    dynamodb=Depends(get_db),
    username=Depends(get_current_user),
    producer=Depends(get_rabbit_queue),
):
    repo = VideoRepository(dynamodb=dynamodb)
    ret = repo.get(key=request.key)
    if ret is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no such video of {request.key} key",
        )
    ret = repo.put(
        user_name=ret.user_name,
        current_time=ret.start_time,
        key=ret.key,
        status="in_queue"
    )
    producer.put(request)

class ShortenVideo(COMMAND):
    type: Literal["ShortenVideo"]
    key: str
    must_include_feature: List[str]

@router.post("/shorten")
async def shorten_video(
    request: ShortenVideo,
    dynamodb=Depends(get_db),
    producer=Depends(get_rabbit_queue),
):
    repo = VideoRepository(dynamodb=dynamodb)
    ret = repo.get(key=request.key)
    if ret is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"no such video of {request.key} key",
        )
    ret = repo.put(
        user_name=ret.user_name,
        current_time=ret.start_time,
        key=ret.key,
        status="shorten_start"
    )
    producer.put(request)
