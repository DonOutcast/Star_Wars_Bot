import aiogram.types
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from template_tgbot.config import load_config


async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Запуск",
        ),
        BotCommand(
            command="help",
            description="Помощь"
        )
    ]
    admin_commands = commands.copy()
    admin_commands.append(
        BotCommand(
            command="admin",
            description="Для админа"
        )
    )
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())

    for admin_id in load_config().tg_bot.admin_ids:
        await bot.set_my_commands(
            commands=admin_commands,
            scope=BotCommandScopeChat(
                chat_id=admin_id
            ),
        )
