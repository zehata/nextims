from pydantic import HttpUrl
from pydantic import BaseModel


class JWTPayload(BaseModel):
    iss: str
    sub: str
    aud: HttpUrl
    jti: str
    iat: str
    exp: str
