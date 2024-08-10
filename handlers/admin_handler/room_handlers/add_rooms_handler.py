import logging
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.rooms_data import add_room
from keyboards.admin_keyboards.main_admin_keyboards import get_admin_keyboards
from keyboards.admin_keyboards.rooms_admin_keyboards import get_rooms_button, stopping_photo_upload_keyboard
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
    await message.answer("Добавьте фото номера (до 5 фотографий)")


@admin_room_router.message(F.photo, AddRoomsState.photo)
async def add_photo_room(message: types.Message, state: FSMContext, session: AsyncSession) -> None:
    # Получаем текущий список фотографий из состояния или создаём новый, если его нет
    data = await state.get_data()
    photos = data.get("photos", [])

    # Добавляем новое фото в список
    photos.append(message.photo[-1].file_id)

    # Обновляем данные в состоянии
    await state.update_data(photos=photos)

    # Если это было последнее фото, завершаем состояние и сохраняем данные
    if len(photos) >= 5:  # Например, если ожидается 3 фото, проверяем количество
        await add_room(
            title_room=data.get("title"),
            description_room=data.get("description"),
            photo_room=photos,  # Передаём список фотографий
            session=session
        )
        await state.clear()  # Очищаем состояние
        await message.answer(f"Номер {data.get('title')} добавлен!", reply_markup=await get_admin_keyboards())
    else:
        await message.answer("Добавьте ещё фото или завершите добавление номера нажав на кнопку ниже",
                             reply_markup=await stopping_photo_upload_keyboard())


@admin_room_router.message(~F.photo, AddRoomsState.photo)
async def add_incorrect_photo(message: types.Message, state: FSMContext) -> None:
    await message.answer(
        f"{message.from_user.first_name}\n"
        "Нужно загрузить фотографию!"
    )


@admin_room_router.callback_query(F.data == "stop_photo")
async def stopping_photo_upload(callback_data: types.CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    data = await state.get_data()
    photos = data.get("photos", [])
    await add_room(
        title_room=data.get("title"),
        description_room=data.get("description"),
        photo_room=photos,  # Передаём список фотографий
        session=session
    )
    await state.clear()  # Очищаем состояние
    await callback_data.message.answer(f"Номер {data.get('title')} добавлен!",
                                       reply_markup=await get_admin_keyboards())
    await callback_data.answer()
