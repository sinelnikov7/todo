from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from application.models.model_user import User, Code


class ServiceUser:
    """Класс пользователя"""

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_admin(self, name: str, surname: str, email: str, password: str, date, session: AsyncSession,
                           number) -> int:
        """Создание нового пользователя суперадмина"""
        hash_password = self.pwd_context.hash(password)
        user = User(name=name, surname=surname, email=email, password=hash_password, activate=False, data_create=date,
                    is_admin=True, admin_id=None)
        key = Code(key=number)
        user.code = key
        session.add(user)
        await session.commit()
        await session.refresh(user)
        await session.close()
        return user.id

    async def get_user_code(self, user_id, session):
        """Получить код активации юзера"""
        query = select(Code.key).where(Code.user_id == user_id)
        result = await session.execute(query)
        result_key = result.fetchone()[0]
        return result_key

    async def activate_user(self, user_id, session):
        """Активировать пользователя"""
        query = update(User).where(User.id == user_id).values(activate=True)
        await session.execute(query)
        await session.commit()
        await session.close()
