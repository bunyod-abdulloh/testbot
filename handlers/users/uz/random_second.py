import asyncio
import random

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.buttons import OfferCallback, play_battle_ibuttons
from loader import db, bot

router = Router()


async def countdown_timer(seconds, call: types.CallbackQuery):
    while seconds > 0:
        await call.message.edit_text(
            text=f"Qolgan vaqt: 00:{seconds}"
        )
        await asyncio.sleep(1)
        seconds -= 1
    await call.message.edit_text(
        text="O'yin uchun ajratilgan vaqt tugadi!"
    )


async def generate_question_second(book_id, counter, call: types.CallbackQuery, battle_id):
    questions = await db.select_all_questions(table_name=f"table_{book_id}")

    letters = ["A", "B", "C", "D"]

    a = ["a", f"{questions[0][2]}"]
    b = ["b", f"{questions[0][3]}"]
    c = ["c", f"{questions[0][4]}"]
    d = ["d", f"{questions[0][5]}"]

    answers = [a, b, c, d]

    random.shuffle(answers)

    answers_dict = dict(zip(letters, answers))

    questions_text = str()

    for letter, question in answers_dict.items():
        questions_text += f"{letter}) {question[1]}\n"

    builder = InlineKeyboardBuilder()
    for letter, callback in answers_dict.items():
        builder.add(
            types.InlineKeyboardButton(
                text=f"{letter}", callback_data=f"second_player:{callback[0]}:{book_id}:{battle_id}"
            )
        )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}/10. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )

    # for n in range(59):
    #     await asyncio.sleep(1)
    #     await call.message.edit_text(
    #         text=f"00:{n}"
    #     )
    # await call.message.answer(
    #     text="O'yin boshlandi!"
    # )
    # seconds = 60
    # while seconds > 0:
    #     await call.message.edit_text(
    #         text=f"Qolgan vaqt: 00:{seconds}"
    #     )
    #     await asyncio.sleep(1)
    #     seconds -= 1
    # await call.message.edit_text(
    #     text="O'yin uchun ajratilgan vaqt tugadi!"
    # )


def send_result(results, first_text=None, second_text=None, first_player=False, second_player=False):
    answer_number = str()
    answer_emoji = str()
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    for number in numbers:
        answer_number += f"{number} "

    for result in results:
        answer_emoji += f"{result['answer']} "

    if first_player:
        first_send = f"{first_text}:\n\n{answer_number}\n\n{answer_emoji}\n\n"
        return first_send
    if second_player:
        second_send = f"{second_text}:\n\n{answer_number}\n\n{answer_emoji}\n\n"
        return second_send


