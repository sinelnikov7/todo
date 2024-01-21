from httpx import AsyncClient
from sqlalchemy import select

from application.models.model_user import User, Code
from conftest import async_session_maker_test

form_data_register = {
        "name": "user",
        "surname": "surname",
        "email": "email@email.ru",
        "password": "hash_password",
        "activate": False
    }


async def test_register(ac: AsyncClient):

    response = await ac.post('/auth/registration', data=form_data_register)
    assert response.status_code == 200

async def test_register_unique_mail(ac: AsyncClient):

    response = await ac.post('/auth/registration', data=form_data_register)
    assert response.status_code == 200
    async with async_session_maker_test() as session:
        query = select(User)
        result = await session.execute(query)
        assert len(result.all()) == 1

async def test_create_and_register_code(ac: AsyncClient):

    async with async_session_maker_test() as session:
        query = select(Code.key).where(Code.user_id == 1)
        result = await session.execute(query)
        code = result.all()[0][0]
        response = await ac.post('/auth/get_password', data={"key":code})
        assert response.status_code == 301
        response = await ac.post('/auth/get_password', data={"key": 1})
        assert response.status_code == 200


async def test_login_true_credit(ac: AsyncClient):

    true_response = await ac.post('/auth/login', data={"email": form_data_register.get('email'),
                                                  "password": form_data_register.get('password')})
    assert true_response.status_code == 301


async def test_login_false_credit(ac: AsyncClient):

    false_response_email = await ac.post('/auth/login', data={"email": 'false@email.ru',
                                                              "password": form_data_register.get('password')})
    assert false_response_email.status_code == 200
    false_response_password = await ac.post('/auth/login', data={"email": 'false@email.ru',
                                                                 "password": '1111'})
    assert false_response_password.status_code == 200
    false_response_password_email = await ac.post('/auth/login', data={"email": form_data_register.get('email'),
                                                                 "password": '1111'})
    assert false_response_password_email.status_code == 200

async def test_logout(ac: AsyncClient):
    response = await ac.get('/auth/logout')
    assert response.status_code == 200



