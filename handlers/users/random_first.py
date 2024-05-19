import random
from datetime import datetime

import aiogram.exceptions
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.users.battle_main import result_time_game
from keyboards.inline.buttons import to_offer_ibuttons
from loader import db, bot

router = Router()

numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟️']


async def generate_question(book_id, counter, call: types.CallbackQuery, battle_id, opponent=False):
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
    if opponent:
        for letter, callback in zip(letters, answers):
            builder.add(
                types.InlineKeyboardButton(
                    text=f"{letter}", callback_data=f"s_question:{callback[0]}:{book_id}:{battle_id}:{question_id}"
                )
            )
    else:
        for letter, callback in zip(letters, answers):
            builder.add(
                types.InlineKeyboardButton(
                    text=f"{letter}", callback_data=f"question:{callback[0]}:{book_id}:{battle_id}:{question_id}"
                )
            )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


async def first_text(first_player, battle_id, book_name, correct_answers, time, second_player=None,
                     second_correct_answers=None, second_time=None, second=False, second_send=False):
    answers = await db.select_answers_temporary(
        battle_id=battle_id, telegram_id=first_player
    )
    full_name = await db.select_user(
        telegram_id=first_player
    )
    vaqt_str = f"{time}"

    # Vaqt obyekti sifatida o'qish
    vaqt = datetime.strptime(vaqt_str, "%H:%M:%S.%f")

    # Vaqtni sekundga aylantirish
    sekundlar = vaqt.hour * 3600 + vaqt.minute * 60 + vaqt.second + vaqt.microsecond / 1000000
    butun_son = round(sekundlar)

    number_ = str()
    answer_ = str()
    answers_ = str()
    for n in numbers:
        number_ += f"{n} "
    for index, answer in enumerate(answers):
        answer_ += f"{answer['answer']} "
        answers_ += f"{numbers[index]} - {answer['question']}\n✅ {answer['correct_answer']}\n\n"
    result = f"{number_}\n\n{answer_}\n\n{answers_}"
    if second:
        second_full_name = await db.select_user(
            telegram_id=second_player
        )
        vaqt_str_ = f"{second_time}"

        # Vaqt obyekti sifatida o'qish
        vaqt_ = datetime.strptime(vaqt_str_, "%H:%M:%S.%f")

        # Vaqtni sekundga aylantirish
        sekundlar_ = vaqt_.hour * 3600 + vaqt_.minute * 60 + vaqt_.second + vaqt_.microsecond / 1000000
        butun_son_ = round(sekundlar_)
        if second_send:
            s_text = (f"<b><i>Yakuniy natijalar</i></b>\n\n<i><b>Kitob nomi:</b> {book_name}</i>"
                      f"\n\n<i><b>{full_name['full_name']}:</b> <u>{correct_answers}/10 </u> |</i> "
                      f"💎: <i><u>{correct_answers} ball</u> |</i> ⏳: <i><u>{butun_son} soniya</u></i>"
                      f"\n\n<i><b>{second_full_name['full_name']}:</b> <u>{second_correct_answers}/10 </u> |</i> "
                      f"💎: <i><u>{second_correct_answers} ball</u> |</i> ⏳: <i><u>{butun_son_} soniya</u></i>"
                      )
            return s_text
        else:
            second_text = (f"<b><i>Bellashuv natijalari</i></b>\n\n<i><b>Kitob nomi:</b> {book_name}</i>"
                           f"\n\n<i><b>{full_name['full_name']}:</b> <u>{correct_answers}/10 </u> |</i> "
                           f"💎: <i><u>{correct_answers} ball</u> |</i> ⏳: <i><u>{butun_son} soniya</u></i>"
                           f"\n\n<i><b>{second_full_name['full_name']}:</b> <u>{second_correct_answers}/10 </u> |</i> "
                           f"💎: <i><u>{second_correct_answers} ball</u> |</i> ⏳: <i><u>{butun_son_} soniya</u></i>"
                           f"\n\n{result}"
                           )
        return second_text
    else:
        text = (f"<b><i>Bellashuv natijalari</i></b>\n\n<i><b>Kitob nomi:</b> {book_name}</i>"
                f"\n\n<i><b>{full_name['full_name']}:</b> <u>{correct_answers}/10 </u> |</i> "
                f"💎: <i><u>{correct_answers} ball</u> |</i> ⏳: <i><u>{butun_son} soniya</u></i>"
                f"\n\n{result}"
                )
        return text


