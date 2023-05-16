import asyncio
import os
import time
from typing import Union, Annotated, Dict
from fastapi import APIRouter, Depends, Request, Response, Header, HTTPException
from jwt import DecodeError
from sqlalchemy import insert, select, and_, update, delete
import jwt
import dotenv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from .schemas import SheduleSchemaGet, SheduleSchemaPost, TaskGet, SheduleResponse, TaskPost, SheduleResponseWithTasks, \
    TaskGetForShedule, TaskGetOne, TaskEdit, TaskDelete
from .models import Shedule, Task
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

to_do_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"],
)

dotenv.load_dotenv()
SECRET = os.environ.get('SECRET')

@to_do_router.post('/task', status_code=201)
async def add_task(task: TaskPost, access_token: Annotated[str | None, Header()] = None,  session: AsyncSession = Depends(get_session)) -> Union[TaskGet, dict]:
    # Проверка токена
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    query = select(Shedule).where(and_(Shedule.date == task.date, Shedule.user_id == user_id))
    exist_shedule = await session.execute(query)
    exist_shedule = exist_shedule.fetchone()
    # Создание задачи(Task) если у юзера есть расписание(Shedule) на эту дату
    try:
        shedule_id = exist_shedule[0].id
        new_task = Task(time=task.time, title=task.title, status=task.status, priority=task.priority,
                        color_priority=task.color_priority, shedule_id=shedule_id)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        response = dict(success=True, id=new_task.id, time=task.time, title=task.title, status=task.status, priority=task.priority,
                        color_priority=task.color_priority, date=task.date)
        return response
    # Создание задачи(Task) если у юзера нету расписание(Shedule) на эту дату, парралельно создаются и расписание(Shedule) и задача(Task)
    except (IndexError, TypeError):
        shedule = Shedule(date=task.date, user_id=user_id)
        new_task = Task(time=task.time, title=task.title, status=task.status, priority=task.priority,
                        color_priority=task.color_priority)
        print(dir(shedule))
        shedule.task.append(new_task)
        session.add(shedule)
        await session.commit()
        await session.refresh(shedule)
        await session.close()
        response = dict(success=True, id=new_task.id, time=task.time, title=task.title, status=task.status,
                        priority=task.priority,
                        color_priority=task.color_priority, date=task.date)
        return response

@to_do_router.get('/shedule/', status_code=200)
async def get_shedule(get_date: date, access_token: Annotated[str | None, Header()] = None, session: AsyncSession = Depends(get_session)) -> Union[SheduleResponseWithTasks, dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    try:
        query = select(Shedule).options(selectinload(Shedule.task)).where(and_(Shedule.date == get_date, Shedule.user_id == user_id))
        shedule = await session.execute(query)
        shedule = shedule.fetchone()[0]
    except TypeError:
        raise HTTPException(status_code=404, detail='Расписания  не существует, или оно не принадлежит данному юзеру')
    response_tasks = []
    tasks = shedule.task
    sortered_tasks = sorted(tasks, key=lambda x: x.__dict__['time'])
    for task in sortered_tasks:
        response_tasks.append(TaskGetForShedule(**task.__dict__))
    response = {"success": True, "id": shedule.id, "date": shedule.date, "tasks": response_tasks}
    return response


@to_do_router.post('/shedule', status_code=201)
async def add_shedule(shedule: SheduleSchemaPost, access_token: Annotated[str | None, Header()] = None, session:AsyncSession = Depends(get_session)) -> Union[SheduleResponse, dict]:

    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
        new_shedule = Shedule(date=shedule.date, user_id=user_id)
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    try:
        session.add(new_shedule)
        await session.commit()
        await session.refresh(new_shedule)
        response = SheduleSchemaGet(**new_shedule.__dict__)
        return {"status": "201", "data": response}
    except IntegrityError:
        return {"status": "У пользователя уже есть расписание на эту дату"}


@to_do_router.get('/task/{id}')
async def get_task(id:int = id,  access_token: Annotated[str | None, Header()] = None, session: AsyncSession = Depends(get_session)) -> Union[TaskGetOne, dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    try:
        query = select(Task).options(selectinload(Task.shedule)).where(Task.id == id)
        task = await session.execute(query)
        task = task.fetchone()[0]
        if task.shedule.user_id == user_id:
            response = TaskGetOne(**task.__dict__)
            response.success =True
        else:
            return {"status": "У вас нету доступа к этой задаче"}
    except (IntegrityError, IndexError, TypeError):
        return {"status": f"Не удалось найти задачу с id={id}"}
    return response

@to_do_router.patch('/task/{id}', status_code=200)
async def edit_task(task: TaskEdit, id:int = id,  access_token: Annotated[str | None, Header()] = None,  session: AsyncSession = Depends(get_session))  -> Union[TaskGet, dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    query = update(Task).where(Task.id == id).values(**task.dict())
    response = await session.execute(query)
    await session.commit()
    return {"status": 200}

@to_do_router.delete('/task/{id}', status_code=200)
async def edit_task(id:int = id,  access_token: Annotated[str | None, Header()] = None,  session: AsyncSession = Depends(get_session))  -> Union[TaskDelete, dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    query = delete(Task).where(Task.id == id)
    response = await session.execute(query)
    await session.commit()
    return {"status": 200}