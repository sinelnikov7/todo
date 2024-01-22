import jwt

from config import SECRET


def get_user_id(token):
    """Получение id юзера по токену"""
    payload = jwt.decode(token, SECRET, algorithms=['HS256'])
    user_id = payload.get('user_id')
    return user_id