from datetime import datetime
from typing import Optional, Union, List

from pydantic import BaseModel, Field, EmailStr


class Task(BaseModel):
    id: Optional[int] = Field()
    description: str


class Status(BaseModel):
    id: Optional[int] = Field()
    title: str


class Priority(BaseModel):
    id: Optional[int] = Field()
    title: str


class Shedule(BaseModel):
    id: Optional[int] = Field()
    user_id: int
    description: str
    tasks: List[Task]
    date: datetime = datetime.now().date()
    status: Status
    priority: Priority
    # send_mail: EmailStr = None
    send_tg: str = None



