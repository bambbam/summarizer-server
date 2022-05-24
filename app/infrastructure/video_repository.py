from typing import List, Optional

import boto3
from fastapi import Depends
from pydantic import BaseModel

from app.infrastructure.base import Repository
from app.infrastructure.now import get_now
from app.infrastructure.uuid import get_uuid
from app.interface.router.auth import get_current_user


class VideoData(BaseModel):
    key: str
    user_name: str
    status: str
    start_time: str
    end_time: Optional[str]



class VideoRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table("Video")

    def get_all(self) -> List[VideoData]:
        return self.table.scan()

    def get(self, key) -> Optional[VideoData]:
        try:
            item = VideoData(**(self.table.get_item(Key={"key": key}))["Item"])
        except:
            item = None
        finally:
            return item

    def put(self, user_name, current_time, key, status="uploaded"):
        try:
            item = VideoData(
                key=key,
                user_name=user_name,
                status=status,
                start_time=current_time,
                end_time=None,
            )
            self.table.put_item(Item=item.dict())
            return True
        except:
            return False
        

    def delete(self, key, username):
        try:
            self.table.delete_item(
                Key={"key": key},
                ConditionExpression="user_name = :val",
                ExpressionAttributeValues={":val": username["user"]},
            )
            return True
        except:
            return False
