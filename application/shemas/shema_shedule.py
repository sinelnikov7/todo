import datetime

from typing import Optional, List
from pydantic import BaseModel

from application.shemas.shema_task import TaskGetForShedule


class SheduleSchemaGet(BaseModel):

    id: Optional[int] = None
    date: datetime.date
    user_id: int


class SheduleResponse(BaseModel):

    status: str
    data: SheduleSchemaGet


class SheduleSchemaPost(BaseModel):

    date: datetime.date

class SheduleResponseWithTasks(BaseModel):
    success: bool
    id: int
    date: datetime.date
    tasks: List[TaskGetForShedule]
