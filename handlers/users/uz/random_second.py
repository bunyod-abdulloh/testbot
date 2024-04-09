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
                text=f"{letter}", callback_data=f"second_player:{callback[0]}:{book_id}:{battle_id}"
            )
        )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


def send_result(results):
    answer_number = str()
    answer_emoji = str()
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    for number in numbers:
        answer_number += f"{number} "

    for result in results:
        answer_emoji += f"{result['answer']} "

    send_message = f"Savollar tugadi!\n\nSizning natijangiz:\n\n{answer_number}\n\n{answer_emoji}\n\n"

    return send_message


@router.callback_query(OfferCallback.filter())
async def get_opponent(call: types.CallbackQuery, callback_data: OfferCallback, state: FSMContext):
    first_player = callback_data.agree_id
    book_id = callback_data.book_id
    fullname = call.from_user.full_name
    book_name = await db.select_book_by_id(
        id_=book_id
    )
    id_ = await db.add_answer_first(
        first_player=first_player
    )
    battle_id = id_[0]

    await bot.send_message(
        chat_id=first_player,
        text=f"Foydalanuvchi {fullname} {book_name['table_name']} kitobi bo'yicha bellashuvga rozilik bildirdi!",
        reply_markup=play_battle_ibuttons(
            start_text="Boshlash", book_id=book_id, battle_id=battle_id
        )
    )
    c_two = 1
    await state.update_data(
        c_two=c_two
    )
    await generate_question_second(
        book_id=book_id, counter=c_two, call=call, battle_id=battle_id
    )


@router.callback_query(F.data.startswith("second_player:a"))
async def get_question_answer_a(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_two']
    book_id = call.data.split(":")[2]
    battle_id = int(call.data.split(":")[3])
    second_player = call.from_user.id

    if c == 10:
        await db.add_answer_second(
            second_player=second_player, battle_id=battle_id, question_number=c, answer="✅", game_status="OVER"
        )

        second_results = await db.select_second_player(second_player=second_player)

        first_battler = await db.get_battle_first(
            battle_id=battle_id
        )
        second_message = send_result(
            results=second_results
        )
        if not first_battler:
            await call.message.edit_text(
                text=f"{second_message}"
                     f"Raqibingiz hali o'yinni boshlamadi! O'yinni boshlaganidan so'ng raqibingiz natijalari ham "
                     f"yuboriladi!"
            )
        else:
            print(first_battler)
            if first_battler['game_status'] == "ON":
                await call.message.edit_text(
                    text=f"{second_message}"
                         f"Raqibingiz hali o'yinni tugatmadi! Tugatganidan so'ng raqibingiz natijalari ham yuboriladi!"
                )
            else:
                print("saom")
        await state.clear()
    else:
        c += 1
        await generate_question_second(
            book_id=book_id, counter=c, call=call, battle_id=battle_id
        )
        await state.update_data(
            c_two=c
        )
        await db.add_answer_second(
            second_player=second_player, battle_id=battle_id, question_number=c - 1, answer="✅", game_status="ON"
        )


second_answer_filter = (F.data.startswith("second_player:b") | F.data.startswith("second_player:c") |
                        F.data.startswith("second_player:d"))


@router.callback_query(second_answer_filter)
async def get_question_answer(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_two']
    book_id = call.data.split(":")[2]
    battle_id = int(call.data.split(":")[3])
    second_player = call.from_user.id

    if c == 10:
        await db.add_answer_second(
            second_player=second_player, battle_id=battle_id, question_number=c, answer="❌", game_status="OVER"
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
        await db.add_answer_second(
            second_player=second_player, battle_id=battle_id, question_number=c - 1, answer="❌", game_status="ON"
        )