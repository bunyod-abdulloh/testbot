import random
from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.users.uz.battle_main import result_time_game
from keyboards.inline.buttons import to_offer_ibuttons, StartPlayingCallback
from loader import db, bot

router = Router()


async def generate_question(book_id, counter, call: types.CallbackQuery, battle_id, opponent=False):
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
    if opponent:
        for letter, callback in answers_dict.items():
            builder.add(
                types.InlineKeyboardButton(
                    text=f"{letter}", callback_data=f"s_question:{callback[0]}:{book_id}:{battle_id}"
                )
            )
    else:
        for letter, callback in answers_dict.items():
            builder.add(
                types.InlineKeyboardButton(
                    text=f"{letter}", callback_data=f"question:{callback[0]}:{book_id}:{battle_id}"
                )
            )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


def first_text(book_name, result_text, correct_answers, wrong_answers,
               book_points, book_rating, all_points, all_rating):
    text = (f"<b><i>Bellashuv natijalari</i></b>\n\n<i><b>Kitob nomi:</b> {book_name}</i>"
            f"\n\n<i><b>Savollar soni:</b> 10 ta</i>\n\n😊 <i><b><u>{result_text}:</u></b></i>"
            f"\n\n✅ <i><b>To'g'ri javob:</b> {correct_answers} ta</i>"
            f"\n\n❌ <i><b>Noto'g'ri javob:</b> {wrong_answers} ta</i>"
            f"\n\n💎 <i><b>Kitob bo'yicha to'plangan ball:</b> {book_points} ball</i>"
            f"\n\n📖 <i><b>Kitob bo'yicha reyting:</b> {book_rating} - o'rin</i>"
            f"\n\n📥 <i><b>Umumiy ball:</b> {all_points} ball</i>"
            f"\n\n📚 <i><b>Umumiy reyting:</b> {all_rating} - o'rin</i>")
    return text


def second_text(correct_answers, result_text, wrong_answers, book_points, book_rating, all_points, all_rating):
    text = (f"😎 <i><b><u>{result_text}:</u></b></i>"
            f"\n\n✅ <i><b>To'g'ri javob:</b> {correct_answers} ta</i>"
            f"\n\n❌ <i><b>Noto'g'ri javob:</b> {wrong_answers} ta</i>"
            f"\n\n💎 <i><b>Kitob bo'yicha to'plangan ball:</b> {book_points} ball</i>"
            f"\n\n📖 <i><b>Kitob bo'yicha reyting:</b> {book_rating} - o'rin</i>"
            f"\n\n📥 <i><b>Umumiy ball:</b> {all_points} ball</i>"
            f"\n\n📚 <i><b>Umumiy reyting:</b> {all_rating} - o'rin</i>")
    return text


