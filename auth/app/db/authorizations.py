from secrets import token_urlsafe
from app.typing.authorization import Authorization
from app.utils.authorizations import validate_redis_authorization_response
from app.utils.passwords import get_password_hash
from redis import Redis

DEFAULT_USER_client_id = ""


def create_authorization(redis_client: Redis, user_id: str, client_id: str) -> str:
    authorization_code = token_urlsafe(32)
    hashed_authorization_code = get_password_hash(authorization_code)
    authorization = Authorization.model_construct(
        authorization_code=hashed_authorization_code,
        user_id=user_id,
        client_id=client_id,
    )

    redis_client.hset("authorizations", hashed_authorization_code, mapping=dict(authorization))
    return authorization_code


def read_authorization(redis_client: Redis, authorization_code: str) -> Authorization | None:
    hashed_authorization_code = get_password_hash(authorization_code)
    authorization_response = redis_client.hget("authorizations", hashed_authorization_code)
    authorization = validate_redis_authorization_response(authorization_response)
    return authorization


def delete_authorization(redis_client: Redis, authorization_code: str):
    hashed_authorization_code = get_password_hash(authorization_code)
    authorization_response = redis_client.hget("authorizations", hashed_authorization_code)
    redis_client.hgetdel("authorizations", hashed_authorization_code)
    return validate_redis_authorization_response(authorization_response)
