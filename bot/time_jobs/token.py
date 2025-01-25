import os

import aiohttp

from settings import BOT_API_PASSWORD, BOT_API_USERNAME, API_URL
async def set_token():
    url = API_URL + 'auth/token/'
    data = {
        'username': BOT_API_USERNAME,
        'password': BOT_API_PASSWORD
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                os.environ['access_token'] = response_data['access']
                os.environ['refresh_token'] = response_data['refresh']
                print("Токен установлен")
            else:
                print(f"Ошибка! Статус: {response.status}")

async def update_token():
    url = API_URL + 'auth/token/refresh/'
    data = {
        'refresh': os.environ.get('refresh_token'),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            if response.status == 200:
                response_data = await response.json()
                os.environ['access_token'] = response_data['access']
                os.environ['refresh_token'] = response_data['refresh']
            else:
                print(f"Ошибка! Статус: {response.status}")