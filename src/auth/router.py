import random
import smtplib
from fastapi import FastAPI, Request, Depends, Form, Response, Cookie, APIRouter
from passlib.context import CryptContext
from sqlalchemy import select, and_, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import dotenv
import os
from src.database import async_session, get_session
from .schemas import User_schema, Login_shema
from .models import User, Code
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from passlib.context import CryptContext
from email.mime.application import MIMEApplication

dotenv.load_dotenv()
SECRET = os.environ.get('SECRET')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

templates = Jinja2Templates(directory="templates/")

@auth_router.post("/registration", response_class=HTMLResponse)
async def registration(request: Request, name = Form(), surname = Form(),
                       email = Form(), password = Form(), session: AsyncSession = Depends(get_session)):
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
    template_response.set_cookie(key='access-token', value=token, httponly=True)
    email_sender = EMAIL_SENDER
    password = EMAIL_PASSWORD
    email_getter = user.email
    smtp_server = smtplib.SMTP('smtp.yandex.ru', 587)
    smtp_server.starttls()
    msg = MIMEMultipart()
    msg.attach(MIMEText(f"Здравствуйте {name} {surname}!\nВаш логин - {email}\nПароль - {password}\nДля продолжения введите проверочный код регистрации на сайте ToDo - {str(number)}"))
    msg["From"] = email_sender
    msg["Subject"] = "Код подтверждения регистрации на сайте ToDo"
    smtp_server.set_debuglevel(1)
    smtp_server.login(email_sender, password)
    smtp_server.sendmail(email_sender, email_getter, msg.as_string())
    smtp_server.quit()
    return template_response

@auth_router.post("/login", response_class=HTMLResponse)
async def login(request: Request, email = Form(), password = Form(), session: AsyncSession = Depends(get_session)):
    try:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.fetchone()[0]
        if pwd_context.verify(password, user.password):
            token = jwt.encode({"user_id": user.id, "status": user.activate}, SECRET, algorithm="HS256")
            template_response = RedirectResponse('http://127.0.0.1:8000', status_code=301)
            template_response.set_cookie(key='access-token', value=token, httponly=True)
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
        # query = User.update().values(activate=True).where(User.id == user_id)
        await session.execute(query)
        await session.commit()
        token = jwt.encode({"user_id": user_id, "status": True}, SECRET, algorithm="HS256")
        template_response = RedirectResponse('/', status_code=301)
        template_response.set_cookie(key="access-token", value=token)
        return template_response
    else:
        return templates.TemplateResponse('get_password.html', context={'request': request, "error": "Не правильный код"})

@auth_router.get("/logaut", response_class=HTMLResponse)
async def login(request: Request):
    template_response = templates.TemplateResponse('login.html', context={"request": request})
    template_response.delete_cookie(key='access-token')
    return template_response