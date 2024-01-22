from functools import wraps

import jwt
from jwt import DecodeError
from fastapi import HTTPException

from config import SECRET


def is_authorizated_api(fn):
    """Проверка токена авторизации"""
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            token = kwargs['access_token']
            jwt.decode(token, SECRET, algorithms=['HS256'])
            response = await fn(*args, **kwargs)
            return response
        except DecodeError:
            raise  HTTPException(status_code=401, detail='Неверный токен доступа')
    return wrapper