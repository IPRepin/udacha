from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from sqlalchemy.ext.asyncio import AsyncSession

from data.rooms_data import get_all_rooms


class RoomsKeyboards(CallbackData, prefix="show_room"):
    action: str


async def add_rooms_menu(session: AsyncSession) -> InlineKeyboardMarkup:
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


class InfoRoomsKeyboards(CallbackData, prefix="info_room"):
    action: str


async def info_rooms_menu(session: AsyncSession) -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    rooms = await get_all_rooms(session=session)
    for room in rooms:
        btn_text = room.name
        id_room = room.id  # Получение id номера
        callback_data = InfoRoomsKeyboards(action=str(id_room)).pack()
        menu.row(
            InlineKeyboardButton(text=btn_text, callback_data=callback_data)
        )
    return menu.as_markup()


async def get_about_us_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.row(
        InlineKeyboardButton(text="Номерной фонд", callback_data="all_room_info")
    )
    return menu.as_markup()


async def get_back_all_rooms_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.row(
        InlineKeyboardButton(text="К списку номеров", callback_data="back_all_rooms")
    )
    return menu.as_markup()
