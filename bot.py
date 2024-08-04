import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.exceptions import TelegramNetworkError, TelegramRetryAfter
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage

from config import settings
from data.sqlite_connect import create_db, session_factory
from handlers.admin_handler.booking_admin_handler import booking_admin_router
from handlers.admin_handler.room_handlers.add_rooms_handler import admin_room_router
from handlers.user_handler.about_udacha_handlers import about_router

from handlers.user_handler.command_handlers import commands_router
from handlers.user_handler.booking_handlers import user_handlers_router
from utils.commands import register_commands
from utils.logger_settings import setup_logging
from middleware.db_middlewares import DataBaseMiddleware

logger = logging.getLogger(__name__)


async def connect_bot():
    redis_storage = RedisStorage.from_url(settings.REDIS_URL)
    memory_storage = MemoryStorage()
    bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
    dp = Dispatcher(storage=memory_storage)

    dp.include_routers(
        commands_router,
        user_handlers_router,
        about_router,
        admin_room_router,
        booking_admin_router,
    )
    dp.update.middleware(DataBaseMiddleware(session_pool=session_factory))
    await create_db()
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        await register_commands(bot=bot)
    except TelegramNetworkError as error:
        logger.error(error)
    finally:
        await bot.close()


def main():
    setup_logging()
    try:
        asyncio.run(connect_bot())
    except TelegramRetryAfter as error:
        logger.error(error)
    except KeyboardInterrupt as error:
        logger.error(error)


if __name__ == '__main__':
    main()
