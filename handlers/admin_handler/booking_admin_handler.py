import logging
from aiogram import types, Router, F, Bot
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.booking_data import get_booking_by_params, update_booking_status
from keyboards.admin_keyboards.booking_admin_keyboards import get_booking_admin_keyboards, send_user_keyboard, \
    add_moderation_keyboard
from utils.states import UserIdState
from utils.texts import moderator_text

booking_admin_router = Router()
logger = logging.getLogger(__name__)


@booking_admin_router.message(F.text == "Бронирования")
async def working_with_bookings(message: types.Message) -> None:
    await message.answer("Выберете одно из действий ниже",
                         reply_markup=await get_booking_admin_keyboards())


@booking_admin_router.message(F.text == "Проверить заявки на бронирования")
async def next_moderation_questionnaires(message: types.Message,
                                         state: FSMContext,
                                         session: AsyncSession,
                                         ) -> None:
    try:
        logger.info("next_moderation_booking")
        booking = await get_booking_by_params(session, status="❌Не подтверждено")
        if booking:
            await state.set_state(UserIdState.USER_ID)
            await state.update_data(user_id=int(booking.user_id))
            await message.answer(moderator_text(booking),
                                 reply_markup=await add_moderation_keyboard())
        else:
            await message.answer("😎Все заявки проверены!")
    except TelegramNetworkError as telegram_err:
        logger.error(telegram_err)


@booking_admin_router.callback_query(F.data.in_(['approved', 'rejected']), UserIdState.USER_ID)
async def moderation_booking(callback_query: types.CallbackQuery,
                             state: FSMContext,
                             session: AsyncSession,
                             bot: Bot):
    data = await state.get_data()
    await state.clear()
    user_id = data.get('user_id')
    logger.info("Moderation booking started")
    booking = await get_booking_by_params(session, user_id=user_id)
    if callback_query.data == 'approved' and booking:
        await update_booking_status(session=session, status="Бронирование подтверждено", user_id=user_id)
        await callback_query.message.answer("✅Бронирование одобрено, пользователю отправлено"
                                            "уведомление о результате проверки",
                                            reply_markup=await send_user_keyboard(user_url=booking.user_url))
        await callback_query.answer()
        await bot.send_message(chat_id=user_id, text="✅Бронирование одобрено")
    elif callback_query.data == 'rejected' and booking:
        await update_booking_status(session=session, status="Бронирование отклонено", user_id=user_id)
        await callback_query.message.answer("🚫Бронирование отклонено, пользователю отправлено"
                                            "уведомление о результате проверки",
                                            reply_markup=await send_user_keyboard(user_url=booking.user_url))
        await bot.send_message(chat_id=user_id,
                               text="🚫Бронирование отклонено")
        await callback_query.answer()
