from fastapi import APIRouter

router = APIRouter(
    prefix='/video',
    tags=["video"]
)

@router.get("/")
async def read_all_videos():
    return [{"username": "Rick"}, {"username": "Morty"}]
