from aiogram import Router, F, types

from handlers.users.uz.start import uz_start_buttons
from keyboards.inline.buttons import battle_ibuttons, battle_main_ibuttons, BattleCallback
from loader import bot

router = Router()


@router.message(F.text == "⚔️ Bellashuv")
async def uz_battle_main(message: types.Message):
    await message.answer(
        text="Savollar beriladigan kitob nomini tanlang",
        reply_markup=await battle_main_ibuttons(
            back_text="Ortga", back_callback="uz_back_battle_main"
        )
    )


@router.callback_query(F.data.contains("table_"))
async def get_book_name(call: types.CallbackQuery):

    book_name = call.data

    await call.message.edit_text(
        text="Bellashuv turini tanlang", reply_markup=battle_ibuttons(
            random_opponent="Tasodifiy raqib bilan", offer_opponent="Raqib taklif qilish",
            playing_alone="Yakka o'yin", alone_callback="uz_alone",
            back="Ortga", back_callback="uz_back", book_name=book_name
        )
    )


@router.callback_query(F.data.contains("book_name_"))
async def get_random_in_battle(call: types.CallbackQuery):
    print(call.data)


@router.callback_query(F.data == "uz_back")
async def uz_back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )

