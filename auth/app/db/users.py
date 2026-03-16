from app.exceptions.users import UsernameCollision
from uuid import UUID
from uuid import uuid4
from app.utils.users import validate_redis_user_response
from app.exceptions.redis import UnexpectedRedisResponse
from app.utils.passwords import get_password_hash
from app.typing.user import User
import inspect
from redis import Redis
from app.exceptions.users import UserNotFound

DEFAULT_USER_ROLE = ""


def create_user(redis_client: Redis, username: str, password: str, role: str = DEFAULT_USER_ROLE) -> UUID:
    hashed_username = get_password_hash(username)
    colliding_user = redis_client.hget("users", hashed_username)
    if colliding_user is not None:
        raise UsernameCollision
    user_id = uuid4()
    user = User.model_construct(
        hashed_username=hashed_username,
        hashed_password=get_password_hash(password),
        user_id=user_id,
        role=str,
    )
    redis_client.hset("users", username, mapping=dict(user))
    return user_id


def read_user(redis_client: Redis, username: str) -> User | None:
    hashed_username = get_password_hash(username)
    user_response = redis_client.hget("users", hashed_username)
    user = validate_redis_user_response(user_response)
    if user is None:
        return None
    if inspect.isawaitable(user):
        raise UnexpectedRedisResponse
    return user


def update_user_username(
    redis_client: Redis,
    current_username: str,
    new_username: str,
) -> None:
    hashed_current_username = get_password_hash(current_username)
    current_user_response = redis_client.hget("users", hashed_current_username)
    current_user = validate_redis_user_response(current_user_response)
    if current_user is None:
        raise UserNotFound

    hashed_new_username = get_password_hash(new_username)
    colliding_user = redis_client.hget("users", hashed_new_username)
    if colliding_user is not None:
        raise UsernameCollision

    new_user = current_user.model_copy(deep=True)
    new_user.hashed_username = hashed_new_username
    redis_client.hdel("users", hashed_current_username)
    redis_client.hset("users", hashed_new_username, mapping=dict(new_user))


def update_user_password_or_role(
    redis_client: Redis,
    username: str,
    password: str | None,
    role: str | None,
) -> None:
    hashed_username = get_password_hash(username)
    current_user_response = redis_client.hget("users", hashed_username)
    current_user = validate_redis_user_response(current_user_response)
    if current_user is None:
        raise UserNotFound

    new_user = current_user.model_copy(deep=True)
    if password is not None:
        new_user.hashed_password = get_password_hash(password)
    if role is not None:
        new_user.role = role
    redis_client.hset("users", username, mapping=dict(new_user))


def delete_user(redis_client: Redis, username: str, password: str) -> User | None:
    user_response = redis_client.hget("users", username)
    if user_response is None:
        return None
    redis_client.hdel("users", username)
    return validate_redis_user_response(user_response)
