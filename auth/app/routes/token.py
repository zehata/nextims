# receive username and password from user
from fastapi import APIRouter
from app.utils.tokens import create_access_token
from fastapi import HTTPException
from app.typing.token import Token
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Request
from app.utils.users import authenticate_user
from app.main import password_hash
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import timedelta
from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/oauth")


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
) -> Token:
    redis_client = request.state["redis_client"]
    hashed_username = password_hash.hash(form_data.username)
    user_authenticated = authenticate_user(redis_client, hashed_username, form_data.password)
    if not user_authenticated:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        iss=str(request.url),
        sub=hashed_username,
        aud="",
        expires_delta=access_token_expires,
    )
    request.session["access_token"] = access_token
    return Token(access_token=access_token, token_type="bearer")
