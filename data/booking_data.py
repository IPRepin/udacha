import logging

from aiogram import types

from data.models import Booking

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def add_booking(
        session: AsyncSession,
        message: types.Message,
):
    """Создание нового бронирования"""
    try:
        session.add(Booking(
            user_first_name=message.text,
            user_id=message.text,
            room=message.text,
            check_in_date=message.text,
            departure_date=message.text,
            status=message.text
        ))
        await session.commit()
        logger.info(f"Бронирование добавлено {message.from_user.first_name} добавлено")
    except IntegrityError as error:
        logger.error(f"Бронирование  {message.from_user.first_name} уже существует")
        logger.error(error)
        await session.rollback()


async def get_all_bookings(session: AsyncSession):
    """Получение всех бронирований"""
    query = select(Booking)
    result = await session.execute(query)
    return result.scalars().all()


async def get_all_booking_by_user_id(session: AsyncSession, user_id: int):
    """Получение всех бронирований по user_id"""
    query = select(Booking).where(user_id == Booking.user_id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_booking_by_user_id(session: AsyncSession, user_id: int):
    """Получение бронирования по user_id"""
    query = select(Booking).where(user_id == Booking.user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_booking_status(session: AsyncSession, message: types.Message):
    """Обновление бронирования"""
    query = update(Booking).where(Booking.user_id == message.from_user.id).values(
        status=message.text
    )
    await session.execute(query)
    await session.commit()


async def delete_booking(session: AsyncSession, message: types.Message):
    """Удаление пользователя"""
    query = delete(Booking).where(Booking.user_id == message.from_user.id)
    await session.execute(query)
    await session.commit()
