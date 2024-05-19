import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.strategy import FSMStrategy

from filters.is_group import ChatTypeFilter
# from handlers.admin.scheduler import scheduler

from loader import db


def setup_handlers(dispatcher: Dispatcher) -> None:
    """HANDLERS"""
    from handlers import setup_routers

    dispatcher.include_router(setup_routers())


def setup_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    """MIDDLEWARE"""
    from middlewares.throttling import ThrottlingMiddleware

    # Spamdan himoya qilish uchun klassik ichki o'rta dastur. So'rovlar orasidagi asosiy vaqtlar 0,5 soniya
    dispatcher.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))


def setup_filters(dispatcher: Dispatcher) -> None:
    """FILTERS"""
    dispatcher.message.filter(ChatTypeFilter(chat_types=['supergroup', 'private']))


async def setup_aiogram(dispatcher: Dispatcher, bot: Bot) -> None:
    setup_handlers(dispatcher=dispatcher)
    setup_middlewares(dispatcher=dispatcher, bot=bot)
    setup_filters(dispatcher=dispatcher)


async def database_connected():
    await db.create()
    # await db.drop_table_users()
    # await db.drop_table_tables()
    await db.drop_table_temporary()
    # await db.drop_table_results()
    # await db.drop_table_sos()
    await db.create_table_users()
    await db.create_table_tables()
    await db.create_table_temporary_answers()
    await db.create_table_results()
    await db.create_table_sos()


async def aiogram_on_startup_polling(dispatcher: Dispatcher, bot: Bot) -> None:
    from utils.set_bot_commands import set_default_commands
    from utils.notify_admins import on_startup_notify

    logger.info("Database connected")
    await database_connected()

    logger.info("Starting polling")
    await bot.delete_webhook(drop_pending_updates=True)
    await setup_aiogram(bot=bot, dispatcher=dispatcher)
    await on_startup_notify(bot=bot)
    await set_default_commands(bot=bot)
    # scheduler.start()


async def aiogram_on_shutdown_polling(dispatcher: Dispatcher, bot: Bot):
    logger.info("Stopping polling")
    await bot.session.close()
    await dispatcher.storage.close()


def main():
    """CONFIG"""
    from data.config import BOT_TOKEN
    from aiogram.enums import ParseMode
    from aiogram.fsm.storage.memory import MemoryStorage

    allowed_updates = ['message', 'chat_member', 'callback_query']
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    storage = MemoryStorage()
    dispatcher = Dispatcher(storage=storage, fsm_strategy=FSMStrategy.CHAT)
    dispatcher.startup.register(aiogram_on_startup_polling)
    dispatcher.shutdown.register(aiogram_on_shutdown_polling)
    asyncio.run(dispatcher.start_polling(bot, close_bot_session=True, allowed_updates=allowed_updates))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped!")
