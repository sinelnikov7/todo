from typing import Optional
from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: Optional[int] = Field()
    name: str
    surname: str
    email: str
    password: str

class UserProfile(BaseModel):
    email: str
    name: str
    surname: str
    admin: bool


class LoginShema(BaseModel):
    email: str
    password: str

