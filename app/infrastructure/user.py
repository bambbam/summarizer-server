from typing import Optional
from pydantic import BaseModel

from app.infrastructure.base import Repository
import boto3


class User(BaseModel):
    username:str
    password: str
    disabled: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class UserRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table('User')

    def create(self, obj:User):
        try:
            self.table.put_item(
                Item = obj
            )
            return True
        except:
            return False

    def put(self):
        ...

    def get(self, username) -> Optional["User"]:
        try:
            return self.table.get_item(
                Key={"username":username}
            )['Item']
        except:
            return None
# TODO dynamdb dependency injection 필요
async def get_user_repo():
    repo = UserRepository(
        dynamodb=boto3.resource('dynamodb', endpoint_url="http://localhost:8000"),
    )
    try:
        yield repo
    finally:
        ...