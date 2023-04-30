from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel, Field, EmailStr


class User_schema(BaseModel):
    id: Optional[int] = Field()
    email: str
    password: str
    name: str
    surname: str


class Login_shema(BaseModel):
    email: str
    password: str

