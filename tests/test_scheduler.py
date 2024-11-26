import pytest
from unittest.mock import AsyncMock, patch

from utils.scheduler import NotificationScheduler


@pytest.mark.asyncio
async def test_scheduler_initialization(bot, db_session_factory):
    """Test scheduler initialization"""
    scheduler = NotificationScheduler(bot, db_session_factory)
    assert scheduler.bot == bot
    assert scheduler.session_maker == db_session_factory
    assert scheduler.tasks == []
    assert not scheduler.is_running


@pytest.mark.asyncio
async def test_scheduler_start_stop(bot, db_session_factory):
    """Test scheduler start and stop"""
    scheduler = NotificationScheduler(bot, db_session_factory)
    
    # Start scheduler
    await scheduler.start()
    assert scheduler.is_running
    assert len(scheduler.tasks) == 3  # Should have 3 tasks
    
    # Stop scheduler
    await scheduler.stop()
    assert not scheduler.is_running
    assert len(scheduler.tasks) == 0


@pytest.mark.asyncio
async def test_schedule_task(bot, db_session_factory):
    """Test schedule_task method"""
    scheduler = NotificationScheduler(bot, db_session_factory)
    
    # Create mock function
    mock_func = AsyncMock()
    
    # Start scheduler
    scheduler.is_running = True
    
    # Schedule task with very short interval
    with patch('asyncio.sleep', AsyncMock()) as mock_sleep:
        # Run schedule_task for a short time
        await scheduler.schedule_task(mock_func, 1)
        
        # Check if function was called
        assert mock_func.called
        # Check if sleep was called
        assert mock_sleep.called


@pytest.mark.asyncio
async def test_scheduler_error_handling(bot, db_session_factory):
    """Test scheduler error handling"""
    scheduler = NotificationScheduler(bot, db_session_factory)
    
    # Create mock function that raises an exception
    async def mock_func(*args):
        raise Exception("Test error")
    
    # Start scheduler
    scheduler.is_running = True
    
    # Schedule task with very short interval
    with patch('asyncio.sleep', AsyncMock()) as mock_sleep:
        # Run schedule_task for a short time
        await scheduler.schedule_task(mock_func, 1)
        
        # Check if sleep was called despite the error
        assert mock_sleep.called
