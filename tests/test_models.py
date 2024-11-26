import pytest
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import User, Room, Booking


@pytest.mark.asyncio
async def test_user_creation(db_session: AsyncSession):
    """Test user creation"""
    # Create user
    user = User(
        user_id=987654321,
        user_first_name="Test2",
        user_url="@test_user2",
        booking_confirmation="❌Не подтверждено"
    )
    db_session.add(user)
    await db_session.commit()
    
    # Query user
    query = select(User).where(User.user_id == 987654321)
    result = await db_session.execute(query)
    fetched_user = result.scalar_one()
    
    # Check user data
    assert fetched_user.user_first_name == "Test2"
    assert fetched_user.user_url == "@test_user2"
    assert fetched_user.booking_confirmation == "❌Не подтверждено"


@pytest.mark.asyncio
async def test_room_creation(db_session: AsyncSession):
    """Test room creation"""
    # Create room
    room = Room(
        name="102",
        description="Test Room 2",
        photo=["test_photo2.jpg"]
    )
    db_session.add(room)
    await db_session.commit()
    
    # Query room
    query = select(Room).where(Room.name == "102")
    result = await db_session.execute(query)
    fetched_room = result.scalar_one()
    
    # Check room data
    assert fetched_room.description == "Test Room 2"
    assert fetched_room.photo == ["test_photo2.jpg"]


@pytest.mark.asyncio
async def test_booking_creation(db_session: AsyncSession, test_user: User, test_room: Room):
    """Test booking creation"""
    # Create booking
    check_in = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    departure = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    
    booking = Booking(
        user_id=test_user.user_id,
        user_first_name=test_user.user_first_name,
        user_url=test_user.user_url,
        guests=2,
        room=test_room.name,
        check_in_date=check_in,
        departure_date=departure,
        status="Новое бронирование"
    )
    db_session.add(booking)
    await db_session.commit()
    
    # Query booking
    query = select(Booking).where(
        Booking.user_id == test_user.user_id,
        Booking.room == test_room.name
    )
    result = await db_session.execute(query)
    fetched_booking = result.scalar_one()
    
    # Check booking data
    assert fetched_booking.status == "Новое бронирование"
    assert fetched_booking.check_in_date == check_in
    assert fetched_booking.departure_date == departure
    assert fetched_booking.guests == 2


@pytest.mark.asyncio
async def test_booking_user_relationship(db_session: AsyncSession, test_booking: Booking):
    """Test booking-user relationship"""
    # Query booking
    query = select(Booking).where(Booking.id == test_booking.id)
    result = await db_session.execute(query)
    fetched_booking = result.scalar_one()
    
    # Check user data in booking
    assert fetched_booking.user_first_name == test_booking.user_first_name
    assert fetched_booking.user_url == test_booking.user_url
