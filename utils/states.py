from aiogram.fsm.state import State, StatesGroup


class BookRoomState(StatesGroup):
    starting_date = State()
    finishing_date = State()
    number_guests = State()
    room = State()


class AddRoomsState(StatesGroup):
    title = State()
    description = State()
    photo = State()


class UserIdState(StatesGroup):
    USER_ID = State()

