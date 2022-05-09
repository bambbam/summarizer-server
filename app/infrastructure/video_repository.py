from typing import List, Optional

import boto3
from pydantic import BaseModel

from app.infrastructure.base import Repository
from app.infrastructure.now import get_now


class VideoData(BaseModel):
    key: str
    url: str
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
            item = VideoData(**(self.table.get_item(Key={"key": key})["Item"]))
        except:
            item = None
        return item

    def put(self):
        ...
