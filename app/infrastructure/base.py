import boto3
from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def put(self, data, ttl=None):
        ...

    @abstractmethod
    def get(self, entity_key):
        ...


async def get_db():
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    return dynamodb