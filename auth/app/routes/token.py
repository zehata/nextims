from datetime import timedelta
from app.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from app.db.clients import read_client
import requests
from jwt import PyJWK
from redis import Redis
from app.db.authorizations import read_authorization
from fastapi import APIRouter
from app.typing.jwt_payload import JWTPayload
from app.typing.token import Token
from starlette.status import HTTP_401_UNAUTHORIZED
from app.utils.tokens import create_access_token
import jwt
from fastapi import Request
from fastapi import Response
from typing import Annotated
from app.typing.jwt_client_authentication_form import JWTClientAuthenticationForm
from fastapi import Depends


router = APIRouter(prefix="/oauth")


@router.post("/authorize")
async def authorize_client(
    form_data: Annotated[JWTClientAuthenticationForm, Depends()],
    response: Response,
    request: Request,
):
    client_signed_jwt = form_data.client_assertion

    payload = JWTPayload.model_validate(jwt.decode(client_signed_jwt, options={"verify_signature": False}))
    redis_client: Redis = request.state["redis_client"]
    client_id = payload.iss
    client = read_client(redis_client, client_id)
    if client is None:
        response.status_code = HTTP_401_UNAUTHORIZED
        return response
    client_public_key_endpoint = client.public_key_endpoint
    client_public_key_response = requests.get(client_public_key_endpoint)
    client_public_key: PyJWK = PyJWK.from_json(client_public_key_response.json())
    jwt.decode(client_signed_jwt, client_public_key)

    authorization_code = form_data.code

    authorization = read_authorization(
        redis_client=redis_client,
        authorization_code=authorization_code,
    )
    if authorization is None:
        response.status_code = HTTP_401_UNAUTHORIZED
        return response
    authorized_client_id = authorization.client_id
    if authorized_client_id != payload.iss:
        response.status_code = HTTP_401_UNAUTHORIZED
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        iss=str(request.url),
        aud=authorized_client_id,
        sub=authorization.user_id,
        client_id=authorized_client_id,
        expires_delta=expires_delta,
    )
    return Token(access_token=access_token, token_type="bearer", expires_in=expires_delta, scope="")
