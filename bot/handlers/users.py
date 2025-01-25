import os
from datetime import datetime
from pprint import pprint

from aiogram.filters.callback_data import CallbackData
from settings import ADMINS
from keyboards.kb import get_kb
import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from filters.is_admin import IsAdmin
from db_handlers.utils import add_user, delete_user
from settings import API_URL


async def get_balance():
    url = API_URL + 'api/balance/'
    headers = {'Authorization': f'Bearer {os.environ.get("access_token")}'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return float(data['balance'])


async def get_services():
    url = API_URL + 'api/services/'
    headers = {'Authorization': f'Bearer {os.environ.get("access_token")}'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data['services']

async def get_check(imei, service_id):
    url = API_URL + 'api/check-imei/'
    headers = {
        'Authorization': f'Bearer {os.environ.get("access_token")}'
    }
    data = {
        'imei': imei,
        'service_id': int(service_id)
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            data = await response.json()
            if 'check' in data:
                return data['check'], True
            return data['errors'], False



def validate_imei(imei: str) -> bool:
    if len(imei) != 15 or not imei.isdigit():
        return False

    total = 0
    for i, digit in enumerate(imei[:14]):
        num = int(digit)
        if i % 2 == 1:
            num *= 2
            if num > 9:
                num -= 9
        total += num

    calculated_checksum = (10 - (total % 10)) % 10
    return calculated_checksum == int(imei[-1])


class ServiceCallback(CallbackData, prefix="service_cb"):
    imei: str
    price: float
    service_id: int


users_router = Router()

@users_router.message(IsAdmin(ADMINS), Command(commands=["adduser"]))
async def univers_cmd_handler(message: Message, command: CommandObject):
    command_args: str = command.args
    if await add_user(command_args):
        await message.answer('Пользователь добавлен в список')
    else:
        await message.answer('Пользователь не добавлен')


@users_router.message(IsAdmin(ADMINS), Command(commands=["deleteuser"]))
async def univers_cmd_handler(message: Message, command: CommandObject):
    command_args: str = command.args
    if await delete_user(command_args):
        await message.answer('Пользователь удален')
    else:
        await message.answer('Пользователь не удален / не найден')



@users_router.message(CommandStart())
async def cmd_start(message: Message):
    print(await get_services())
    await message.answer('Это бот для проверки IMEI, отправьте мне IMEI для проверки')


@users_router.message(F.text)
async def cmd(message: Message, state: FSMContext):
    if not validate_imei(message.text):
        await message.answer('Вы ввели невалидный IMEI')
        return
    balance = await get_balance()
    services = list(filter(lambda x: float(x['price']) <= balance, await get_services()))
    await state.update_data(data={
        'services': services,
        'balance': balance,
        'imei': message.text,
    })
    kb = await get_kb(
        services,
        lambda x: ServiceCallback(service_id=x["id"], imei=message.text, price=float(x['price'])).pack(),
        lambda x: f'{x["title"]} | {x["price"]}'
    )
    await message.answer(f'Выберите сервис\nВаш текущий баланс: {balance}', reply_markup=kb)


@users_router.callback_query(ServiceCallback.filter())
async def cb(query: CallbackQuery, callback_data: ServiceCallback, state: FSMContext):
    msg = await query.message.answer('Ожидайте, обработка данных')
    mrkp = query.message.reply_markup
    await query.message.edit_reply_markup(reply_markup=None)
    state_data = await state.get_data()
    service_id = callback_data.service_id
    imei = state_data.get('imei')
    balance = state_data.get('balance')
    service = [i for i in state_data.get('services') if i['id'] == service_id][0]
    if float(service['price']) > balance:
        await query.answer('Нехватает денег на балансе')
        return
    data, is_check = await get_check(imei, service_id)
    #print(data)
    if not is_check:
        await query.message.answer('Ошибка: ' + (str(data)))
        return
    pprint(data)
    await msg.delete()
    if data['status'] != 'successful':
        await query.message.answer('Сервис не смог получить информацию об IMEI')
        await query.message.edit_reply_markup(reply_markup=mrkp)
        return

    def format_timestamp(timestamp):
        return datetime.utcfromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M:%S")
    properties = data['properties']
    try:
        formatted_output = f"""
📋 **Информация о заказе**
- Статус: {data.get("status", "Не указано")}
- Услуга: {data.get("service", {}).get("title", "Не указано")} (ID: {data.get("service", {}).get("id", "Не указано")})
- Сумма: {data.get("amount", "Не указано")} USD
- Обработано: {format_timestamp(data.get("processedAt"))}

📱 **Информация об устройстве**
- IMEI: {properties.get("imei", "Не указано")}
- Устройство: {properties.get("deviceName", "Не указано")}
- Изображение: {properties.get("image", "Не указано")}
- Дата покупки: {format_timestamp(properties.get("estPurchaseDate"))}
- SIM Lock: {"Да" if properties.get("simLock") else "Нет"}
- Гарантия: {properties.get("warrantyStatus", "Не указано")}
- Покрытие ремонта: {properties.get("repairCoverage", "Не указано")}
- Техническая поддержка: {properties.get("technicalSupport", "Не указано")}
- Описание модели: {properties.get("modelDesc", "Не указано")}
- Страна покупки: {properties.get("purchaseCountry", "Не указано")}
- Регион: {properties.get("apple/region", "Не указано")}
- FMI включён: {"Да" if properties.get("fmiOn") else "Нет"}
- Режим утери: {properties.get("lostMode", "Не указано")}
- Статус блокировки в США: {properties.get("usaBlockStatus", "Не указано")}
- Сеть: {properties.get("network", "Не указано")}
- Демонстрационная модель: {"Да" if properties.get("demoUnit") else "Нет"}
- Восстановленный: {"Да" if properties.get("refurbished") else "Нет"}
        """

        await query.message.answer(formatted_output)
        await query.message.answer('Введите IMEI для нового заказа')
        await query.message.delete()
    except Exception as e:
        print(e)
        await query.message.answer(str(e))
        await query.message.edit_reply_markup(reply_markup=mrkp)


