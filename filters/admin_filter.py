from aiogram import types
from aiogram.filters import Filter

from config import settings


class AdminProtect(Filter):
    def __init__(self):
        self.admins = settings.ADMINS

    async def __call__(self, message: types.Message):
        return message.from_user.id == self.admins
