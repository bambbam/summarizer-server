from typing import Dict, List

from fastapi import Depends
from pydantic import BaseModel

from app.infrastructure.base import Repository


class FrameFeature(BaseModel):
    current_frame: int
    name: str
    box_points: List[int]


class VideoFeature(BaseModel):
    key: str
    features: List[FrameFeature]
    representing_features: Dict[str,FrameFeature] = {}

def encode_video_key(user_name):
    return f"{user_name}"


class FeatureRepository(Repository):
    def __init__(self, dynamodb):
        self.table = dynamodb.Table("Feature")

    def get_all(self) -> List[VideoFeature]:
        video_feature: VideoFeature = self.table.scan()
        return video_feature
    
    def get(self, key) -> VideoFeature:
        try:
            return VideoFeature(**(self.table.get_item(Key={"key": key})["Item"]))
        except:
            return None
    
    def put(self):
        ...

