from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_key: str

    dynamodb_url: str
    dynamodb_aws_access_key_id: str
    dynamodb_aws_secret_access_key: str
    class Config:
        env_file = ".env"
