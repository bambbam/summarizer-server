from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.interface import router
from app.interface.router import feature, user, video
from app.settings import Settings



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(video.router)
app.include_router(feature.router)
