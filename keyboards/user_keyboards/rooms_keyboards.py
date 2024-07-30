from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from data.rooms_data import get_all_rooms


class RoomsKeyboards(CallbackData, prefix="show_room"):
    action: str


async def add_rooms_menu(session: AsyncSession) -> InlineKeyboardBuilder:
    menu = InlineKeyboardBuilder()
    rooms = await get_all_rooms(session=session)
    for room in rooms:
        btn_text = room.name
        id_room = room.id  # Получение id номера
        callback_data = RoomsKeyboards(action=str(id_room)).pack()
        menu.row(
            InlineKeyboardButton(text=btn_text, callback_data=callback_data)
        )
    return menu.as_markup()
