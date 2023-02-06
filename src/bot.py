import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from template_tgbot.config import load_config
from template_tgbot.handlers.admin import admin_router
from template_tgbot.handlers.echo import echo_router
from template_tgbot.handlers.user import user_router
from template_tgbot.middlewares.config import ConfigMiddleware
from template_tgbot.services import broadcaster
from template_tgbot.utils import set_bot_commands


from template_tgbot.database import base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from template_tgbot.middlewares.database import DatabaseMiddleware


logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот работает")


def register_global_middlewares(dp: Dispatcher, config):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    # print(db.make_connection_string(config.db))
    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    for router in [
        admin_router,
        user_router,
        echo_router
    ]:
        dp.include_router(router)

    register_global_middlewares(dp, config)

    engine: AsyncEngine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/'
        f'{config.db.database}', echo=False, future=True)
    db_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    dp.message.middleware(DatabaseMiddleware(db_session))
    try:
        await set_bot_commands.set_default_commands(bot)
        await on_startup(bot, config.tg_bot.admin_ids)
        await dp.start_polling(bot)
    finally:
        await engine.dispose()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Ошибка")
