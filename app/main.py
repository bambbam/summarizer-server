from fastapi import Depends, FastAPI

from app.interface.router import user, video

app = FastAPI()

app.include_router(user.router)
app.include_router(video.router)
