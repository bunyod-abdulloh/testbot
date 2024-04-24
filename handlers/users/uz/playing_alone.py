import asyncio
import datetime
import random
import time


from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.users.uz.random_first import first_text
from loader import db

router = Router()

first_time = datetime.datetime.now()
time.sleep(2)
later_time = datetime.datetime.now()

difference = later_time - first_time

minutes, seconds = divmod(difference.total_seconds(), 60)

print(f"Time difference: {minutes} minutes, {seconds} seconds")
time.sleep(5)
first_times = datetime.datetime.now()
time.sleep(6)
later_times = datetime.datetime.now()

differences = later_times - first_times

minutess, secondss = divmod(differences.total_seconds(), 60)

print(f"Time difference: {minutess} minutes, {secondss} seconds")

if difference < differences:
    print("natija")

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


async def send_alone_result_or_continue(counter, call: types.CallbackQuery, answer_emoji, book_id, book_name,
                                        counter_key, state: FSMContext):
    telegram_id = call.from_user.id

    if counter == 10:
        await db.add_answer_(
            telegram_id=telegram_id, battle_id=0, question_number=counter, answer=answer_emoji, game_status="ON"
        )
        await db.update_all_game_status(
            game_status="OVER", telegram_id=telegram_id, battle_id=0
        )
        # To'g'ri javoblar soni
        correct_answers = await db.count_answers(
            telegram_id=telegram_id, answer="✅"
        )
        # Noto'g'ri javoblar soni
        wrong_answers = await db.count_answers(
            telegram_id=telegram_id, answer="❌"
        )
        # To'g'ri javoblar sonini Results jadvalidan yangilash
        await db.update_results(
            results=correct_answers, telegram_id=telegram_id, book_id=book_id
        )
        # Results jadvalidan user reytingini kitob bo'yicha aniqlash
        rating_book = await db.get_rating_book(
            book_id=book_id
        )
        rating_book_ = int()
        for index, result in enumerate(rating_book):
            if result['telegram_id'] == telegram_id:
                rating_book_ += index + 1
                break
        # Results jadvalidan userning umumiy reytingini aniqlash
        all_rating = await db.get_rating_all()
        all_rating_ = int()
        for index, result in enumerate(all_rating):
            if result['telegram_id'] == telegram_id:
                all_rating_ += index + 1
                break
        f_text = first_text(
            book_name=book_name, result_text="Sizning natijangiz", correct_answers=correct_answers,
            wrong_answers=wrong_answers, book_rating=rating_book_, all_rating=all_rating_
        )
        await call.message.edit_text(
            text=f_text
        )
        await db.edit_status_users(
            game_on=False, telegram_id=telegram_id
        )
        await db.delete_user_results(
            telegram_id=telegram_id
        )
    else:
        await db.add_answer_(
            telegram_id=telegram_id, battle_id=0, question_number=counter, answer=answer_emoji, game_status="ON"
        )
        counter += 1
        await generate_question_alone(
            book_id=book_id, call=call, counter=counter
        )
        await state.update_data(
            {counter_key: counter}
        )


async def countdown(t, call: types.CallbackQuery):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        await call.message.edit_text(
            text=f"{timer}"
        )
        await asyncio.sleep(1)
        t -= 1


@router.callback_query(F.data.startswith("alone:"))
async def alone_first(call: types.CallbackQuery, state: FSMContext):
    book_id = int(call.data.split(":")[1])
    telegram_id = call.from_user.id

    # await call.message.answer(
    #     text="Boshlandi!!!"
    # )
    # t = 10
    # while t:
    #     mins, secs = divmod(t, 60)
    #     timer = '{:02d}:{:02d}'.format(mins, secs)
    #     print(timer, end="\r")
    #     await call.message.edit_text(
    #         text=f"{timer}"
    #     )
    #     await asyncio.sleep(1)
    #     t -= 1
    c = 1

    await generate_question_alone(
        book_id=book_id, call=call, counter=c
    )
    # Userni natijalar jadvalida bor yo'qligini tekshirish
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
    await state.update_data(
        c_alone=c
    )


@router.callback_query(F.data.endswith(":timer"))
async def alone_timer(call: types.CallbackQuery):
    print(call.data)
    # t = 60
    # while t:
    #     mins, secs = divmod(t, 60)
    #     timer = '{:02d}:{:02d}'.format(mins, secs)
    #     print(timer, end="\r")
    #     await call.message.edit_text(
    #         text=f"{timer}"
    #     )
    #     await asyncio.sleep(1)
    #     t -= 1


@router.callback_query(F.data.startswith("al_question:a"))
async def alone_second(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_alone']
    book_id = int(call.data.split(":")[2])
    book_name = await db.select_book_by_id(id_=book_id)

    await send_alone_result_or_continue(
        counter=c, call=call, answer_emoji="✅", book_id=book_id, book_name=book_name['table_name'],
        counter_key="c_alone", state=state
    )


magic_alone = (F.data.startswith("al_question:b") | F.data.startswith("al_question:c") |
               F.data.startswith("al_question:d"))


@router.callback_query(magic_alone)
async def alone_third(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_alone']
    book_id = int(call.data.split(":")[2])
    book_name = await db.select_book_by_id(id_=book_id)

    await send_alone_result_or_continue(
        counter=c, call=call, answer_emoji="❌", book_id=book_id, book_name=book_name['table_name'],
        counter_key="c_alone", state=state
    )
