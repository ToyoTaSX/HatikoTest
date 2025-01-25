import logging
import settings
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from db_handlers import database
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from middlewares.whitelist import WhitelistMiddleware

scheduler = AsyncIOScheduler(timezone=settings.TIMEZONE)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
dp.message.outer_middleware(WhitelistMiddleware())