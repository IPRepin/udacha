import logging

from aiogram import types

from data.models import User

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def add_user(
        session: AsyncSession,
        message: types.Message,
):
    """Создание нового пользователя"""
    try:
        session.add(User(
            user_first_name=message.from_user.first_name,
            user_id=message.from_user.id,
            user_url=message.from_user.url
        ))
        await session.commit()
        logger.info(f"Пользователь {message.from_user.id} добавлен")
    except IntegrityError as error:
        logger.error(f"Пользователь {message.from_user.id} уже существует")
        logger.error(error)
        await session.rollback()


async def get_all_users(session: AsyncSession):
    """Получение всех пользователей"""
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


async def get_user_by_user_id(session: AsyncSession, user_id: int):
    """Получение пользователя по user_id"""
    query = select(User).where(user_id == User.user_id)
    result = await session.execute(query)
    return result.scalars().first()


async def update_user(session: AsyncSession, message: types.Message):
    """Обновление пользователя"""
    query = update(User).where(User.user_id == message.from_user.id).values(
        user_name=message.from_user.first_name,
        user_url=message.from_user.url
    )
    await session.execute(query)
    await session.commit()


async def delete_user(session: AsyncSession, message: types.Message):
    """Удаление пользователя"""
    query = delete(User).where(User.user_id == message.from_user.id)
    await session.execute(query)
    await session.commit()
