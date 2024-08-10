import logging

from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession

from data.rooms_data import get_room_by_id
from keyboards.user_keyboards.rooms_keyboards import info_rooms_menu, InfoRoomsKeyboards, get_about_us_menu, \
    get_back_all_rooms_menu
from utils.texts import about_us

about_router = Router()
logger = logging.getLogger(__name__)


@about_router.message(F.text == "👋О гостевом доме УДАЧА")
async def get_info_udacha(message: types.Message):
    await message.answer_photo(photo="https://telegra.ph/file/d5f02c18c7163623d1870.jpg",
                               caption=about_us, reply_markup=await get_about_us_menu()
                               )


@about_router.callback_query(F.data.in_(['all_room_info', 'back_all_rooms']))
async def get_all_rooms(callback_query: types.CallbackQuery, session: AsyncSession) -> None:
    await callback_query.message.answer("Номера:", reply_markup=await info_rooms_menu(session))
    await callback_query.answer()


@about_router.callback_query(InfoRoomsKeyboards.filter())
async def get_info_rooms(callback_query: types.CallbackQuery, callback_data: InfoRoomsKeyboards,
                         session: AsyncSession):
    room_id = int(callback_data.action)
    room = await get_room_by_id(session, room_id)
    media_group = [types.InputMediaPhoto(media=photo) for photo in room.photo]
    await callback_query.message.answer_media_group(media_group)
    await callback_query.message.answer(f"{room.name}\n"
                                        f"{room.description}",
                                        reply_markup=await get_back_all_rooms_menu())
    await callback_query.answer()
