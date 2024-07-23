from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboards() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🐬Забронировать номер")],
            [KeyboardButton(text="🧳Проверить бронирование")],
            [KeyboardButton(text="👋О гостевом доме УДАЧА")],
            [KeyboardButton(text="💬Связаться с нами")],
        ],
        resize_keyboard=True,
    )
    return main_keyboard
