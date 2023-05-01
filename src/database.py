from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, MetaData
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
# from auth.models import User
from sqlalchemy.ext.declarative import declarative_base


metadata = MetaData()
Base = declarative_base(metadata=metadata)


DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session




# # Синхронно
# from sqlalchemy import create_engine, insert
# from sqlalchemy.orm import sessionmaker
#
# from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
# from auth.models import User, Code
#
# DATABASE_URLS = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
#
# engines = create_engine(DATABASE_URLS, echo=True)
# asyn_session = sessionmaker(bind=engines)
#
# #
# session = asyn_session()
#
# # query = insert(User).values(name="name", surname="surname", email="email", password="password", activate=True)
# query = User(name="name", surname="surname", email="emafil", password="password", activate=True)
# qqq = Code(key=1234)