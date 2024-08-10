from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_rooms_button() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Добавить номер", callback_data="add_room")
    keyboard_builder.button(text="Отредактировать номер", callback_data="edit_room")
    keyboard_builder.button(text="Удалить все номера", callback_data="delite_all_rooms")
    keyboard_builder.adjust(1)
    return keyboard_builder.as_markup()


async def stopping_photo_upload_keyboard() -> InlineKeyboardMarkup:
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text="Сохранить номер в базе", callback_data="stop_photo")
    return keyboard_builder.as_markup()
