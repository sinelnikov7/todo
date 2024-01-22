from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from application.services.service_shedule import ServiceShedule
from application.shemas.shema_shedule import SheduleSchemaGet
from application.shemas.shema_task import TaskGetForShedule
from application.support.support_functions import get_user_id
from application.support.decorators import is_authorizated_api

usecase_shedule = ServiceShedule()


@is_authorizated_api
async def create_chedule(shedule, session, access_token=None):
    """Создание расписания"""
    user_id = get_user_id(access_token)
    try:
        new_shedule = await usecase_shedule.create(shedule.date, user_id, session)
        response = SheduleSchemaGet(**new_shedule.__dict__)
        return {"status": "201", "data": response}
    except IntegrityError:
        return {"status": "У пользователя уже есть расписание на эту дату"}


@is_authorizated_api
async def shedule_get(get_date, session, access_token=None):
    """Получение расписания"""
    user_id = get_user_id(access_token)
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
