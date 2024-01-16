import random
import os
from application.usecases.usecase_user import registration_admin, user_activate
import datetime
from typing import Annotated, Union, List

import jwt
from fastapi import Request, Depends, Form, APIRouter, Header, HTTPException
from jwt import DecodeError
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from infrastructure.database.database import get_session
from application.models.model_user import User, Code
from infrastructure.celery.worker import send_code, send_code_staff
from application.shemas.shema_user import UserProfile, UserSchema
from config import HOST, SECRET, EMAIL_PASSWORD, EMAIL_SENDER

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

templates = Jinja2Templates(directory="src/templates/")


@auth_router.post("/registration", response_class=HTMLResponse)
async def registration(request: Request, name=Form(), surname=Form(),
                       email=Form(), password=Form(), session: AsyncSession = Depends(get_session)):
    """Регистрация нового пользователя админа"""
    return await registration_admin(request, name, surname, email, password, session)

@auth_router.post("/get_password", response_class=HTMLResponse)
async def get_password(request: Request, key=Form(), session: AsyncSession = Depends(get_session)):
    """Активация пользователя"""
    return await user_activate(request, key, session)


@auth_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, email=Form(), password=Form(), session: AsyncSession = Depends(get_session)):
    try:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.fetchone()[0]
        if pwd_context.verify(password, user.password):
            token = jwt.encode({"user_id": user.id, "status": user.activate}, SECRET, algorithm="HS256")
            template_response = RedirectResponse(HOST, status_code=301)
            template_response.set_cookie(key='access-token', value=token)
            return template_response
        else:
            raise Exception
    except:
        context = {
            "request": request,
            "error": "Неверный email или пароль",
            "email": email,
            "password": password
        }
        return templates.TemplateResponse('login.html', context=context)





@auth_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    template_response = templates.TemplateResponse('login.html', context={"request": request})
    template_response.delete_cookie(key='access-token')
    return template_response


@auth_router.get("/profile")
async def get_profile(access_token: Annotated[str | None, Header()] = None,
                      session: AsyncSession = Depends(get_session)) -> Union[UserProfile, dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    query = select(User).where(User.id == user_id)
    response = await session.execute(query)
    response = response.fetchone()[0]
    return UserProfile(**response.__dict__)


@auth_router.post("/staff")
async def add_staff(user: UserSchema, access_token: Annotated[str | None, Header()] = None,
                    session: AsyncSession = Depends(get_session)) -> Union[UserSchema, dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    date = datetime.datetime.now().date()
    password = user.password
    hash_password = pwd_context.hash(user.password)
    user = User(name=user.name, surname=user.surname, email=user.email, password=hash_password, activate=True,
                data_create=date,
                is_admin=False, admin_id=user_id)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    await session.close()
    send_code_staff(user.email, user.name, user.surname, password)
    return UserSchema(**user.__dict__)


@auth_router.get('/staff')
async def get_staff_list(access_token: Annotated[str | None, Header()] = None,
                         session: AsyncSession = Depends(get_session)) -> Union[List[UserProfile], dict]:
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    query = select(User).where(User.admin_id == user_id)
    response = await session.execute(query)
    # print(response)
    response = response.fetchmany()
    print(response)
    # print(dir(response))
    users = []
    for user in response:
        print(user[0])
        users.append(UserProfile(**user[0].__dict__))
        print(users)
    # return UserProfile(**response.__dict__)
    return users
