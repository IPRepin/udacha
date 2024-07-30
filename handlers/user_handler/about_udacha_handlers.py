from aiogram import Router, F, types

from utils.texts import about_us

about_router = Router()


@about_router.message(F.text == "👋О гостевом доме УДАЧА")
async def get_info_udacha(message: types.Message):
    await message.answer_photo(photo="https://telegra.ph/file/15b6b2d0265dffa8afab1.jpg",
                               caption=about_us
    )