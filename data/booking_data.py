import logging

from aiogram import types

from data.models import Booking

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def add_booking(
        session: AsyncSession,
        user_id: str,
        first_name: str,
        user_url: str,
        room: str,
        guests: str,
        check_in_date: str,
        departure_date: str,
        status: str = "❌Не подтверждено"
):
    """Создание нового бронирования"""
    try:
        session.add(Booking(
            user_first_name=first_name,
            user_id=user_id,
            user_url=user_url,
            guests=guests,
            room=room,
            check_in_date=check_in_date,
            departure_date=departure_date,
            status=status
        ))
        await session.commit()
        logger.info(f"Бронирование добавлено")
    except IntegrityError as error:
        logger.error(f"Бронирование уже существует")
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


async def get_booking_by_params(session: AsyncSession, **kwargs):
    query = select(Booking)
    for key, value in kwargs.items():
        query = query.where(getattr(Booking, key) == value)
    result = await session.execute(query)
    return result.scalars().first()


async def update_booking_status(session: AsyncSession, status: str, user_id: Booking):
    """Обновление бронирования"""
    query = update(Booking).where(Booking.user_id == user_id).values(
        status=status
    )
    await session.execute(query)
    await session.commit()


async def delete_booking(session: AsyncSession, message: types.Message):
    """Удаление пользователя"""
    query = delete(Booking).where(Booking.user_id == message.from_user.id)
    await session.execute(query)
    await session.commit()
