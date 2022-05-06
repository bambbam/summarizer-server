import boto3
from pydantic import BaseModel
from typing import Optional


from app.infrastructure.base import Repository
from app.infrastructure.now import get_now

class VideoData(BaseModel):
    key: str
    url: str
    status: str
    start_time: str
    end_time: Optional[str]

class VideoRepository(Repository):
    def __init__(self, dynamodb, algorithm):
        self.table = dynamodb.Table('Video')

    def get_all(self):
        return self.table.query()
    
    def get(self, key):
        item = VideoData(**(self.table.get_item(Key={"key":key})['Item']))
        return item
