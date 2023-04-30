from fastapi import APIRouter
from .schemas import Task, Shedule
from database import async_session, get_session
from sqlalchemy.ext.asyncio import AsyncSession

to_do_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"],
)

@to_do_router.post('/task', response_model=Task)
async def add_task(task: Task):
    return task