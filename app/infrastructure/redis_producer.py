import json
import os

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
            host=os.environ.get("redis_host"),
            port=os.environ.get("redis_port")
        )
        yield RedisProducer(redis=Redis, key=os.environ.get("redis_key"))
    finally:
        ...
