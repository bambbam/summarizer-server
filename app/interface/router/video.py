
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.infrastructure.base import get_db
from app.infrastructure.now import get_now
from app.infrastructure.video_repository import VideoRepository
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
async def delete_video(key: str, dynamodb=Depends(get_db)):
    repo = VideoRepository(dynamodb=dynamodb)
    


class UploadVideo(BaseModel):
    url: str

@router.post("/upload")
async def upload_video(request: UploadVideo, dynamodb=Depends(get_db), username=Depends(get_current_user)):
    repo = VideoRepository(dynamodb=dynamodb)
    current_time = get_now()
    ret = repo.put(
        user_name=username["user"],
        video_url=request.url,
        current_time=current_time
    )
    if ret is not None:
        return ret
    raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"db error"
        )
    
