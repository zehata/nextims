from pydantic import BaseModel


class User(BaseModel):
    hashed_username: str
    hashed_password: str
    user_id: str
    role: str
