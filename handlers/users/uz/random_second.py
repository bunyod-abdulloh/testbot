import random

from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.inline.buttons import OfferCallback, play_battle_ibuttons
from loader import db, bot

router = Router()


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
                text=f"{letter}", callback_data=f"question_second:{callback[0]}:{book_id}:{battle_id}"
            )
        )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(OfferCallback.filter())
async def get_opponent(call: types.CallbackQuery, callback_data: OfferCallback, state: FSMContext):
    first_player = callback_data.agree_id
    book_id = callback_data.book_id
    fullname = call.from_user.full_name
    second_player = call.from_user.id
    book_name = await db.select_book_by_id(id_=book_id)
    id_ = await db.add_answer_first(first_player=first_player)
    battle_id = id_[0]
    try:
        print("trying to")
        await db.update_game_status_second(game_status="ONNO", second_player=second_player)
    except Exception as err:
        print(err)
    print(f"Game status updated {second_player}")
    await bot.send_message(
        chat_id=first_player,
        text=f"Foydalanuvchi {fullname} {book_name['table_name']} kitobi bo'yicha bellashuvga rozilik bildirdi!",
        reply_markup=play_battle_ibuttons(
            start_text="Boshlash", user_id=second_player, book_id=book_id, battle_id=battle_id
        )
    )
    counter = 1
    await state.update_data(c=counter)

    await generate_question_second(
        book_id=book_id, counter=counter, call=call, battle_id=battle_id
    )


@router.callback_query(F.data.startswith("question_second:"))
async def get_question_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c']
    answer = call.data.split(":")[1]
    book_id = call.data.split(":")[2]
    battle_id = int(call.data.split(":")[3])
    second_player = call.from_user.id

    if c == 10:

        if answer == "a":
            await db.add_answer_second(
                second_player=second_player, battle_id=battle_id, question_number=c, answer="✅"
            )
        else:
            await db.add_answer_second(
                second_player=second_player, battle_id=battle_id, question_number=c, answer="❌"
            )

        await db.update_game_status_second(game_status="OVER", second_player=second_player)

        answer_number = str()
        answer_emoji = str()
        numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

        for number in numbers:
            answer_number += f"{number} "
        print(f"{answer} 105")
        # if opponent_results['game_over'] and user_results['game_over'] is True:
        #
        #     first_player = await db.select_answers_user(telegram_id=user_id)
        #     second_player = await db.select_answers_user(telegram_id=opponent_id)
        #     first_result = str()
        #     second_result = str()

        # else:
        #     for result in user_results:
        #         answer_emoji += f"{result['correct_answer']} "
        #
        #     await call.message.edit_text(
        #         text=f"Savollar tugadi!\n\nSizning natijangiz:\n\n"
        #              f"{answer_number}\n\n{answer_emoji}\n\n"
        #              f"Raqibingiz hozircha o'yinni yakunlamadi! Yakunlagach raqibingizni ham natijalari"
        #              f"yuboriladi!"
        #     )

        await state.clear()

    else:
        c += 1
        await generate_question_second(
            book_id=book_id, counter=c, call=call, battle_id=battle_id
        )

        await state.update_data(
            c=c
        )

        if answer == "a":
            await db.add_answer_second(
                second_player=second_player, battle_id=battle_id, question_number=c - 1, answer="✅"
            )
        else:
            await db.add_answer_second(
                second_player=second_player, battle_id=battle_id, question_number=c - 1, answer="❌"
            )