from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import jwt

from app.infrastructure.user import User, get_user_repo
import bcrypt

## TODO 토큰 비밀키 .env로 따로 뺴기
SECRET_PRE = "123"

router = APIRouter(
    prefix='/user',
    tags=["users"]
)

@router.post('/signup')
def create_user(request:User, repo=Depends(get_user_repo)):
    hashed_pass = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
    user_object = request.dict()
    user_object["password"] = hashed_pass
    print(repo.create(user_object))
    return {
        "res": "created"
    }


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), repo=Depends(get_user_repo)):
    user = repo.get(request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
    if not bcrypt.checkpw(request.password.encode("utf-8"), user["password"].value):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
    access_token = jwt.encode({
        'exp': datetime.utcnow() + timedelta(seconds=300),
        'user': user["username"]
    },SECRET_PRE, algorithm="HS256")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def decode_token(token):
    try:
        return jwt.decode(token, SECRET_PRE, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="user/login")
def get_current_user(token: str=Depends(oauth2_sheme)):
    print(token)
    token_check = decode_token(token)
    if token_check is status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=token_check,detail = f'not authorized token')
    return token_check

@router.get("/")
def read_root(current_user: str=Depends(get_current_user)):
    return current_user


        

