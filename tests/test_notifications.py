import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from data.models import Booking, User
from utils.notifications import (
    send_notification,
    check_upcoming_bookings,
    check_checkout_reminders,
    send_booking_reminder,
    send_checkout_reminder,
    send_feedback_request
)


@pytest.mark.asyncio
async def test_send_notification(bot):
    """Test send_notification function"""
    user_id = 123456789
    message = "Test message"
    
    # Mock bot.send_message
    bot.send_message = AsyncMock()
    
    await send_notification(bot, user_id, message)
    
    # Check if bot.send_message was called with correct parameters
    bot.send_message.assert_called_once_with(
        chat_id=user_id,
        text=message
    )


@pytest.mark.asyncio
async def test_check_upcoming_bookings(db_session: AsyncSession, test_booking: Booking):
    """Test check_upcoming_bookings function"""
    # Modify check_in_date to be within next 24 hours
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_booking.check_in_date = tomorrow
    test_booking.status = "Подтверждено"
    await db_session.commit()
    
    bookings = await check_upcoming_bookings(db_session)
    assert len(bookings) == 1
    assert bookings[0].id == test_booking.id


@pytest.mark.asyncio
async def test_check_checkout_reminders(db_session: AsyncSession, test_booking: Booking):
    """Test check_checkout_reminders function"""
    # Modify departure_date to be within next 24 hours
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_booking.departure_date = tomorrow
    test_booking.status = "Подтверждено"
    await db_session.commit()
    
    bookings = await check_checkout_reminders(db_session)
    assert len(bookings) == 1
    assert bookings[0].id == test_booking.id


@pytest.mark.asyncio
async def test_send_booking_reminder(bot, db_session: AsyncSession, test_booking: Booking):
    """Test send_booking_reminder function"""
    # Modify check_in_date to be within next 24 hours
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_booking.check_in_date = tomorrow
    test_booking.status = "Подтверждено"
    await db_session.commit()
    
    # Mock send_notification
    with patch('utils.notifications.send_notification') as mock_send:
        mock_send.return_value = None
        
        await send_booking_reminder(bot, db_session)
        
        # Check if send_notification was called
        assert mock_send.called
        # Get the call arguments
        args = mock_send.call_args[0]
        # Check if bot instance was passed
        assert args[0] == bot
        # Check if user_id was passed
        assert args[1] == test_booking.user_id
        # Check if message contains booking details
        assert test_booking.room in args[2]
        assert test_booking.check_in_date in args[2]
        assert test_booking.departure_date in args[2]
        assert str(test_booking.guests) in args[2]


@pytest.mark.asyncio
async def test_send_checkout_reminder(bot, db_session: AsyncSession, test_booking: Booking):
    """Test send_checkout_reminder function"""
    # Modify departure_date to be within next 24 hours
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_booking.departure_date = tomorrow
    test_booking.status = "Подтверждено"
    await db_session.commit()
    
    # Mock send_notification
    with patch('utils.notifications.send_notification') as mock_send:
        mock_send.return_value = None
        
        await send_checkout_reminder(bot, db_session)
        
        # Check if send_notification was called
        assert mock_send.called
        # Get the call arguments
        args = mock_send.call_args[0]
        # Check if bot instance was passed
        assert args[0] == bot
        # Check if user_id was passed
        assert args[1] == test_booking.user_id
        # Check if message contains booking details
        assert test_booking.departure_date in args[2]


@pytest.mark.asyncio
async def test_send_feedback_request(bot, db_session: AsyncSession, test_booking: Booking):
    """Test send_feedback_request function"""
    # Modify departure_date to be yesterday
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    test_booking.departure_date = yesterday
    test_booking.status = "Подтверждено"
    await db_session.commit()
    
    # Mock send_notification
    with patch('utils.notifications.send_notification') as mock_send:
        mock_send.return_value = None
        
        await send_feedback_request(bot, db_session)
        
        # Check if send_notification was called
        assert mock_send.called
        # Get the call arguments
        args = mock_send.call_args[0]
        # Check if bot instance was passed
        assert args[0] == bot
        # Check if user_id was passed
        assert args[1] == test_booking.user_id
        # Check if message contains feedback request
        assert "отзыв" in args[2]
        assert "/feedback" in args[2]
