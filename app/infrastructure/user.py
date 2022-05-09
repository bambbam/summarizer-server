from typing import Optional

import boto3
from pydantic import BaseModel

from app.infrastructure.base import Repository


class User(BaseModel):
    username: str
    password: str
    disabled: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table("User")

    def put(self, obj):
        try:
            self.table.put_item(Item=obj)
            return True
        except:
            return False

    def get(self, username):
        try:
            return self.table.get_item(Key={"username": username})["Item"]
        except:
            return None
