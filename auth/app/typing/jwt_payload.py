from pydantic import HttpUrl
from pydantic import BaseModel


class JWTPayload(BaseModel):
    iss: str
    exp: str
    aud: HttpUrl
    sub: str
    client_id: str
    iat: str
    jti: str
