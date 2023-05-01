from datetime import date
from typing import Optional, Union, List

from pydantic import BaseModel, Field, EmailStr


class Shedule_Schema(BaseModel):
    id: Optional[int] = Field()
    date: date


class Status(BaseModel):
    id: Optional[int] = Field()
    title: str


class Priority(BaseModel):
    id: Optional[int] = Field()
    title: str


# class Shedule(BaseModel):
#     id: Optional[int] = Field()
#     user_id: int
#     description: str
#     tasks: List[Task_Schema]
#     date: datetime = datetime.now().date()
#     status: Status
#     priority: Priority
#     # send_mail: EmailStr = None
#     send_tg: str = None



