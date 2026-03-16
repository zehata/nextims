from app.typing.user import User
from app.exceptions.redis import UnexpectedRedisResponse
import inspect
from app.utils.passwords import verify_password
from app.db.users import read_user
from redis import Redis
from app.typing.redis import RedisResponse


def validate_redis_user_response(redis_response: RedisResponse):
    if inspect.isawaitable(redis_response):
        raise UnexpectedRedisResponse
    if redis_response is None:
        return None
    return User.model_validate_json(redis_response)


def authenticate_user(user: User | None, password: str):
    if not user:
        verify_password(password, "DUMMY_PASSWORD_TO_PREVENT_TIMING_ATTACKS")
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return True
