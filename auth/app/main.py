from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2AuthorizationCodeBearer
from app.utils.db import get_redis_client
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state["redis_client"] = get_redis_client()
    yield


app = FastAPI()

oauth_authorization_code_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="/authorize",
    tokenUrl="/token",
    refreshUrl="/refresh",
    scopes={},
)


async def get_current_user():
    pass
