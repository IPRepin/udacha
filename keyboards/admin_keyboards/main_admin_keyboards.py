from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_admin_keyboards() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Номера")],
            [KeyboardButton(text="Бронирования")],
            [KeyboardButton(text="Рассылка")],
            [KeyboardButton(text="База посетителей")],
        ],
        resize_keyboard=True,
    )
    return main_keyboard
