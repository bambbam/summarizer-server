import bcrypt
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.container import Container
from app.infrastructure.base import get_db
from app.infrastructure.feature_repository import FeatureRepository
from app.infrastructure.user_repository import User, UserRepository
from app.interface.router.auth import TOKEN, encode_token, get_current_user

router = APIRouter(prefix="/feature", tags=["feautures"])

@router.get("/{key}")
def get_video_feature(key: str, dynamodb=Depends(get_db)):
    repo = FeatureRepository(dynamodb=dynamodb)
    ret = repo.get(key)
    if ret is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Feature is not found with {key}",
        )
    return ret
