from fastapi.security import OAuth2PasswordRequestFormStrict
from app.utils.clients import authenticate_client
from app.db.users import read_user
from app.db.clients import read_client
from fastapi import Response
from fastapi import APIRouter
from app.utils.tokens import create_access_token
from fastapi import HTTPException
from app.typing.token import Token
from fastapi import Depends
from typing import Annotated
from fastapi import Request
from app.utils.users import authenticate_user
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import timedelta
from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/oauth")


@router.post("/login")
async def user_password_login(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    request: Request,
    response: Response,
) -> Token | Response:
    redis_client = request.state["redis_client"]

    username = form_data.username
    user = read_user(redis_client=redis_client, username=username)
    user_authenticated = authenticate_user(user, form_data.password)

    client_id = form_data.client_id
    client = read_client(redis_client=redis_client, client_id=client_id)
    client_authenticated = authenticate_client(client, form_data.client_secret)

    if not (user and user_authenticated and client_id and client and client_authenticated):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        iss=str(request.url),
        aud="",
        sub=user.user_id,
        client_id=client_id,
        expires_delta=access_token_expires,
    )
    request.session["access_token"] = access_token
    return Token(access_token=access_token, token_type="bearer")
