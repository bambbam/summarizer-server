from abc import ABC, abstractmethod

import boto3


class Repository(ABC):
    @abstractmethod
    def put(self, data, ttl=None):
        ...

    @abstractmethod
    def get(self, entity_key):
        ...


async def get_db():
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    return dynamodb
