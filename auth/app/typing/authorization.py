from datetime import timedelta
from pydantic import BaseModel


class Authorization(BaseModel):
    authorization_code: str
    user_id: str
    client_id: str
    requested_expiry_delta: timedelta
