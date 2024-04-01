from aiogram import Router, F, types

from loader import db, bot

router = Router()


@router.callback_query(F.data == "uz_random_opponent")
async def uz_random_opponent(call: types.CallbackQuery):
    pass


@router.message(F.text == "ran")
async def sampler(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    random_user = await db.select_user_random()

    if random_user['telegram_id'] == user_id:
        other_random = await db.select_user_random()

        while other_random['telegram_id'] == random_user['telegram_id']:
            other_random = await db.select_user_random()

        await bot.send_message(
            chat_id=other_random['telegram_id'],
            text=f"Sizni {full_name} bellashuvga taklif qilmoqda!"
        )

    else:
        print(random_user)

