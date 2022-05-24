## TODO 토큰 비밀키 .env로 따로 뺴기
from datetime import datetime, timedelta
from enum import Enum
from tokenize import Token

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


class TOKEN(Enum):
    access = "access"
    refresh = "refresh"


def get_tokens(user):
    return (
        encode_token(user, 300, TOKEN.access),
        encode_token(user, 3600, TOKEN.refresh),
    )


def encode_token(user, expire_time, secret_pre: TOKEN):
    return jwt.encode(
        {
            "exp": datetime.utcnow() + timedelta(seconds=expire_time),
            "user": user["username"],
        },
        secret_pre.name,
        algorithm="HS256",
    )


def decode_token(token, secret_pre: TOKEN):
    try:
        return jwt.decode(token, secret_pre.name, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        return status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED


oauth2_sheme = OAuth2PasswordBearer(tokenUrl="user/login")


def get_current_user(token: str = Depends(oauth2_sheme)):
    token_check = decode_token(token, TOKEN.access)
    if token_check is status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=token_check, detail=f"not authorized token")
    return token_check
