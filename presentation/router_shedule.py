import os
from datetime import date

import jwt
import dotenv
from jwt import DecodeError
from typing import Union, Annotated
from fastapi import APIRouter, Depends, Header, HTTPException



from sqlalchemy.ext.asyncio import AsyncSession

from application.shemas.shema_shedule import SheduleSchemaPost, SheduleResponse, SheduleResponseWithTasks
from application.usecases.usecase_shedule import create_chedule, shedule_get
from infrastructure.database.database import get_session

shedule_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"],
)


@shedule_router.post('/shedule', status_code=201)
async def add_shedule(shedule: SheduleSchemaPost, access_token: Annotated[str | None, Header()] = None,
                      session:AsyncSession = Depends(get_session)) -> Union[SheduleResponse, dict]:
    return await create_chedule(shedule, access_token, session)


@shedule_router.get('/shedule/', status_code=200)
async def get_shedule(get_date: date, access_token: Annotated[str | None, Header()] = None,
                      session: AsyncSession = Depends(get_session)) -> Union[SheduleResponseWithTasks, dict]:
    return await shedule_get(get_date, access_token, session)






