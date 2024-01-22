from typing import Union, Annotated
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from application.shemas.shema_task import TaskPost, TaskGet, TaskGetOne, TaskEdit, TaskDelete
from application.usecases.usecase_task import create_tak, task_get, task_edit, task_dellete
from infrastructure.database.database import get_session


task_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"],
)


@task_router.post('/task', status_code=201)
async def add_task(task: TaskPost, access_token: Annotated[str | None, Header()] = None,
                   session: AsyncSession = Depends(get_session)) -> Union[TaskGet, dict]:
    """Создание задачи"""
    return await create_tak(task, session,  access_token=access_token)


@task_router.get('/task/{id}')
async def get_task(id: int = id,  access_token: Annotated[str | None, Header()] = None,
                   session: AsyncSession = Depends(get_session)) -> Union[TaskGetOne, dict]:
    """Получение задачи"""
    return await task_get(id, session, access_token=access_token)


@task_router.patch('/task/{id}', status_code=200)
async def edit_task(task: TaskEdit, id:int = id,  access_token: Annotated[str | None, Header()] = None,
                    session: AsyncSession = Depends(get_session))  -> Union[TaskGet, dict]:
    """Обновление задачи"""
    return await task_edit(task, id, session, access_token=access_token)


@task_router.delete('/task/{id}', status_code=200)
async def dellete_task(id:int = id,  access_token: Annotated[str | None, Header()] = None,
                       session: AsyncSession = Depends(get_session))  -> Union[TaskDelete, dict]:
    """Удаление задачи"""
    return await task_dellete(id, session,  access_token=access_token)