import logging

from aiogram import types

from data.models import Room

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def add_room(
        title_room: Room.name,
        description_room: Room.description,
        photo_room: Room.photo,
        session: AsyncSession,
):
    """Добавление нового номера"""
    try:
        session.add(Room(
            name=title_room,
            description=description_room,
            photo=photo_room
        ))
        await session.commit()
        logger.info("Номер добавлен")
    except IntegrityError:
        logger.error("Номер уже существует")
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


async def get_room_by_id(session: AsyncSession, id: Room.id):
    """Получение комнаты по name"""
    query = select(Room).where(id == Room.id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_room(session: AsyncSession,
                      id_room: Room.id,
                      title_room: Room.name,
                      description_room: Room.description,
                      photo_room: Room.photo):
    """Обновление информации по комнате"""
    query = update(Room).where(Room.id == id_room).values(
        name=title_room,
        description=description_room,
        photo=photo_room
    )
    await session.execute(query)
    await session.commit()


async def delete_room(session: AsyncSession, message: types.Message):
    """Удаление комнаты"""
    query = delete(Room).where(Room.name == message.from_user.id)
    await session.execute(query)
    await session.commit()
