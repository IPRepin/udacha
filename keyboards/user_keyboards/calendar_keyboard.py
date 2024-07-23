from datetime import datetime, timedelta

from aiogram.utils.keyboard import InlineKeyboardBuilder


async def create_calendar_keyboard(callback_prefix: str, start_date: datetime, end_date: datetime):
    builder = InlineKeyboardBuilder()

    # Generate dates buttons
    date = start_date
    while date <= end_date:
        builder.button(text=date.strftime("%d.%m.%Y"), callback_data=f"{callback_prefix}:{date.strftime('%Y-%m-%d')}")
        date += timedelta(days=1)

    builder.adjust(3)  # Adjust the number of buttons per row
    builder.button(text="Отмена", callback_data="cancel")

    return builder.as_markup()
