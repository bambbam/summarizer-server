import json
import os

import redis
import pika
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

class RabbitProducer(EventProducer):
    def __init__(self, rabbit, key):
        self.rabbit = rabbit.channel()
        self.rabbit.queue_declare(queue=key)
        self.key = key

    def put(self, data:COMMAND):
        self.rabbit.basic_publish(exchange='',
                                  routing_key=self.key,
                                  body=json.dumps(data.dict()))
        
        
async def get_rabbit_queue():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        yield RabbitProducer(rabbit=connection, key=os.environ.get("redis_key"))
        
    finally:
        ...