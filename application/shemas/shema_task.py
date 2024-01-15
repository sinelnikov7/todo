import datetime

from typing import Optional, Union,  Dict
from pydantic import BaseModel, Field, validator


class TaskPost(BaseModel):

    time: datetime.time = Field(..., title="Time", description="Time of day", example="08:00")
    title: str
    status: int
    priority: str
    color_priority: str
    date: datetime.date
    user_id: Union[int, None]

    @validator('status')
    def status_range(cls, value):
        if value < 0 or value > 2:
            raise ValueError('Статус может включать: 0 - Ожидание, 1 - Выполнено, 2 - Отменено')
        return value

    @validator('priority')
    def priority_range(cls, value:str):
        if len(value) < 0 or len(value) > 15:
            raise ValueError('Приоритет должен содержать 0т 1 до 15 символов')
        return value


class TaskGet(BaseModel):

    success: Optional[bool] = None
    id: int
    time: datetime.time = Field(..., title="Time", description="Time of day", example="08:00")
    title: str
    status: int
    priority: str
    color_priority: str
    date: datetime.date

class TaskGetOne(BaseModel):

    success: Optional[bool] = None
    id: int
    time: datetime.time = Field(..., title="Time", description="Time of day", example="08:00")
    title: str
    status: int
    priority: str
    color_priority: str


class TaskGetForShedule(BaseModel):

    id: int
    time: datetime.time = Field(..., title="Time", description="Time of day", example="08:00")
    title: str
    status: int
    priority: str
    color_priority: str



class TaskEdit(BaseModel):

    time: datetime.time = Field(..., title="Time", description="Time of day", example="08:00")
    title: str
    status: int
    priority: str
    color_priority: str

    @validator('status')
    def status_range(cls, value):
        if value < 0 or value > 2:
            raise ValueError('Статус может включать: 0 - Ожидание, 1 - Выполнено, 2 - Отменено')
        return value

    @validator('priority')
    def priority_range(cls, value:str):
        if len(value) < 0 or len(value) > 15:
            raise ValueError('Приоритет должен содержать 0т 1 до 15 символов')
        return value


class TaskDelete(BaseModel):
    staus: Dict = {"status": 200}