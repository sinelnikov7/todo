from typing import Optional
from pydantic import BaseModel, Field


class User_schema(BaseModel):
    id: Optional[int] = Field()
    email: str
    password: str
    name: str
    surname: str


class Login_shema(BaseModel):
    email: str
    password: str

