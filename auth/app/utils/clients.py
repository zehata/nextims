from app.typing.client import Client
from app.exceptions.redis import UnexpectedRedisResponse
import inspect
from app.typing.redis import RedisResponse


def validate_redis_client_response(redis_response: RedisResponse):
    if inspect.isawaitable(redis_response):
        raise UnexpectedRedisResponse
    if redis_response is None:
        return None
    return Client.model_validate_json(redis_response)
