from keyboards.user_keyboards.rooms_keyboards import rooms_menu
from utils.states import BookRoomState
from aiogram import types, Router, F
from aiogram_calendar import DialogCalendar, DialogCalendarCallback, \
    get_user_locale
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

user_handlers_router = Router()


@user_handlers_router.message(F.text == "🐬Забронировать номер")
async def book_a_room(message: types.Message, state: FSMContext):
    await message.answer("Дата начала поездки:",
                         reply_markup=await DialogCalendar(
                             locale=await get_user_locale(message.from_user)
                         ).start_calendar())
    await state.set_state(BookRoomState.starting_date)


@user_handlers_router.callback_query(DialogCalendarCallback.filter(), BookRoomState.starting_date)
async def add_start_date(callback_query: types.CallbackQuery, callback_data: CallbackData,
                         state: FSMContext
                         ):
    selected, date = await DialogCalendar(
        locale=await get_user_locale(callback_query.from_user)
    ).process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(start_date={date.strftime("%d.%m.%Y")})
        await callback_query.message.answer(f"{date.strftime('%d.%m.%Y')}")
        await state.set_state(BookRoomState.finishing_date)
        await callback_query.message.answer("Дата окончания поездки:",
                                            reply_markup=await DialogCalendar(
                                                locale=await get_user_locale(callback_query.from_user)
                                            ).start_calendar())


@user_handlers_router.callback_query(DialogCalendarCallback.filter(), BookRoomState.finishing_date)
async def add_finishing_date(callback_query: types.CallbackQuery, callback_data: CallbackData,
                             state: FSMContext
                             ):
    selected, date = await DialogCalendar(
        locale=await get_user_locale(callback_query.from_user)
    ).process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(finish_date={date.strftime("%d.%m.%Y")})
        await callback_query.message.answer(f"{date.strftime('%d.%m.%Y')}")
        await state.set_state(BookRoomState.number_guests)
        await callback_query.message.answer("Введите количество готей")


@user_handlers_router.message(BookRoomState.number_guests)
async def add_number_guests(message: types.Message, state: FSMContext):
    await state.update_data(number_guests=message.text)
    await state.set_state(BookRoomState.room)
    await message.answer("Номер для проживания", reply_markup=await rooms_menu())


@user_handlers_router.callback_query(BookRoomState.room)
async def select_room(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(room=callback_query.message.text)
    data = await state.get_data()
    await state.clear()
    await callback_query.message.answer(f"{callback_query.message.from_user.first_name} вы выбрали:\n"
                                        f"Дата заезда: {data.get('start_date')}\n"
                                        f"Дата выезда: {data.get('finish_date')}\n"
                                        f"{data.get('number_guests')} проживающих\n"
                                        f"Выбранный номер:  {data.get('room')}")