async def send_result_or_continue(answer_emoji, call: types.CallbackQuery, state: FSMContext, opponent=False):
    first_telegram_id = call.from_user.id
    book_id = int(call.data.split(":")[2])
    battle_id = int(call.data.split(":")[3])
    question_id = int(call.data.split(":")[4])
    get_question = await db.select_question_by_id(table_name=f"table_{book_id}", id_=question_id)
    book_name = await db.select_book_by_id(
        id_=book_id
    )
    c = await state.get_data()
    counter = c['duet']
    if counter >= 10:
        await db.add_answer_to_temporary(
            telegram_id=first_telegram_id, battle_id=battle_id, answer=answer_emoji, game_status="ON",
            question=get_question['question'], correct_answer=get_question['a_correct']
        )
        await db.update_all_game_status(
            game_status="OVER", telegram_id=first_telegram_id, battle_id=battle_id
        )
        # To'g'ri javoblar soni
        first_correct_answers = await db.count_answers(
            telegram_id=first_telegram_id, battle_id=battle_id, answer="✅"
        )
        second_battler = await db.get_battle_temporary(
            battle_id=battle_id, telegram_id=first_telegram_id
        )
        # User o'yinni tugatgan vaqtni DBga yozish
        end_time = datetime.now()
        await db.end_answer_to_temporary(
            telegram_id=first_telegram_id, battle_id=battle_id, game_status="OFF", end_time=end_time
        )
        start_time = await db.select_start_time(
            telegram_id=first_telegram_id, battle_id=battle_id
        )
        # O'yin boshlangan va tugagan vaqtni hisoblash
        difference = await result_time_game(
            start_time=start_time[0]['start_time'], end_time=end_time
        )
        # Birinchi o'yinchiga Users jadvalida game_on FALSE qilish
        await db.edit_status_users(
            game_on=False, telegram_id=first_telegram_id
        )
        # To'g'ri javoblar sonini Results jadvalidan yangilash
        await db.update_results(
            results=first_correct_answers, telegram_id=first_telegram_id, book_id=book_id, time_result=difference
        )
        f_text = await first_text(
            first_player=first_telegram_id, book_name=book_name['table_name'], correct_answers=first_correct_answers,
            time=difference, battle_id=battle_id
        )
        if not second_battler or second_battler[0]['game_status'] == "ON":
            if not second_battler:
                await call.message.edit_text(
                    text=f"{f_text}\nRaqibingiz hali o'yinni boshlamadi! O'yinni boshlaganidan so'ng raqibingiz "
                         f"natijalari ham yuboriladi!"
                )
            else:
                await call.message.edit_text(
                    text=f"{f_text}\n"
                         f"Raqibingiz hali o'yinni tugatmadi! Tugatganidan so'ng raqibingiz natijalari ham yuboriladi!"
                )
        else:
            second_telegram_id = second_battler[0]['telegram_id']
            # Raqib o'yinni tugatgan vaqtni ma'lumotlar omboriga yozish
            end_time_ = await db.select_end_time(
                telegram_id=second_telegram_id, battle_id=battle_id
            )
            start_time_ = await db.select_start_time(
                telegram_id=second_telegram_id, battle_id=battle_id
            )
            # O'yin boshlangan va tugagan vaqtni hisoblash
            difference_ = await result_time_game(
                start_time=start_time_[0][0], end_time=end_time_[0][0]
            )
            # Raqib to'g'ri javoblari soni
            second_correct_answers = await db.count_answers(
                telegram_id=second_telegram_id, battle_id=battle_id, answer="✅"
            )
            # Userni Result jadvalida natijasini tekshirish
            check_results_ = await db.select_user_in_results(
                telegram_id=second_telegram_id, book_id=book_id
            )
            if check_results_['result'] == 0:
                # Raqib to'g'ri javoblari sonini Results jadvalidan yangilash
                await db.update_results(
                    results=second_correct_answers, telegram_id=second_telegram_id,
                    book_id=book_id, time_result=difference_
                )
            # Birinchi o'yinchiga ikkala natijani yuborish
            s_text = await first_text(
                first_player=first_telegram_id, battle_id=battle_id, book_name=book_name['table_name'],
                correct_answers=first_correct_answers, time=difference, second_player=second_telegram_id,
                second_correct_answers=second_correct_answers, second_time=difference_, second=True
            )
            await call.message.edit_text(
                text=f"{s_text}"
            )
            # Ikkinchi o'yinchiga ikkala natijani yuborish
            s_text_bot = await first_text(
                first_player=first_telegram_id, battle_id=battle_id, book_name=book_name['table_name'],
                correct_answers=first_correct_answers, time=difference, second_player=second_telegram_id,
                second_correct_answers=second_correct_answers, second_time=difference_, second=True, second_send=True
            )
            try:
                await bot.send_message(
                    chat_id=second_telegram_id, text=f"{s_text_bot}"
                )
                # Users jadvalida ikkinchi o'yinchiga game_on FALSE qilish
                await db.edit_status_users(
                    game_on=False, telegram_id=second_telegram_id
                )
                # Ikkinchi o'yinchi natijalarini Temporary jadvalidan tozalash
                await db.delete_from_temporary(
                    telegram_id=second_telegram_id
                )
            except aiogram.exceptions.TelegramForbiddenError:
                await db.userni_ochir(
                    telegram_id=second_telegram_id
                )
            # Birinchi o'yinchiga Users jadvalida game_on FALSE qilish
            await db.edit_status_users(
                game_on=False, telegram_id=first_telegram_id
            )
            # Birinchi o'yinchi natijalarini Temporary jadvalidan tozalash
            await db.delete_from_temporary(
                telegram_id=first_telegram_id
            )
        await state.clear()
    else:
        await db.add_answer_to_temporary(
            telegram_id=first_telegram_id, battle_id=battle_id, answer=answer_emoji, game_status="ON",
            question=get_question['question'], correct_answer=get_question['a_correct']
        )
        counter = c['duet'] + 1
        if opponent:
            await generate_question(
                book_id=book_id, counter=counter, call=call, battle_id=battle_id, opponent=True
            )
        else:
            await generate_question(
                book_id=book_id, counter=counter, call=call, battle_id=battle_id
            )
        await state.update_data(
            duet=counter
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
    not_battler = "Bellashish uchun raqib topilmadi! Raqib taklif qilishingiz yoki Yakka o'yin o'ynashingiz mumkin!"
    if random_user is None:
        await call.message.edit_text(
            text=not_battler
        )
    else:
        telegram_id = random_user['telegram_id']
        markup = to_offer_ibuttons(
            agree_text="Qabul qilish", agree_id=user_id, refusal_text="Rad qilish", book_id=book_id
        )
        try:
            await bot.send_message(
                chat_id=telegram_id,
                text=f"Foydalanuvchi {full_name} Sizni {book_name} kitobi bo'yicha bellashuvga taklif qilmoqda!",
                reply_markup=markup
            )
            await call.answer(
                text="Bellashuv taklifi yuborildi! Raqibingizdan javob kelmasa qayta Tasodifiy raqib bilan tugmasini "
                     "bosing!", show_alert=True
            )
        except aiogram.exceptions.TelegramForbiddenError:
            await db.userni_ochir(
                telegram_id=telegram_id
            )
            await call.answer(
                text=not_battler, show_alert=True
            )


@router.callback_query(F.data.startswith("play_b:"))
async def start_playing(call: types.CallbackQuery, state: FSMContext):
    book_id = call.data.split(":")[1]
    battle_id = int(call.data.split(":")[2])
    first_player_id = call.from_user.id
    c = 1
    await state.update_data(
        duet=c
    )
    await generate_question(
        book_id=book_id, counter=c, call=call, battle_id=battle_id
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
        telegram_id=first_player_id, battle_id=battle_id, game_status="ON", start_time=start_time
    )


@router.callback_query(F.data.startswith("question:a"))
async def get_question_first_a(call: types.CallbackQuery, state: FSMContext):
    await send_result_or_continue(
        answer_emoji="✅", call=call, state=state
    )


first_answer_filter = (F.data.startswith("question:b") | F.data.startswith("question:c") |
                       F.data.startswith("question:d"))


@router.callback_query(first_answer_filter)
async def get_question_first(call: types.CallbackQuery, state: FSMContext):
    await send_result_or_continue(
        answer_emoji="❌", call=call, state=state
    )
