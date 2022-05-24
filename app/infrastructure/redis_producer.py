import json

import redis

from app.infrastructure.base import COMMAND, EventProducer


class RedisProducer(EventProducer):
    def __init__(self, redis, key):
        self.redis = redis
        self.key = key

    def put(self, data: COMMAND):
        self.redis.lpush(self.key, json.dumps(data.dict()))


async def get_queue():

    try:
        Redis = redis.Redis(
            host="127.0.0.1",
            port="6379"
        )
        yield RedisProducer(redis=Redis, key="summarizer")
    finally:
        ...
