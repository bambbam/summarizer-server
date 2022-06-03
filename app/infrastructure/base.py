from abc import ABC, abstractmethod
import os

import boto3
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Repository(ABC):
    @abstractmethod
    def put(self, data, ttl=None):
        ...

    @abstractmethod
    def get(self, entity_key):
        ...


class COMMAND(BaseModel):
    ...


class EventProducer(ABC):
    @abstractmethod
    def put(self, message: COMMAND):
        ...


async def get_db():
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get('dynamodb_aws_access_key_id'), 
        aws_secret_access_key=os.environ.get('dynamodb_aws_secret_access_key'), 
        region_name=os.environ.get('dynamodb_region')
    )
    return dynamodb
