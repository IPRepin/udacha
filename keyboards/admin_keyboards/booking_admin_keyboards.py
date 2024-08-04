from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from data.booking_data import get_all_bookings


async def get_booking_admin_keyboards() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Проверить заявки на бронирования")],
        ],
        resize_keyboard=True,
    )
    return main_keyboard


async def send_user_keyboard(user_url: str):
    send_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Написать клиенту", url=user_url)],
        ]
    )
    return send_keyboard


async def add_moderation_keyboard():
    moderation_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅Одобрено", callback_data="approved")],
            [InlineKeyboardButton(text="🚫Отклонено", callback_data="rejected")],
        ]
    )
    return moderation_keyboard
