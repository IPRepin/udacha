import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.rooms_data import update_room
from keyboards.admin_keyboards.main_admin_keyboards import get_admin_keyboards
from keyboards.user_keyboards.rooms_keyboards import add_rooms_menu, RoomsKeyboards
from utils.states import EditRoomState

edit_room_router = Router()
logger = logging.getLogger(__name__)


@edit_room_router.callback_query(F.data == "edit_room")
async def choosing_room(callback_query: types.CallbackQuery,
                        state: FSMContext,
                        session: AsyncSession) -> None:
    await state.set_state(EditRoomState.room)
    await callback_query.message.answer("Выбор номера для редактирования",
                                        reply_markup=await add_rooms_menu(session))
    await callback_query.answer()


@edit_room_router.callback_query(EditRoomState.room, RoomsKeyboards.filter())
async def edit_name_room(callback_query: types.CallbackQuery,
                         state: FSMContext, callback_data: RoomsKeyboards,
                         ) -> None:
    room_id = int(callback_data.action)
    await state.update_data(room_id=room_id)
    await callback_query.message.answer("Введите новое название номера")
    await callback_query.answer()
    await state.set_state(EditRoomState.title)


@edit_room_router.message(EditRoomState.title)
async def edit_description_room(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите новое описание номера")
    await state.set_state(EditRoomState.description)


@edit_room_router.message(EditRoomState.description)
async def edit_photo_room(message: types.Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await message.answer("Довьте фото номера")
    await state.set_state(EditRoomState.photo)


@edit_room_router.message(F.photo, EditRoomState.photo)
async def add_edited_room(message: types.Message,
                          state: FSMContext,
                          session: AsyncSession) -> None:
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    await state.clear()
    await update_room(
        session=session,
        id_room=data.get("room_id"),
        title_room=data.get("title"),
        description_room=data.get("description"),
        photo_room=data.get("photo")
    )
    logger.info(f"Номер {data.get('title')} обновлен!")
    await message.answer(f"Номер {data.get('title')} обновлен", reply_markup=await get_admin_keyboards())


@edit_room_router.message(~F.photo, EditRoomState.photo)
async def add_incorrect_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )