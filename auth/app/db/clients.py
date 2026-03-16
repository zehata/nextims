from app.exceptions.clients import ClientNotFound
from app.typing.client import Client
from app.utils.clients import validate_redis_client_response
from app.exceptions.redis import UnexpectedRedisResponse
import inspect
from app.utils.passwords import get_password_hash
from redis import Redis
from secrets import token_urlsafe


def create_client(redis_client: Redis, public_key_endpoint: str) -> Client:
    client_id = token_urlsafe(32)
    client_secret = token_urlsafe(32)
    hashed_client_id = get_password_hash(client_id)
    client = Client.model_construct(
        client_id=hashed_client_id,
        client_secret=get_password_hash(client_secret),
        public_key_endpoint=public_key_endpoint,
    )
    redis_client.hset("clients", hashed_client_id, mapping=dict(client))
    return client


def read_client(redis_client: Redis, client_id: str) -> Client | None:
    hashed_client_id = get_password_hash(client_id)
    user_response = redis_client.hget("clients", hashed_client_id)
    client = validate_redis_client_response(user_response)
    if client is None:
        return None
    if inspect.isawaitable(client):
        raise UnexpectedRedisResponse
    return client


def regenerate_client_secret(redis_client: Redis, client_id: str) -> str:
    hashed_client_id = get_password_hash(client_id)
    user_response = redis_client.hget("clients", hashed_client_id)
    client = validate_redis_client_response(user_response)
    if client is None:
        raise ClientNotFound
    if inspect.isawaitable(client):
        raise UnexpectedRedisResponse
    regenerated_secret = token_urlsafe(32)
    client.hashed_client_secret = get_password_hash(regenerated_secret)
    return regenerated_secret


def update_public_key_endpoint(redis_client: Redis, client_id: str, public_key_endpoint: str) -> None:
    hashed_client_id = get_password_hash(client_id)
    user_response = redis_client.hget("clients", hashed_client_id)
    client = validate_redis_client_response(user_response)
    if client is None:
        raise ClientNotFound
    if inspect.isawaitable(client):
        raise UnexpectedRedisResponse
    client.public_key_endpoint = public_key_endpoint
    redis_client.hset("clients", hashed_client_id, mapping=dict(client))


def delete_client(redis_client: Redis, client_id: str) -> Client | None:
    hashed_client_id = get_password_hash(client_id)
    user_response = redis_client.hget("clients", hashed_client_id)
    client = validate_redis_client_response(user_response)
    if client is None:
        return None
    if inspect.isawaitable(client):
        raise UnexpectedRedisResponse
    redis_client.hdel("clients", hashed_client_id)
    return client
