from aiogram import Router, types
from aiogram.filters import CommandStart

from filters.admin_filter import AdminProtect
from keyboards.user_keyboards.main_user_keyboards import get_main_keyboards

commands_router = Router()


@commands_router.message(CommandStart(), AdminProtect())
async def get_start_command_admin(message: types.Message):
    await message.answer(f"{message.from_user.first_name} добро пожаловать!\n"
                         f"Вы являетесь администратором бота")


@commands_router.message(CommandStart())
async def get_start_command_user(message: types.Message):
    await message.answer_photo(photo="https://telegra.ph/file/8b95208dd427aedc02ed3.png",
                               caption=f"{message.from_user.first_name} добро пожаловать!\n"
                                       f'Я 🤖чат-бот гостевого дома "УДАЧА"\n'
                                       f'Я помогу:\n'
                                       f'☀️Забронировать номер\n'
                                       f'☀️Проверить текущее бронирование...',
                               reply_markup=await get_main_keyboards()
                               )
