from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from handlers.users.start import uz_start_buttons
from keyboards.inline.buttons import battle_ibuttons, battle_main_ibuttons
from loader import db

router = Router()


async def result_time_game(start_time, end_time):
    """
    O'yin boshlangan va tugagan vaqtni qabul qilib oradagi
    farqni chiqaruvchi funksiya
    """
    difference = end_time - start_time
    return difference


# @router.message(F.poll)
# async def m_mes(message: types.Message):
#     # print(message.poll)
#     question = message.poll.question.split("\n\n")[0]
#     a = message.poll.options[0].text
#     b = message.poll.options[1].text
#     c = message.poll.options[2].text
#     d = "Bilmayman"
#     await db.add_question(
#         table_name="table_3", question=question, a_correct=a, b=b, c=c, d=d
#     )
#     print("qo'shildi!")


@router.message(F.text == "⚔️ Bellashuv")
async def uz_battle_main(state: FSMContext, message: types.Message = None, call: types.CallbackQuery = None):
    await state.clear()
    telegram_id = str()
    if message:
        telegram_id = message.from_user.id
    if call:
        telegram_id = call.from_user.id

    # Users jadvalidan game_on ustunini FALSE holatiga tushirish
    await db.edit_status_users(
        game_on=False, telegram_id=telegram_id
    )
    # Results jadvalidan user ma'lumotlarini tozalash
    await db.delete_from_results(
        telegram_id=telegram_id
    )
    # Temporary answers jadvalidan user ma'lumotlarini tozalash
    await db.delete_from_temporary(
        telegram_id=telegram_id
    )
    # Counter jadvalidan hisoblagichni tozalash
    await db.delete_from_counter(
        telegram_id=telegram_id
    )
    if message:
        await message.answer(
            text="Savollar beriladigan kitob nomini tanlang",
            reply_markup=await battle_main_ibuttons(
                back_text="Ortga", back_callback="back_battle_main"
            )
        )
    if call:
        await call.message.edit_text(
            text="Savollar beriladigan kitob nomini tanlang",
            reply_markup=await battle_main_ibuttons(
                back_text="Ortga", back_callback="back_battle_main"
            )
        )


@router.callback_query(F.data.startswith("table_"))
async def get_book_name(call: types.CallbackQuery):
    book_id = call.data.split("_")[1]
    await call.message.edit_text(
        text="Bellashuv turini tanlang", reply_markup=battle_ibuttons(
            random_opponent="Tasodifiy raqib bilan", offer_opponent="Do'stni taklif qilish",
            playing_alone="Yakka o'yin", back="Ortga", back_callback="back_select_book", book_id=book_id
        )
    )


@router.callback_query(F.data == "back_battle_main")
async def uz_back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )


@router.callback_query(F.data == "back_select_book")
async def uz_back_books(call: types.CallbackQuery):
    await uz_battle_main(
        call=call
    )
