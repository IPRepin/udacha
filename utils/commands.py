from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def register_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Начать работу с ботом.",
        ),
        BotCommand(
            command="help",
            description="Помощь по функциям бота.",
        ),
    ]
    return bot.set_my_commands(commands, scope=BotCommandScopeDefault())
