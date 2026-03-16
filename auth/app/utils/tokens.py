from app.constants import ALGORITHM
from app.constants import SECRET_KEY
from uuid import uuid4
from app.typing.jwt_payload import JWTPayload
from datetime import datetime, timedelta, UTC
import jwt


def create_access_token(
    iss: str,
    aud: str,
    sub: str,
    client_id: str,
    expires_delta: timedelta = timedelta(minutes=15),
):
    issued_at = datetime.now(UTC)
    expires_at = issued_at + expires_delta
    to_encode = JWTPayload.model_construct(
        iss=iss,
        exp=expires_at,
        aud=aud,
        sub=sub,
        client_id=client_id,
        iat=issued_at,
        jti=uuid4(),
    )
    encoded_jwt = jwt.encode(dict(to_encode), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