async def question_answer_function(call: types.CallbackQuery, answer: str, state: FSMContext, c: str):
    book_id = int(call.data.split(":")[2])
    battle_id = int(call.data.split(":")[3])
    player_id = call.from_user.id
    book_name = await db.select_book_by_id(
        id_=book_id
    )

    if c == 10:
        await db.add_answer_(
            telegram_id=player_id, battle_id=battle_id, question_number=c, answer=answer, game_status="OVER"
        )
        second_answers = await db.count_answers(
            telegram_id=player_id, answer="✅"
        )
        second_answers_ = await db.count_answers(
            telegram_id=player_id, answer="❌"
        )
        await db.update_all_game_status(
            game_status="OVER", telegram_id=player_id, battle_id=battle_id
        )
        first_battler = await db.get_battle(
            battle_id=battle_id, telegram_id=player_id
        )
        second_results = await db.select_player(
            telegram_id=player_id
        )
        # second_send = send_result(
        #     results=second_results, first_text=first_text, first_player=True
        # )
        bot_opponent_result = send_result(
            results=second_results, second_text="Raqibingiz natijasi", second_player=True
        )
        first_text = (f"<b><i>Bellashuv natijalari</i></b>\n\n<i><b>Kitob nomi:</b>{book_name['table_name']}</i>"
                      f"<i><b>Savollar soni:</b>10 ta</i>\n\n😊 <i><b>Sizning natijangiz:</b></i>"
                      f"\n\n✅ <i><b>To'g'ri javob:</b>{second_answers} ta</i>"
                      f"\n\n❌ <i><b>Noto'g'ri javob:</b>{second_answers_} ta</i>"
                      f"\n\n⏳ <i><b>Sarflangan vaqt:</b></i>"
                      f"\n\n📖 <i><b>Kitob bo'yicha reyting:</b></i>"
                      f"\n\n📚 <i><b>Umumiy reyting:</b></i>")
        if not first_battler:
            await call.message.edit_text(
                text=f"{second_send}"
                     f"Raqibingiz hali o'yinni boshlamadi! O'yinni boshlaganidan so'ng raqibingiz natijalari ham "
                     f"yuboriladi!"
            )
            await db.edit_status_users(
                game_on=False, telegram_id=player_id
            )
        else:
            player_id_ = first_battler[0]['telegram_id']
            first_results = await db.select_player(
                telegram_id=player_id_
            )
            first_send = send_result(
                results=first_results, second_text="Raqibingiz natijasi", second_player=True
            )
            bot_your_result = send_result(
                results=first_results, first_text=first_text, first_player=True
            )
            if first_battler[0]['game_status'] == "ON":
                await call.message.edit_text(
                    text=f"{second_send}"
                         f"Raqibingiz hali o'yinni tugatmadi! Tugatganidan so'ng raqibingiz natijalari ham yuboriladi!"
                )
                await db.edit_status_users(
                    game_on=False, telegram_id=player_id
                )
            else:
                await call.message.edit_text(
                    text=f"{second_send}\n{first_send}"
                )
                await bot.send_message(
                    chat_id=player_id_,
                    text=f"{bot_your_result}\n{bot_opponent_result}"
                )
                first_answers = await db.count_answers(
                    telegram_id=player_id_, answer=answer
                )
                await db.update_results(
                    results=first_answers, book_id=book_id, telegram_id=player_id_
                )
                await db.update_results(
                    results=second_answers, book_id=book_id, telegram_id=player_id
                )
                # Temporary jadvalni tozalash
                await db.clean_temporary_table(
                    battle_id=battle_id
                )
                # Users jadvalidan o'yinchilar game on ustunini FALSE holatiga keltirish
                await db.edit_status_users(
                    game_on=False, telegram_id=player_id
                )
                await db.edit_status_users(
                    game_on=False, telegram_id=player_id_
                )
        await state.clear()
    else:
        c += 1
        await generate_question_second(
            book_id=book_id, counter=c, call=call, battle_id=battle_id
        )
        await state.update_data(
            c_two=c
        )
        await db.add_answer_(
            telegram_id=player_id, battle_id=battle_id, question_number=int(c) - 1, answer=answer, game_status="ON"
        )


@router.callback_query(OfferCallback.filter())
async def get_opponent(call: types.CallbackQuery, callback_data: OfferCallback, state: FSMContext):
    first_player_id = callback_data.agree_id
    second_player_id = call.from_user.id
    book_id = callback_data.book_id
    fullname = call.from_user.full_name

    book_name = await db.select_book_by_id(
        id_=book_id
    )
    # Temporary jadvaliga user ma'lumotlarini qo'shib battle idsini olish
    id_ = await db.add_answer(
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
    await state.update_data(
        c_two=c_two
    )
    # Users jadvalida userga game_on yoqish
    await db.edit_status_users(
        game_on=True, telegram_id=second_player_id
    )
    await generate_question_second(
        book_id=book_id, counter=c_two, call=call, battle_id=battle_id
    )
    # Results jadvaliga userni qo'shish
    await db.add_gamer(
        telegram_id=second_player_id, book_id=book_id
    )


@router.callback_query(F.data.startswith("second_player:a"))
async def get_question_answer_a(call: types.CallbackQuery, state: FSMContext):
    data = await state.update_data()
    c = data['c_two']
    await question_answer_function(
        call=call, answer="✅", state=state, c=c
    )


second_answer_filter = (F.data.startswith("second_player:b") | F.data.startswith("second_player:c") |
                        F.data.startswith("second_player:d"))


@router.callback_query(second_answer_filter)
async def get_question_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.update_data()
    c = data['c_two']
    await question_answer_function(
        call=call, answer="❌", state=state, c=c
    )
