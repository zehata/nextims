from app.exceptions.redis import MissingRedisConnectionInfo
from app.constants import REDIS_PORT
from app.constants import REDIS_HOST
from redis import Redis


def get_redis_client():
    host = REDIS_HOST
    port = REDIS_PORT

    if host is None or port is None or not port.isnumeric:
        raise MissingRedisConnectionInfo

    port_number = int(port)

    return Redis(
        host=host,
        port=port_number,
        decode_responses=True,
    )
