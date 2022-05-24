import bcrypt
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.container import Container
from app.infrastructure.base import get_db
from app.infrastructure.user_repository import User, UserRepository
from app.interface.router.auth import TOKEN, encode_token, get_current_user

router = APIRouter(prefix="/user", tags=["users"])


@router.post("/signup")
@inject
async def create_user(request: User, dynamodb=Depends(get_db)):
    repo = UserRepository(dynamodb=dynamodb)
    hashed_pass = bcrypt.hashpw(request.password.encode("utf-8"), bcrypt.gensalt())
    user_object = request.dict()
    user_object["password"] = hashed_pass
    user = repo.get(request.username)

    if user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Already exist username with this {request.username} username",
        )

    ret = repo.put(User(**user_object))
    if ret:
        return {"res": "created"}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong Username or password"
        )


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(), dynamodb=Depends(get_db)
):
    repo = UserRepository(dynamodb=dynamodb)
    user = repo.get(request.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user found with this {request.username} username",
        )
    if not bcrypt.checkpw(request.password.encode("utf-8"), user["password"].encode()):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Wrong Username or password"
        )
    access_token = encode_token(user, 300, TOKEN.access)

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/")
async def read_root(current_user: str = Depends(get_current_user)):
    return current_user
