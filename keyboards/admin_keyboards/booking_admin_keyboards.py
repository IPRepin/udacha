from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


async def get_booking_admin_keyboards() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Проверить заявки на бронирования")],
            [KeyboardButton(text="На главное меню")],
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
