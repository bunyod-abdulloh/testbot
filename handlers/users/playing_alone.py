import random
from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.users.battle_main import result_time_game
from handlers.users.random_first import first_text
from loader import db

router = Router()


async def generate_question_alone(book_id, counter, call: types.CallbackQuery):
    questions = await db.select_all_questions(table_name=f"table_{book_id}")
    question_id = questions[0]['id']
    letters = ["A", "B", "C", "D"]

    a = ["a", f"{questions[0]['a_correct']}"]
    b = ["b", f"{questions[0]['b']}"]
    c = ["c", f"{questions[0]['c']}"]
    d = ["d", f"{questions[0]['d']}"]

    answers = [a, b, c, d]
    random.shuffle(answers)
    questions_text = str()

    for letter, question in zip(letters, answers):
        questions_text += f"{letter}) {question[1]}\n"

    builder = InlineKeyboardBuilder()
    for letter, callback in zip(letters, answers):
        builder.add(
            types.InlineKeyboardButton(
                text=f"{letter}", callback_data=f"al_question:{callback[0]}:{book_id}:{question_id}"
            )
        )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


async def send_alone_result_or_continue(call: types.CallbackQuery, answer_emoji, state: FSMContext):
    telegram_id = call.from_user.id
    book_id = int(call.data.split(":")[2])
    question_id = int(call.data.split(":")[3])
    get_question = await db.select_question_by_id(table_name=f"table_{book_id}", id_=question_id)
    book_name = await db.select_book_by_id(id_=book_id)

    c = await state.get_data()
    counter = c['alone']
    if counter >= 10:
        await db.add_answer_to_temporary(
            telegram_id=telegram_id, battle_id=0, answer=answer_emoji, game_status="ON",
            question=get_question['question'], correct_answer=get_question['a_correct']
        )
        await db.update_all_game_status(
            game_status="OVER", telegram_id=telegram_id, battle_id=0
        )
        # User o'yinni tugatgan vaqtni DBga yozish
        end_time = datetime.now()
        await db.end_answer_to_temporary(
            telegram_id=telegram_id, battle_id=0, game_status="OFF", end_time=end_time
        )
        start_time = await db.select_start_time(
            telegram_id=telegram_id, battle_id=0
        )
        # O'yin boshlangan va tugagan vaqtni hisoblash
        difference = await result_time_game(
            start_time=start_time[0][0], end_time=end_time
        )
        # To'g'ri javoblar soni
        correct_answers = await db.count_answers(
            telegram_id=telegram_id, battle_id=0, answer="✅"
        )
        # To'g'ri javoblar sonini Results jadvalidan yangilash
        await db.update_results(
            results=correct_answers, telegram_id=telegram_id, book_id=book_id, time_result=difference
        )
        f_text = await first_text(
            first_player=telegram_id, book_name=book_name['table_name'], correct_answers=correct_answers,
            time=difference, battle_id=0
        )
        await call.message.edit_text(
            text=f_text
        )
        await db.edit_status_users(
            game_on=False, telegram_id=telegram_id
        )
        # Natijani Temporary jadvalidan tozalash
        await db.delete_from_temporary(
            telegram_id=telegram_id
        )
    else:
        await db.add_answer_to_temporary(
            telegram_id=telegram_id, battle_id=0, answer=answer_emoji, game_status="ON",
            question=get_question['question'], correct_answer=get_question['a_correct']
        )
        counter = c['alone'] + 1
        await generate_question_alone(
            book_id=book_id, call=call, counter=counter
        )
        await state.update_data(
            alone=counter
        )


@router.callback_query(F.data.startswith("alone:"))
async def alone_first(call: types.CallbackQuery, state: FSMContext):
    book_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id
    c = 1
    await generate_question_alone(
        book_id=book_id, call=call, counter=c
    )
    # Userni Results jadvalida bor yo'qligini tekshirish
    check_in_results = await db.select_user_in_results(
        telegram_id=telegram_id, book_id=book_id
    )
    if not check_in_results:
        # Results jadvaliga userni qo'shish
        await db.add_gamer(
            telegram_id=telegram_id, book_id=book_id
        )
    # Users jadvalida userga game_on yoqish
    await db.edit_status_users(
        game_on=True, telegram_id=telegram_id
    )
    start_time = datetime.now()
    await db.start_time_to_temporary(
        telegram_id=telegram_id, battle_id=0, game_status="ON", start_time=start_time
    )
    await state.update_data(
        alone=c
    )


@router.callback_query(F.data.startswith("al_question:a"))
async def alone_second(call: types.CallbackQuery, state: FSMContext):
    await send_alone_result_or_continue(
        call=call, answer_emoji="✅", state=state
    )


magic_alone = (F.data.startswith("al_question:b") | F.data.startswith("al_question:c") |
               F.data.startswith("al_question:d"))


@router.callback_query(magic_alone)
async def alone_third(call: types.CallbackQuery, state: FSMContext):
    await send_alone_result_or_continue(
        call=call, answer_emoji="❌", state=state
    )
