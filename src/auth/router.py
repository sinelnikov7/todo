import random
import os

import jwt
import dotenv
from fastapi import Request, Depends, Form, APIRouter
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext

from src.database import get_session
from .models import User, Code
from worker import send_code
from src.config import HOST


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

dotenv.load_dotenv()
SECRET = os.environ.get('SECRET')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="src/templates/")

@auth_router.post("/registration", response_class=HTMLResponse)
async def registration(request: Request, name = Form(), surname = Form(),
                       email = Form(), password = Form(), session: AsyncSession = Depends(get_session)):
    try:
        number = random.randint(1000, 9999)
        hash_password = pwd_context.hash(password)
        user = User(name=name, surname=surname, email=email, password=hash_password, activate=False)
        key = Code(key=number)
        user.code = key
        session.add(user)
        await session.commit()
        await session.refresh(user)
        await session.close()
        token = jwt.encode({"user_id": user.id, "status": False}, SECRET, algorithm="HS256")
        template_response = templates.TemplateResponse('get_password.html', context={'request': request})
        template_response.set_cookie(key='access-token', value=token)
        send_code.delay(email, name, surname, password, number)
        return template_response
    except IntegrityError:
        return templates.TemplateResponse('login.html', context={'request': request, 'error_registration': 'Пользователь с таким email уже зарегестрирован'})

@auth_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, email = Form(), password = Form(), session: AsyncSession = Depends(get_session)):
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

@auth_router.post("/get_password", response_class=HTMLResponse)
async def get_password(request: Request, key = Form(), session: AsyncSession = Depends(get_session)):
    try:
        key = int(key)
    except Exception:
        return templates.TemplateResponse('get_password.html',
                                          context={'request': request, "error": "Не правильный код"})
    token = request.cookies.get('access-token')
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = payload.get('user_id')
    query = select(Code.key).where(Code.user_id == user_id)
    result = await session.execute(query)
    result_key = result.fetchone()[0]
    if result_key == key:
        query = update(User).where(User.id == user_id).values(activate = True)
        await session.execute(query)
        await session.commit()
        token = jwt.encode({"user_id": user_id, "status": True}, SECRET, algorithm="HS256")
        template_response = RedirectResponse(HOST, status_code=301)
        template_response.set_cookie(key="access-token", value=token)
        return template_response
    else:
        return templates.TemplateResponse('get_password.html', context={'request': request, "error": "Не правильный код"})

@auth_router.get("/logout", response_class=HTMLResponse)
async def login(request: Request):
    template_response = templates.TemplateResponse('login.html', context={"request": request})
    template_response.delete_cookie(key='access-token')
    return template_response

