from datetime import datetime, timedelta
import logging
from typing import List

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Booking, User

logger = logging.getLogger(__name__)


async def send_notification(bot: Bot, user_id: int, message: str) -> None:
    """Отправка уведомления пользователю"""
    try:
        await bot.send_message(chat_id=user_id, text=message)
        logger.info(f"Notification sent to user {user_id}")
    except Exception as e:
        logger.error(f"Failed to send notification to user {user_id}: {e}")


async def check_upcoming_bookings(session: AsyncSession) -> List[Booking]:
    """Получение бронирований, которые начинаются в ближайшие 24 часа"""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    query = select(Booking).where(
        Booking.check_in_date <= tomorrow,
        Booking.check_in_date >= today,
        Booking.status != "Отменено"
    )
    result = await session.execute(query)
    return result.scalars().all()


async def check_checkout_reminders(session: AsyncSession) -> List[Booking]:
    """Получение бронирований, где выезд через 24 часа"""
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    query = select(Booking).where(
        Booking.departure_date <= tomorrow,
        Booking.departure_date >= today,
        Booking.status != "Отменено"
    )
    result = await session.execute(query)
    return result.scalars().all()


async def send_booking_reminder(bot: Bot, session: AsyncSession) -> None:
    """Отправка напоминаний о предстоящем заезде"""
    bookings = await check_upcoming_bookings(session)
    for booking in bookings:
        message = (
            f"Напоминаем о вашем предстоящем заезде!\n\n"
            f"Дата заезда: {booking.check_in_date}\n"
            f"Дата выезда: {booking.departure_date}\n"
            f"Номер комнаты: {booking.room}\n"
            f"Количество гостей: {booking.guests}\n\n"
            f"Ждем вас! Если у вас есть вопросы, пожалуйста, свяжитесь с нами."
        )
        await send_notification(bot, booking.user_id, message)


async def send_checkout_reminder(bot: Bot, session: AsyncSession) -> None:
    """Отправка напоминаний о предстоящем выезде"""
    bookings = await check_checkout_reminders(session)
    for booking in bookings:
        message = (
            f"Напоминаем о предстоящем выезде!\n\n"
            f"Дата выезда: {booking.departure_date}\n"
            f"Время выезда до 12:00\n\n"
            f"Спасибо, что выбрали наш гостевой дом!"
        )
        await send_notification(bot, booking.user_id, message)


async def send_feedback_request(bot: Bot, session: AsyncSession) -> None:
    """Отправка запроса на отзыв после выезда"""
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    query = select(Booking).where(
        Booking.departure_date <= yesterday,
        Booking.departure_date >= two_days_ago,
        Booking.status != "Отменено"
    )
    result = await session.execute(query)
    bookings = result.scalars().all()

    for booking in bookings:
        message = (
            f"Спасибо, что выбрали наш гостевой дом!\n\n"
            f"Пожалуйста, поделитесь своими впечатлениями о пребывании. "
            f"Ваш отзыв поможет нам стать лучше!\n\n"
            f"Для того чтобы оставить отзыв, воспользуйтесь командой /feedback"
        )
        await send_notification(bot, booking.user_id, message)
