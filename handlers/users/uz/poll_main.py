import asyncio

from aiogram import Router, F, types

from handlers.users.uz.start import uz_start_buttons
from keyboards.inline.buttons import battle_ibuttons, battle_main_ibuttons, BattleCallback, to_offer_ibuttons, \
    OfferCallback
from loader import bot, db

router = Router()


@router.message(F.text == "⚔️ Bellashuv")
async def uz_battle_main(message: types.Message):
    await message.answer(
        text="Savollar beriladigan kitob nomini tanlang",
        reply_markup=await battle_main_ibuttons(
            back_text="Ortga", back_callback="uz_back_battle_main"
        )
    )


@router.callback_query(F.data.startswith("table_"))
async def get_book_name(call: types.CallbackQuery):

    book_id = call.data.split("_")[1]
    await call.message.edit_text(
        text="Bellashuv turini tanlang", reply_markup=battle_ibuttons(
            random_opponent="Tasodifiy raqib bilan", offer_opponent="Raqib taklif qilish",
            playing_alone="Yakka o'yin", alone_callback="uz_alone",
            back="Ortga", back_callback="uz_back", book_id=book_id
        )
    )


@router.callback_query(F.data.startswith("book_id:"))
async def get_random_in_battle(call: types.CallbackQuery):
    book_id = call.data.split(':')[1]
    book_name = f"table_{book_id}"
    user_id = call.from_user.id

    full_name = call.from_user.full_name
    markup = to_offer_ibuttons(
        agree_text="Qabul qilish", agree_id=user_id, refusal_text="Rad qilish", book_id=book_id
    )
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

    random_user = await db.select_user_random()

    if random_user['telegram_id'] == user_id:
        other_random = await db.select_user_random()

        while other_random['telegram_id'] == random_user['telegram_id']:
            other_random = await db.select_user_random()

        await bot.send_message(
            chat_id=other_random['telegram_id'],
            text=f"Foydalanuvchi {full_name} Sizni {book_name} kitobi bo'yicha bellashuvga taklif qilmoqda!",
            reply_markup=markup
        )
    else:
        await bot.send_message(
            chat_id=random_user['telegram_id'],
            text=f"Foydalanuvchi {full_name} Sizni {book_name} kitobi bo'yicha bellashuvga taklif qilmoqda!",
            reply_markup=markup
        )
    await call.answer(
        text="Raqibingizga bellashuv taklifi yuborildi!"
    )
    for n in numbers:
        await call.message.edit_text(
            text=f"{n}"
        )
        await asyncio.sleep(1)
    await call.message.edit_text(
        text="Raqibingizdan javob kelmasa qayta <b>Tasodifiy raqib bilan</b> tugmasini bosing!"
    )


@router.callback_query(OfferCallback.filter())
async def get_opponent(query: types.CallbackQuery, callback_data: OfferCallback):
    print(callback_data)
    opponent_id = callback_data.agree_id



@router.callback_query(F.data == "uz_back")
async def uz_back(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )

