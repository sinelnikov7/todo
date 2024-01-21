from typing import Annotated, Union, List
from fastapi import Request, Depends, Form, APIRouter, Header
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from infrastructure.database.database import get_session
from application.shemas.shema_user import UserProfile, UserSchema
from application.usecases.usecase_user import registration_admin, user_activate, user_login, \
    get_user_profile, registration_staff, staff_list


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
templates = Jinja2Templates(directory="templates/")


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
    """Авторизация пользователя"""
    return await user_login(request, email, password, session)


@auth_router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    """Выход из профиля пользоватля"""
    template_response = templates.TemplateResponse('login.html', context={"request": request})
    template_response.delete_cookie(key='access-token')
    return template_response


@auth_router.get("/profile")
async def get_profile(access_token: Annotated[str | None, Header()] = None,
                      session: AsyncSession = Depends(get_session)) -> Union[UserProfile, dict]:
    """Получить профиль пользователя"""
    return await get_user_profile(access_token, session)


@auth_router.post("/staff")
async def add_staff(user_shema: UserSchema, access_token: Annotated[str | None, Header()] = None,
                    session: AsyncSession = Depends(get_session)) -> Union[UserSchema, dict]:
    """Создание сотрудника"""
    return await registration_staff(user_shema, access_token, session)


@auth_router.get('/staff')
async def get_staff_list(access_token: Annotated[str | None, Header()] = None,
                         session: AsyncSession = Depends(get_session)) -> Union[List[UserProfile], dict]:
    """Получить список сотрудников"""
    return await staff_list(access_token, session)
