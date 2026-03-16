from typing import Literal
from pydantic import BaseModel


class JWTClientAuthenticationForm(BaseModel):
    grant_type: Literal["authorization_code"]
    code: str
    client_assertion_type: Literal["urn:ietf:params:oauth:client-assertion-type:jwt-bearer"]
    client_assertion: str
