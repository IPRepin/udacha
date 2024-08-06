import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.rooms_data import add_room
from keyboards.admin_keyboards.main_admin_keyboards import get_admin_keyboards
from keyboards.admin_keyboards.rooms_admin_keyboards import get_rooms_button
from utils.states import AddRoomsState

admin_room_router = Router()
logger = logging.getLogger(__name__)


@admin_room_router.message(F.text == "Номера")
async def working_rooms(message: types.Message) -> None:
    await message.answer("Для добавления, редактирования или "
                         "удаления номера выберете один из слудующих "
                         "пунктов меню:", reply_markup=await get_rooms_button())


@admin_room_router.callback_query(F.data == "add_room")
async def add_new_room(callback: types.CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AddRoomsState.title)
    await callback.message.answer("Напишите название номера")
    await callback.answer()


@admin_room_router.message(AddRoomsState.title)
async def add_title_room(message: types.Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.set_state(AddRoomsState.description)
    await message.answer("Добавьте описание номера")


@admin_room_router.message(AddRoomsState.description)
async def add_description_room(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddRoomsState.photo)
    await message.answer("Добавьте фото номера")


@admin_room_router.message(F.photo, AddRoomsState.photo)
async def add_photo_room(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    await state.update_data(photo=message.photo[-1].file_id)
    data = await state.get_data()
    await state.clear()
    await add_room(
        title_room=data.get("title"),
        description_room=data.get("description"),
        photo_room=data.get("photo"),
        session=session
    )
    await message.answer(f"Номер {data.get('title')} добавлен!", reply_markup=await get_admin_keyboards())


@admin_room_router.message(~F.photo, AddRoomsState.photo)
async def add_incorrect_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )
