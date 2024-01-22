from sqlalchemy.exc import IntegrityError

from application.services.service_task import ServiceTask
from application.shemas.shema_task import TaskGetOne
from application.usecases.usecase_shedule import usecase_shedule
from application.support.decorators import is_authorizated_api
from application.support.support_functions import get_user_id


use_task = ServiceTask()

@is_authorizated_api
async def create_tak(task, session,  access_token=None):
    """Создание задачи"""
    user_id = get_user_id(access_token)
    if task.user_id != None:
        user_id = task.user_id
    exist_shedule = await usecase_shedule.get_shedule_with_task(task.date, user_id, session)
    # Создание задачи(Task) если у юзера есть расписание(Shedule) на эту дату
    try:
        shedule_id = exist_shedule[0].id
        new_task = await use_task.create_with_shedule(task.time, task.title, task.status, task.priority,
                        task.color_priority, shedule_id, session)
        response = dict(success=True, id=new_task.id, time=task.time, title=task.title, status=task.status, priority=task.priority,
                        color_priority=task.color_priority, date=task.date)
        return response
    # Создание задачи(Task) если у юзера нету расписание(Shedule) на эту дату, парралельно создаются и расписание(Shedule) и задача(Task)
    except (IndexError, TypeError):
        new_task = await use_task.create_without_shedule(task.date, user_id,task.time, task.title, task.status, task.priority,
                        task.color_priority, session)
        response = dict(success=True, id=new_task.id, time=task.time, title=task.title, status=task.status,
                        priority=task.priority,
                        color_priority=task.color_priority, date=task.date)
        return response

@is_authorizated_api
async def task_get(id, session, access_token=None):
    """Получение задачи"""
    user_id = get_user_id(access_token)
    try:
        task = await use_task.get(id, session)
        if task.shedule.user_id == user_id:
            response = TaskGetOne(**task.__dict__)
            response.success =True
        else:
            return {"status": "У вас нету доступа к этой задаче"}
    except (IntegrityError, IndexError, TypeError):
        return {"status": f"Не удалось найти задачу с id={id}"}
    return response

@is_authorizated_api
async def task_edit(task, id, session,  access_token=None):
    """Обновление задачи"""
    await use_task.edit(task, id, session)
    return {"status": 200}

@is_authorizated_api
async def task_dellete(id, session, access_token=None):
    """Удаление задачи"""
    await use_task.dellete(id, session)
    return {"status": 200}