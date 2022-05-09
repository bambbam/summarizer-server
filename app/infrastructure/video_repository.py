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


def encode_video_key(user_name):
    return f'{user_name}'

class VideoRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table("Video")

    def get_all(self) -> List[VideoData]:
        return self.table.scan()

    def get(self, key) -> Optional[VideoData]:
        try:
            item=VideoData(**(self.table.get_item(Key={"key": key}))['Item'])
        except:
            item=None
        finally:
            return item
        

    def put(self, user_name, video_url, current_time, status="uploaded"):
        try:
            item = VideoData(
                key=encode_video_key(user_name),
                url=video_url,
                status=status,
                start_time=current_time,
                end_time=None    
            )
            self.table.put_item(Item=item.dict())
            return True
        except:
            return False
    
    def delete(self, key):
    
        res = self.table.delete_item(
            Key={
                'key': key
            }
        )
        return res