async def send_result_or_continue(counter, answer_emoji, call: types.CallbackQuery, state: FSMContext,
                                  counter_key, opponent=False):
    first_telegram_id = call.from_user.id
    book_id = int(call.data.split(":")[2])
    book_name = await db.select_book_by_id(
        id_=book_id
    )
    battle_id = int(call.data.split(":")[3])
    if counter == 10:
        await db.add_answer_to_temporary(
            telegram_id=first_telegram_id, battle_id=battle_id, question_number=counter,
            answer=answer_emoji, game_status="ON"
        )
        await db.update_all_game_status(
            game_status="OVER", telegram_id=first_telegram_id, battle_id=battle_id
        )
        # User o'yinni tugatgan vaqtni DBga yozish
        end_time = datetime.now()
        await db.end_answer_to_temporary(
            telegram_id=first_telegram_id, battle_id=battle_id, answer="FIRST_END", end_time=end_time
        )
        start_time = await db.select_start_time(
            telegram_id=first_telegram_id
        )
        # O'yin boshlangan va tugagan vaqtni hisoblash
        difference = await result_time_game(
            start_time=start_time[0][0], end_time=end_time
        )
        # To'g'ri javoblar soni
        first_correct_answers = await db.count_answers(
            telegram_id=first_telegram_id, answer="✅"
        )
        # Noto'g'ri javoblar soni
        first_wrong_answers = await db.count_answers(
            telegram_id=first_telegram_id, answer="❌"
        )
        # Userni Result jadvalida natijasini tekshirish
        check_results = await db.select_battle_id_results(
            telegram_id=first_telegram_id, book_id=book_id, battle_id=battle_id
        )
        if check_results['result'] == 0:
            # To'g'ri javoblar sonini Results jadvalidan yangilash
            await db.update_results(
                results=first_correct_answers, telegram_id=first_telegram_id, book_id=book_id, time_result=difference
            )
        # Results jadvalidan user reytingini kitob bo'yicha aniqlash
        rating_book = await db.get_rating_by_result(
            book_id=book_id
        )
        first_rating_book_ = int()
        first_points = int()
        for index, result in enumerate(rating_book):
            if result['telegram_id'] == first_telegram_id:
                first_rating_book_ += index + 1
                first_points += result['result']
                break
        # Results jadvalidan userning umumiy reytingini aniqlash
        all_rating = await db.get_rating_all()
        first_all_rating = int()
        first_all_points = int()
        for index, result in enumerate(all_rating):
            if result['telegram_id'] == first_telegram_id:
                first_all_rating += index + 1
                first_all_points += result['result']
                break
        f_text = first_text(
            book_name=book_name, result_text="Sizning natijangiz", correct_answers=first_correct_answers,
            wrong_answers=first_wrong_answers, book_rating=first_rating_book_, all_rating=first_all_rating,
            book_points=first_points, all_points=first_all_points
        )
        # Raqib o'yin holatini aniqlash
        second_battler = await db.get_battle(
            battle_id=battle_id, telegram_id=first_telegram_id
        )
        if not second_battler:
            await call.message.edit_text(
                text=f"{f_text}\n\nRaqibingiz hali o'yinni boshlamadi! O'yinni boshlaganidan so'ng raqibingiz "
                     f"natijalari ham yuboriladi!"
            )
            await db.edit_status_users(
                game_on=False, telegram_id=first_telegram_id
            )
        else:
            second_telegram_id = second_battler[0]['telegram_id']
            # Raqib o'yinni tugatgan vaqtni ma'lumotlar omboriga yozish
            end_time_ = datetime.now()
            await db.end_answer_to_temporary(
                telegram_id=second_telegram_id, battle_id=battle_id, answer="SECOND_END", end_time=end_time_
            )
            start_time_ = await db.select_start_time(
                telegram_id=second_telegram_id
            )
            # O'yin boshlangan va tugagan vaqtni hisoblash
            difference_ = await result_time_game(
                start_time=start_time_[0][0], end_time=end_time_
            )
            # Raqib to'g'ri javoblari soni
            second_correct_answers = await db.count_answers(
                telegram_id=second_telegram_id, answer="✅"
            )
            # Raqib noto'g'ri javoblari soni
            second_wrong_answers = await db.count_answers(
                telegram_id=second_telegram_id, answer="❌"
            )
            # Userni Result jadvalida natijasini tekshirish
            check_results_ = await db.select_battle_id_results(
                telegram_id=second_telegram_id, book_id=book_id, battle_id=battle_id
            )
            if check_results_['result'] == 0:
                # Raqib to'g'ri javoblari sonini Results jadvalidan yangilash
                await db.update_results(
                    results=second_correct_answers, telegram_id=second_telegram_id, book_id=book_id, time_result=difference_
                )
            # Results jadvalidan raqib reytingini kitob bo'yicha aniqlash
            second_rating_book = int()
            second_points = int()
            for index, result in enumerate(rating_book):
                if result['telegram_id'] == second_telegram_id:
                    second_rating_book += index + 1
                    second_points += result['result']
                    break
            # Results jadvalidan raqib umumiy reytingini aniqlash
            second_all_rating = int()
            second_all_points = int()
            for index, result in enumerate(all_rating):
                if result['telegram_id'] == second_telegram_id:
                    second_all_rating += index + 1
                    second_all_points += result['result']
                    break

            if second_battler[0]['game_status'] == "ON":
                await call.message.edit_text(
                    text=f"{f_text}\n\n"
                         f"Raqibingiz hali o'yinni tugatmadi! Tugatganidan so'ng raqibingiz natijalari ham yuboriladi!"
                )
                await db.edit_status_users(
                    game_on=False, telegram_id=first_telegram_id
                )
            else:
                # Birinchi o'yinchiga ikkala natijani yuborish
                s_text = second_text(
                    correct_answers=second_correct_answers, result_text="Raqibingiz natijasi",
                    wrong_answers=second_wrong_answers, book_rating=second_rating_book, all_rating=second_all_rating,
                    book_points=second_points, all_points=second_all_points
                )
                await call.message.edit_text(
                    text=f"{f_text}\n\n{s_text}"
                )
                # Ikkinchi o'yinchiga ikkala natijani yuborish
                s_text_bot = first_text(
                    book_name=book_name, result_text="Sizning natijaningiz", correct_answers=second_correct_answers,
                    wrong_answers=second_wrong_answers, book_points=second_points, book_rating=second_rating_book,
                    all_points=second_all_points, all_rating=second_all_rating
                )
                f_text_bot = second_text(
                    correct_answers=first_correct_answers, result_text="Raqibingiz natijasi",
                    wrong_answers=first_wrong_answers, book_points=first_points, book_rating=first_rating_book_,
                    all_points=first_all_points, all_rating=first_all_rating
                )
                await bot.send_message(
                    chat_id=second_telegram_id, text=f"{s_text_bot}\n\n{f_text_bot}"
                )
                await db.edit_status_users(
                    game_on=False, telegram_id=first_telegram_id
                )
                await db.edit_status_users(
                    game_on=False, telegram_id=second_telegram_id
                )
                await db.delete_user_results(
                    telegram_id=first_telegram_id
                )
                await db.delete_user_results(
                    telegram_id=second_telegram_id
                )
    else:
        await db.add_answer_to_temporary(
            telegram_id=first_telegram_id, battle_id=battle_id, question_number=counter,
            answer=answer_emoji, game_status="ON"
        )

        counter += 1
        if opponent:
            await generate_question(
                book_id=book_id, counter=counter, call=call, battle_id=battle_id, opponent=True
            )
        else:
            await generate_question(
                book_id=book_id, counter=counter, call=call, battle_id=battle_id
            )
        await state.update_data(
            {counter_key: counter}
        )


