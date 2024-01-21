import datetime
import random

import jwt
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from jwt import DecodeError

from application.services.service_user import ServiceUser
from application.shemas.shema_user import UserProfile, UserSchema
from config import SECRET, HOST
from infrastructure.celery.worker import send_code, send_code_staff


templates = Jinja2Templates(directory="templates/")
user = ServiceUser()


async def registration_admin(request, name: str, surname: str, email: str, password: str, session: AsyncSession):
        """Регистрация нового пользователя админа"""
        try:
            date = datetime.datetime.now().date()
            number = random.randint(1000, 9999)
            user_id = await user.create_admin(name, surname, email, password, date, session, number) # Создание нового пользователя суперадмина
            token = jwt.encode({"user_id": user_id, "status": False}, SECRET, algorithm="HS256")
            template_response = templates.TemplateResponse('get_password.html', context={'request': request})
            template_response.set_cookie(key='access-token', value=token)
            send_code(email, name, surname, password, number)
            return template_response
        except IntegrityError:
            return templates.TemplateResponse('login.html', context={'request': request, 'error_registration': 'Пользователь с таким email уже зарегестрирован'})


async def user_activate(request, key, session: AsyncSession):
    """Активация пользователя"""
    try:
        key = int(key)
    except Exception:
        return templates.TemplateResponse('get_password.html',
                                          context={'request': request, "error": "Не правильный код"})
    token = request.cookies.get('access-token')
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = payload.get('user_id')
    result_key = await user.get_user_code(user_id, session)
    if result_key == key:
        await user.activate_user(user_id, session)
        token = jwt.encode({"user_id": user_id, "status": True}, SECRET, algorithm="HS256")
        template_response = RedirectResponse(HOST, status_code=301)
        template_response.set_cookie(key="access-token", value=token)
        return template_response
    else:
        return templates.TemplateResponse('get_password.html',
                                          context={'request': request, "error": "Не правильный код"})


async  def user_login(request, email, password, session: AsyncSession):
    """Авторизация пользователя"""
    try:
        user_info = await user.get_user_with_email(email, session)
        if user.pwd_context.verify(password, user_info.password):
            token = jwt.encode({"user_id": user_info.id, "status": user_info.activate}, SECRET, algorithm="HS256")
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


async def get_user_profile(access_token, session: AsyncSession):
    """Получить профиль пользователя"""
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    profile = await user.get_user_with_id(user_id, session)
    return UserProfile(**profile.__dict__)


async def registration_staff(user_shema, access_token, session):
    """Создание сотрудника"""
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    date = datetime.datetime.now().date()
    new_staff = await user.create_staff(user_shema.name, user_shema.surname,
                                        user_shema.email, user_shema.email, user_id, date, session)
    send_code_staff(new_staff.email, new_staff.name, new_staff.surname, user_shema.email)
    return UserSchema(**new_staff.__dict__)


async def staff_list(access_token, session):
    """Получить список сотрудников"""
    try:
        token = access_token
        user_id = jwt.decode(token, SECRET, algorithms=['HS256']).get("user_id")
    except DecodeError:
        raise HTTPException(status_code=401, detail='Неверный токен доступа')
    users = await user.get_employees_list(user_id, session)
    users_list = []
    for user_staff in users:
        users_list.append(UserProfile(**user_staff[0].__dict__))
    return users_list