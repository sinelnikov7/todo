from fastapi import APIRouter, Depends
from sqlalchemy import insert
from .schemas import Shedule_Schema
from .models import Shedule
from database import async_session, get_session
from sqlalchemy.ext.asyncio import AsyncSession

to_do_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"],
)


@to_do_router.post('/task', response_model=Shedule_Schema)
async def add_task(task: Shedule_Schema, session: AsyncSession = Depends(get_session)):
    shedule = Shedule(date=task.date)
    session.add(shedule)
    await session.commit()
    await session.refresh(shedule)
    response = Shedule_Schema(**shedule.__dict__)
    return response

