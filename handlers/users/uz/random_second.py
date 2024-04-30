from datetime import datetime

from aiogram import types, Router, F
from handlers.users.uz.random_first import send_result_or_continue, generate_question
from keyboards.inline.buttons import OfferCallback, play_battle_ibuttons
from loader import db, bot

router = Router()


@router.callback_query(OfferCallback.filter())
async def get_opponent(call: types.CallbackQuery, callback_data: OfferCallback):
    first_player_id = callback_data.agree_id
    second_player_id = call.from_user.id
    book_id = callback_data.book_id
    fullname = call.from_user.full_name

    book_name = await db.select_book_by_id(
        id_=book_id
    )
    # Temporary jadvaliga user ma'lumotlarini qo'shib battle idsini olish
    id_ = await db.add_battle_to_temporary(
        telegram_id=first_player_id
    )
    battle_id = id_[0]

    await bot.send_message(
        chat_id=first_player_id,
        text=f"Foydalanuvchi {fullname} {book_name['table_name']} kitobi bo'yicha bellashuvga rozilik bildirdi!",
        reply_markup=play_battle_ibuttons(
            start_text="Boshlash", book_id=book_id, battle_id=battle_id
        )
    )
    c_two = 1
    # Counter jadvaliga savol tartib raqamini kiritish
    await db.add_to_counter(
        telegram_id=second_player_id, battle_id=battle_id, counter=c_two
    )
    # Userni Results jadvalida bor yo'qligini tekshirish
    check_in_results = await db.select_user_in_results(
        telegram_id=second_player_id, book_id=book_id
    )
    if not check_in_results:
        # Results jadvaliga userni qo'shish
        await db.add_gamer(
            telegram_id=second_player_id, book_id=book_id
        )
    # Users jadvalida userga game_on yoqish
    await db.edit_status_users(
        game_on=True, telegram_id=second_player_id
    )
    await generate_question(
        book_id=book_id, counter=c_two, call=call, battle_id=battle_id, opponent=True
    )
    start_time = datetime.now()
    await db.start_time_to_temporary(
        telegram_id=second_player_id, battle_id=battle_id, game_status="ON", start_time=start_time
    )


@router.callback_query(F.data.startswith("s_question:a"))
async def get_question_answer_a(call: types.CallbackQuery):
    await send_result_or_continue(
        answer_emoji="✅", call=call, opponent=True
    )


second_answer_filter = (F.data.startswith("s_question:b") | F.data.startswith("s_question:c") |
                        F.data.startswith("s_question:d"))


@router.callback_query(second_answer_filter)
async def get_question_answer(call: types.CallbackQuery):
    await send_result_or_continue(
        answer_emoji="❌", call=call, opponent=True
    )
