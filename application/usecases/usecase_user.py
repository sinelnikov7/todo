import datetime
import random
import jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from application.services.service_user import ServiceUser
from config import SECRET, HOST
from infrastructure.celery.worker import send_code


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
