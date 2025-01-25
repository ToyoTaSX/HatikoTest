import asyncio
from create_bot import bot, dp, scheduler
from handlers.users import users_router
from time_jobs.token import set_token, update_token

async def main():
    await set_token()

    scheduler.add_job(update_token, 'interval', hours=1)
    scheduler.start()
    dp.include_router(users_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())