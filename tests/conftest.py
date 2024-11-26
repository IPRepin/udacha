import asyncio
from datetime import datetime, timedelta
from typing import AsyncGenerator, Generator
import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from data.models import BaseModelBot as Base, User, Room, Booking
from tests.test_config import test_settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create event loop for tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def db_engine():
    """Create engine for tests"""
    engine = create_async_engine(
        test_settings.DB_URL,
        poolclass=StaticPool,
        echo=False
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="session")
async def db_session_factory(db_engine):
    """Create session factory for tests"""
    async_session = sessionmaker(
        db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    return async_session


@pytest.fixture
async def db_session(db_session_factory) -> AsyncGenerator[AsyncSession, None]:
    """Create session for tests"""
    async with db_session_factory() as session:
        yield session
        # Clear the session after each test
        await session.rollback()
        await session.close()


@pytest.fixture
def user_id():
    """Generate unique user_id for tests"""
    return int(str(uuid.uuid4().int)[:9])


@pytest.fixture
async def test_user(db_session: AsyncSession, user_id: int) -> User:
    """Create test user"""
    user = User(
        user_id=user_id,
        user_first_name="Test",
        user_url="@test_user",
        booking_confirmation="❌Не подтверждено"
    )
    db_session.add(user)
    await db_session.commit()
    return user


@pytest.fixture
async def test_room(db_session: AsyncSession) -> Room:
    """Create test room"""
    room = Room(
        name="101",
        description="Test Room",
        photo=["test_photo.jpg"]
    )
    db_session.add(room)
    await db_session.commit()
    return room


@pytest.fixture
async def test_booking(db_session: AsyncSession, test_user: User, test_room: Room) -> Booking:
    """Create test booking"""
    booking = Booking(
        user_id=test_user.user_id,
        user_first_name=test_user.user_first_name,
        user_url=test_user.user_url,
        guests=2,
        room=test_room.name,
        check_in_date=datetime.now().strftime("%Y-%m-%d"),
        departure_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        status="Подтверждено"
    )
    db_session.add(booking)
    await db_session.commit()
    return booking


@pytest.fixture
async def bot() -> AsyncGenerator[Bot, None]:
    """Create bot instance for tests with test token"""
    # Use a properly formatted test token
    test_token = "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456789"
    bot = Bot(token=test_token, parse_mode="HTML")
    yield bot
    await bot.session.close()


@pytest.fixture
async def dp() -> AsyncGenerator[Dispatcher, None]:
    """Create dispatcher instance for tests"""
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    yield dp
    await dp.storage.close()
