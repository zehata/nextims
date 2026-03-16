from app.constants import ALGORITHM
from app.constants import SECRET_KEY
from uuid import uuid4
from app.typing.jwt_payload import JWTPayload
from datetime import datetime, timedelta, UTC
import jwt


def create_access_token(
    iss: str,
    sub: str,
    aud: str,
    expires_delta: timedelta = timedelta(minutes=15),
):
    issued_at = datetime.now(UTC)
    expires_at = issued_at + expires_delta
    to_encode = JWTPayload.model_construct(
        iss=iss,
        sub=sub,
        aud=aud,
        jti=uuid4(),
        iat=issued_at,
        exp=expires_at,
    )
    encoded_jwt = jwt.encode(dict(to_encode), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
