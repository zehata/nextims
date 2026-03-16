from app.typing.authorization import Authorization
from app.exceptions.redis import UnexpectedRedisResponse
import inspect
from app.typing.redis import RedisResponse


def validate_redis_authorization_response(redis_response: RedisResponse):
    if inspect.isawaitable(redis_response):
        raise UnexpectedRedisResponse
    if redis_response is None:
        return None
    return Authorization.model_validate_json(redis_response)
