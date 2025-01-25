from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types
from aiogram.types import Message

from db_handlers.utils import is_in_whitelist

class WhitelistMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        if await is_in_whitelist(user_id):
            return await handler(event, data)

        await event.answer("У вас нет доступа к использованию этого бота. Для доступа свяжитесь с @ToyoTaSX")