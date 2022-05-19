import boto3
from dependency_injector import containers, providers
from redis import Redis

from app.infrastructure.redis_producer import RedisProducer
from app.infrastructure.user_repository import UserRepository
from app.infrastructure.video_repository import VideoRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis = providers.Singleton(Redis, host=config.redis_host, port=config.redis_port)
    event_producer = providers.Factory(RedisProducer, redis=redis, key=config.redis_key)

    dynamodb = providers.Singleton(
        boto3.resource, "dynamodb", endpoint_url=config.dynamodb_url
    )
    # feature_repository = providers.Singleton(FeatureRepository, dynamodb)
    video_repository = providers.Singleton(VideoRepository, dynamodb)
    user_repository = providers.Singleton(UserRepository, dynamodb)
