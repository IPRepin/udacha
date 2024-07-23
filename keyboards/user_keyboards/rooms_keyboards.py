from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


async def rooms_menu() -> InlineKeyboardBuilder:
    menu = InlineKeyboardBuilder()
    menu.row(InlineKeyboardButton(text="Апартаменты 2х этажные с кухней", callback_data="apart_2_etaja"))
    menu.row(InlineKeyboardButton(text="Семейный 2х комнатный номер", callback_data="family_2_rooms"))
    menu.row(InlineKeyboardButton(text="Семейный 5,6ти местный номер", callback_data="family_5-6_4_places"))
    menu.row(InlineKeyboardButton(text="4х местный номер", callback_data="4_places"))
    menu.row(InlineKeyboardButton(text="3х местный номер", callback_data="3_places"))
    menu.row(InlineKeyboardButton(text="2х местный номер Комфорт", callback_data="2_places_comfort"))
    menu.row(InlineKeyboardButton(text="2х местный номер без балкона", callback_data="2_places"))
    return menu.as_markup()
