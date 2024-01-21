from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from application.models.model_shedule import Shedule


class ServiceShedule:

    async def create(self, date, user_id, session):
        new_shedule = Shedule(date=date, user_id=user_id)
        session.add(new_shedule)
        await session.commit()
        await session.refresh(new_shedule)
        return new_shedule

    async def get(self, get_date, user_id, session):
        query = select(Shedule).options(selectinload(Shedule.task)).where(
            and_(Shedule.date == get_date, Shedule.user_id == user_id))
        shedule = await session.execute(query)
        shedule = shedule.fetchone()[0]
        return shedule

    async def get_shedule_with_task(self, date, user_id, session):
        query = select(Shedule).where(and_(Shedule.date == date, Shedule.user_id == user_id))
        exist_shedule = await session.execute(query)
        exist_shedule = exist_shedule.fetchone()
        return exist_shedule