@router.callback_query(F.data.startswith("book_id:"))
async def get_random_in_battle(call: types.CallbackQuery):
    book_id = int(call.data.split(':')[1])
    book_name_ = await db.select_book_by_id(id_=book_id)
    book_name = book_name_['table_name']
    user_id = call.from_user.id
    full_name = call.from_user.full_name

    random_user = await db.select_user_random(
        telegram_id=user_id
    )

    if random_user is None:
        await call.message.edit_text(
            text="Bellashish uchun raqib topilmadi! <b>Raqib taklif qilish</b>ingiz yoki <b>Yakka o'yin</b> "
                 "o'ynashingiz mumkin!"
        )
    else:
        markup = to_offer_ibuttons(
            agree_text="Qabul qilish", agree_id=user_id, refusal_text="Rad qilish", book_id=book_id
        )
        await bot.send_message(
            chat_id=random_user['telegram_id'],
            text=f"Foydalanuvchi {full_name} Sizni {book_name} kitobi bo'yicha bellashuvga taklif qilmoqda!",
            reply_markup=markup
        )
        await call.message.edit_text(
            text="Raqibingizdan javob kelmasa qayta <b>Tasodifiy raqib bilan</b> tugmasini bosing!"
        )
        await call.answer(
            text="Raqibingizga bellashuv taklifi yuborildi!"
        )


@router.callback_query(StartPlayingCallback.filter())
async def start_playing(call: types.CallbackQuery, callback_data: StartPlayingCallback, state: FSMContext):
    book_id = callback_data.book_id
    battle_id = callback_data.battle_id
    first_player_id = call.from_user.id
    c_one = 1

    await generate_question(
        book_id=book_id, counter=c_one, call=call, battle_id=battle_id
    )
    await state.update_data(
        c_one=c_one
    )
    # Userni natijalar jadvalida bor yo'qligini tekshirish
    check_in_results = await db.select_user_in_results(
        telegram_id=first_player_id, book_id=book_id
    )
    if not check_in_results:
        # Results jadvaliga userni qo'shish
        await db.add_gamer(
            telegram_id=first_player_id, book_id=book_id
        )
    # Users jadvalida userga game_on yoqish
    await db.edit_status_users(
        game_on=True, telegram_id=first_player_id
    )
    start_time = datetime.now()
    await db.start_time_to_temporary(
        telegram_id=first_player_id, battle_id=battle_id, answer="START_TIME", start_time=start_time
    )


@router.callback_query(F.data.startswith("question:a"))
async def get_question_first_a(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_one']
    await send_result_or_continue(
        counter=c, answer_emoji="✅", call=call, state=state, counter_key="c_one"
    )


first_answer_filter = (F.data.startswith("question:b") | F.data.startswith("question:c") |
                       F.data.startswith("question:d"))


@router.callback_query(first_answer_filter)
async def get_question_first(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_one']
    await send_result_or_continue(
        counter=c, answer_emoji="❌", call=call, state=state, counter_key="c_one"
    )
