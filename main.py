from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Depends,  Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import jwt
import dotenv
import os
from src.database import async_session
from src.auth.schemas import User_schema
from src.auth.models import User
from src.todo.router import to_do_router
from src.auth.router import auth_router
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


dotenv.load_dotenv()
SECRET = os.environ.get('SECRET')
EMAIL_SENDER = os.environ.get('EMAIL_SENDER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
app = FastAPI(title="Main")
app.include_router(to_do_router)
app.include_router(auth_router)
templates = Jinja2Templates(directory="src/templates/")
app.mount("/static", StaticFiles(directory="src/static"), name="static")

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        token = request.cookies['access-token']
        status = jwt.decode(token, SECRET, algorithms=['HS256'])
        if status.get('status') == False:
            return templates.TemplateResponse('get_password.html', context={'request': request})
        else:
            return templates.TemplateResponse('index.html', context={'request': request})
    except:
        return templates.TemplateResponse('login.html', context={'request': request})

@app.get("/users/{id}")
async def get_user(id: int, response: Response,  session: AsyncSession = Depends(get_session), )-> User_schema:
    response.set_cookie(key='qqq', value="qqq", httponly=False)
    query = select(User)
    result = await session.execute(query)
    user = result.fetchone()[0]
    responses = {
        "id": user.id,
        "email": user.email,
        "password": user.password,
        "name": user.name,
        "surname": user.surname
    }
    return responses

