import asyncio
import logging
from datetime import datetime
from typing import Any, Awaitable, Callable

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from utils.notifications import (
    send_booking_reminder,
    send_checkout_reminder,
    send_feedback_request
)

logger = logging.getLogger(__name__)


class NotificationScheduler:
    def __init__(self, bot: Bot, session_maker: Callable[..., AsyncSession]):
        self.bot = bot
        self.session_maker = session_maker
        self.tasks = []
        self.is_running = False

    async def schedule_task(
            self,
            func: Callable[..., Awaitable[Any]],
            interval_seconds: int
    ) -> None:
        """Планирование периодического выполнения задачи"""
        while self.is_running:
            try:
                async with self.session_maker() as session:
                    await func(self.bot, session)
            except Exception as e:
                logger.error(f"Error in scheduled task {func.__name__}: {e}")
            
            await asyncio.sleep(interval_seconds)

    async def start(self) -> None:
        """Запуск планировщика"""
        self.is_running = True
        
        # Проверка предстоящих заездов каждый час
        self.tasks.append(
            asyncio.create_task(
                self.schedule_task(send_booking_reminder, 3600)
            )
        )
        
        # Проверка предстоящих выездов каждый час
        self.tasks.append(
            asyncio.create_task(
                self.schedule_task(send_checkout_reminder, 3600)
            )
        )
        
        # Запрос отзывов каждые 12 часов
        self.tasks.append(
            asyncio.create_task(
                self.schedule_task(send_feedback_request, 43200)
            )
        )

        logger.info(f"Notification scheduler started at {datetime.now()}")

    async def stop(self) -> None:
        """Остановка планировщика"""
        self.is_running = False
        for task in self.tasks:
            task.cancel()
        
        await asyncio.gather(*self.tasks, return_exceptions=True)
        self.tasks.clear()
        logger.info(f"Notification scheduler stopped at {datetime.now()}")
