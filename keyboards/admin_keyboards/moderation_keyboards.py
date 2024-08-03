from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def add_moderation_keyboard():
    moderation_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅Одобрено", callback_data="approved")],
            [InlineKeyboardButton(text="🚫Отклонено", callback_data="rejected")],
        ]
    )
    return moderation_keyboard
