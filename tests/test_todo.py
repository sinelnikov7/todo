from httpx import AsyncClient

from test_auth import form_data_register

token = ''

async def test_create_shedule(ac: AsyncClient):
    global token
    get_token = await ac.post('/auth/login', data={"email": form_data_register.get('email'),
                                                   "password": form_data_register.get('password')})
    token = get_token.cookies.get('access-token')
    response_true_token = await ac.post('/todo/shedule', json={"date": "2021-07-05"}, headers={'access-token': token})
    assert response_true_token.json() == {"status": "201", "data": {"id": 1, "date": "2021-07-05", "user_id": 1}}
    response_false_token = await ac.post('/todo/shedule', json={"date": "2021-07-05"}, headers={'access-token': '123'})
    assert response_false_token.status_code == 401
    response_double_shedule = await ac.post('/todo/shedule', json={"date": "2021-07-05"}, headers={'access-token': token})
    assert response_double_shedule.json() == {"status": "У пользователя уже есть расписание на эту дату"}

async def test_get_shedule(ac: AsyncClient):
    response_true_date = await ac.get('/todo/shedule/?get_date=2021-07-05', headers={'access-token': token})
    assert response_true_date.json() == {"success": True, "id": 1, "date": "2021-07-05", "tasks": []}
    response_false_date = await ac.get('/todo/shedule/?get_date=2021-07-06', headers={'access-token': token})
    assert response_false_date.json() == {"detail": "Расписания  не существует, или оно не принадлежит данному юзеру"}
    response_false_token = await ac.get('/todo/shedule/?get_date=2021-07-05', headers={'access-token': '123'})
    assert response_false_token.json() == {"detail": "Неверный токен доступа"}

async def test_create_task(ac: AsyncClient):

    data = {
              "time": "09:00",
              "title": "Подъем",
              "status": 1,
              "priority": "Важное",
              "color_priority": "#b64dc3b2",
              "date": "2021-07-05"
            }
    response = await ac.post('/todo/task', json=data, headers={'access-token': token})
    assert response.json() == {
                                "success": True,
                                "id": 1,
                                "time": "09:00:00",
                                "title": "Подъем",
                                "status": 1,
                                "priority": "Важное",
                                "color_priority": "#b64dc3b2",
                                "date": "2021-07-05"
                            }

async def test_get_task(ac: AsyncClient):
    response = await ac.get('/todo/task/1', headers={'access-token': token})
    assert response.json() == {'success': True, 'id': 1, 'time': '09:00:00', 'title': 'Подъем',
                               'status': 1, 'priority': 'Важное', 'color_priority': '#b64dc3b2'}

async def test_update_task(ac: AsyncClient):
    data = {
            "time": "10:00",
            "title": "Завтрак",
            "status": 2,
            "priority": "Тоже важный",
            "color_priority": "#FFFFF"
            }
    response = await ac.patch('/todo/task/1', json=data, headers={'access-token': token})
    assert response.json() == {'status': 200}

async def test_dellete_task(ac: AsyncClient):
    response = await ac.delete('/todo/task/1', headers={'access-token': token})
    assert response.json() == {'staus': {'status': 200}}
