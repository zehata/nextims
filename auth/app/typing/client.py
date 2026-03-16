from pydantic import BaseModel


class Client(BaseModel):
    hashed_client_id: str
    hashed_client_secret: str
    public_key_endpoint: str
