from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from application.models.model_shedule import Shedule
from application.models.model_task import Task


class ServiceTask:

    async def create_with_shedule(self, time, title, status, priority,
                     color_priority, shedule_id, session):
        """Создание расписания и задачи"""
        new_task = Task(time=time, title=title, status=status, priority=priority,
                        color_priority=color_priority, shedule_id=shedule_id)
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return new_task

    async def create_without_shedule(self, date, user_id, time, title, status, priority,
                     color_priority, session):
        """Создание задачи на уже созданное расписание"""
        shedule = Shedule(date=date, user_id=user_id)
        new_task = Task(time=time, title=title, status=status, priority=priority,
                        color_priority=color_priority)
        shedule.task.append(new_task)
        session.add(shedule)
        await session.commit()
        await session.refresh(shedule)
        await session.close()
        return new_task

    async def get(self, id, session):
        """Получение задачи"""
        query = select(Task).options(selectinload(Task.shedule)).where(Task.id == id)
        task = await session.execute(query)
        task = task.fetchone()[0]
        return task

    async def edit(self, task, id, session):
        """Редактирование задачи"""
        query = update(Task).where(Task.id == id).values(**task.dict())
        response = await session.execute(query)
        await session.commit()
        await session.close()
        return response

    async def dellete(self, id, session):
        """Удаление задачи"""
        query = delete(Task).where(Task.id == id)
        response = await session.execute(query)
        await session.commit()
        await session.close()
        return response