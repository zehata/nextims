from typing import Awaitable

type RedisResponse = Awaitable[str | None] | str | None
