## TODO 토큰 비밀키 .env로 따로 뺴기
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_PRE = "123"


def encode_token(user, secret_pre=SECRET_PRE):
    return jwt.encode(
        {"exp": datetime.utcnow() + timedelta(seconds=300), "user": user["username"]},
        secret_pre,
        algorithm="HS256",
    )


def decode_token(token, sercret_pre=SECRET_PRE):
    try:
        return jwt.decode(token, sercret_pre, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED


oauth2_sheme = OAuth2PasswordBearer(tokenUrl="user/login")


def get_current_user(token: str = Depends(oauth2_sheme)):
    token_check = decode_token(token)
    if token_check is status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=token_check, detail=f"not authorized token")
    return token_check
