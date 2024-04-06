import asyncio

from aiogram import Router, F, types

from data.config import GROUP_ID
from keyboards.inline.buttons import to_offer_ibuttons, OfferCallback
from loader import db, bot

router = Router()


@router.callback_query(F.data == "uz_random_opponent")
async def uz_random_opponent(call: types.CallbackQuery):
    user_id = call.from_user.id
    full_name = call.from_user.full_name
    markup = to_offer_ibuttons(
        accedence_text="Qabul qilish", accedence_callback=str(user_id), theme="mavzu",
        cancel_text="Rad qilish"
    )
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

    random_user = await db.select_user_random()

    if random_user['telegram_id'] == user_id:
        other_random = await db.select_user_random()

        while other_random['telegram_id'] == random_user['telegram_id']:
            other_random = await db.select_user_random()

        await bot.send_message(
            chat_id=other_random['telegram_id'],
            text=f"Sizni {full_name} bellashuvga taklif qilmoqda!",
            reply_markup=markup
        )
    else:
        await bot.send_message(
            chat_id=random_user['telegram_id'],
            text=f"Sizni {full_name} bellashuvga taklif qilmoqda!",
            reply_markup=markup
        )
    await call.answer(
        text="Raqibingizga bellashuv haqidagi taklifingizni yuborildi!"
    )
    for n in numbers:
        await asyncio.sleep(1)
        await call.message.edit_text(
            text=f"{n}..."
        )
    await call.message.edit_text(
        text="Raqibingizdan javob kelmasa qayta <b>Tasodifiy raqib bilan</b> tugmasini bosing!"
    )


@router.callback_query(OfferCallback.filter())
async def get_opponent(query: types.CallbackQuery, callback_data: OfferCallback):
    opponent_id = callback_data.recipient_id
    theme = callback_data.theme
