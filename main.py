import jwt
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.database import async_session
from presentation.router_user import auth_router
from presentation.router_shedule import shedule_router
from presentation.router_task import task_router
from config import HOST, SECRET


app = FastAPI(title="Main")
app.include_router(auth_router)
templates = Jinja2Templates(directory="templates/")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(shedule_router)
app.include_router(task_router)


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
            return templates.TemplateResponse('index.html', context={'request': request, 'HOST': HOST})
    except:
        return templates.TemplateResponse('login.html', context={'request': request})



# def is_authorizated(fn):
#     @wraps(fn)
#     async def wrapper(*args, **kwargs):
#
#         try:
#             token = kwargs["request"].cookies.get('bearer', None)
#             user = jwt.decode(token, SECRET, algorithms=['HS256'])
#             response = await fn(*args, **kwargs)
#             return response
#         except Exception:
#             return templates.TemplateResponse('login_form.html', context={'request': kwargs["request"]})
#     return wrapper


