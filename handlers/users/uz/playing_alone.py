import random

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db

router = Router()


async def generate_question_alone(book_id, counter, call: types.CallbackQuery):
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
                text=f"{letter}", callback_data=f"al_question:{callback[0]}:{book_id}"
            )
        )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


async def question_answer_alone(call: types.CallbackQuery, c: str, answer: str):
    book_id = call.data.split(':')[2]
    user_id = call.from_user.id

    if c == 10:
        # Temporary jadvaliga savollarni javoblarini qo'shish
        await db.add_answer_(
            telegram_id=user_id, battle_id=0, question_number=c, answer=answer, game_status="OFF"
        )


@router.callback_query(F.data.startswith("alone:"))
async def alone_first(call: types.CallbackQuery, state: FSMContext):
    book_id = call.data.split(":")[1]
    c = 1
    await state.update_data(
        c_alone=c
    )
    await generate_question_alone(
        book_id=book_id, call=call, counter=c
    )


@router.callback_query(F.data.startswith("al_question:a"))
async def alone_second(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_alone']

