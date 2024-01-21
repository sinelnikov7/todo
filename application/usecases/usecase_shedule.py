import jwt
from fastapi import HTTPException
from jwt import DecodeError
from sqlalchemy.exc import IntegrityError

from application.services.service_shedule import ServiceShedule
from application.shemas.shema_shedule import SheduleSchemaGet
from application.shemas.shema_task import TaskGetForShedule
from config import SECRET


usecase_shedule = ServiceShedule()


async def create_chedule(shedule, access_token, session):
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    try:
        new_shedule = await usecase_shedule.create(shedule.date, user_id, session)
        response = SheduleSchemaGet(**new_shedule.__dict__)
        return {"status": "201", "data": response}
    except IntegrityError:
        return {"status": "У пользователя уже есть расписание на эту дату"}


async def shedule_get(get_date, access_token, session):
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    try:
        get_shedule = await usecase_shedule.get(get_date, user_id, session)
    except TypeError:
        raise HTTPException(status_code=404, detail='Расписания  не существует, или оно не принадлежит данному юзеру')
    response_tasks = []
    tasks = get_shedule.task
    sortered_tasks = sorted(tasks, key=lambda x: x.__dict__['time'])
    for task in sortered_tasks:
        response_tasks.append(TaskGetForShedule(**task.__dict__))
    response = {"success": True, "id": get_shedule.id, "date": get_shedule.date, "tasks": response_tasks}
    return response