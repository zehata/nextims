from app.utils.passwords import verify_password
from app.db.clients import read_client
from app.typing.client import Client
from app.exceptions.redis import UnexpectedRedisResponse
import inspect
from app.typing.redis import RedisResponse
from redis import Redis


def validate_redis_client_response(redis_response: RedisResponse):
    if inspect.isawaitable(redis_response):
        raise UnexpectedRedisResponse
    if redis_response is None:
        return None
    return Client.model_validate_json(redis_response)


def authenticate_client(client: Client | None, password: str | None):
    if not (client and password):
        verify_password(password, "DUMMY_PASSWORD_TO_PREVENT_TIMING_ATTACKS")
        return False
    if not verify_password(password, client.hashed_client_secret):
        return False
    return True
