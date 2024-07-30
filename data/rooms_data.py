import logging

from aiogram import types

from data.models import Room

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def add_room(
        name: str,
        description: str,
        photo: str,
        session: AsyncSession,
):
    """Добавление нового номера"""
    try:
        session.add(Room(
            name=name,
            description=description,
            photo=photo
        ))
        await session.commit()
        logger.info(f"Номер добавлен")
    except IntegrityError as error:
        logger.error(f"Номер уже существует")
        logger.error(error)
        await session.rollback()


async def get_all_rooms(session: AsyncSession):
    """Получение всех номеров отеля"""
    query = select(Room)
    result = await session.execute(query)
    return result.scalars().all()


async def get_room_by_name(session: AsyncSession, name: str):
    """Получение комнаты по name"""
    query = select(Room).where(name == Room.name)
    result = await session.execute(query)
    return result.scalars().first()


async def get_room_by_id(session: AsyncSession, id: int):
    """Получение комнаты по name"""
    query = select(Room).where(id == Room.id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_room(session: AsyncSession, message: types.Message):
    """Обновление информации по комнате"""
    query = update(Room).where(Room.name == message.from_user.id).values(
        user_name=message.from_user.first_name,
        user_url=message.from_user.url
    )
    await session.execute(query)
    await session.commit()


async def delete_room(session: AsyncSession, message: types.Message):
    """Удаление комнаты"""
    query = delete(Room).where(Room.name == message.from_user.id)
    await session.execute(query)
    await session.commit()
