from fastapi import APIRouter
from .schemas import Task_Schema, Shedule
from .models import Task
from database import async_session, get_session
from sqlalchemy.ext.asyncio import AsyncSession

to_do_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"],
)

@to_do_router.post('/task', response_model=Task_Schema)
async def add_task(task: Task_Schema):
    return task