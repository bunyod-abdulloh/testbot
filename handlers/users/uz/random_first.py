import asyncio
import random

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.users.uz.random_second import send_result
from keyboards.inline.buttons import to_offer_ibuttons, StartPlayingCallback
from loader import db, bot

router = Router()


async def generate_question(book_id, counter, call: types.CallbackQuery, battle_id):
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
                text=f"{letter}", callback_data=f"question:{callback[0]}:{book_id}:{battle_id}"
            )
        )
    builder.adjust(2, 2)

    await call.message.edit_text(
        text=f"{counter}. {questions[0]['question']}\n\n"
             f"{questions_text}",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("book_id:"))
async def get_random_in_battle(call: types.CallbackQuery):
    book_id = int(call.data.split(':')[1])
    book_name_ = await db.select_book_by_id(id_=book_id)
    book_name = book_name_['table_name']
    user_id = call.from_user.id
    full_name = call.from_user.full_name

    random_user = await db.select_user_random()
    count_users = await db.count_users()
    print(random_user)
    if count_users == 1:
        await call.answer(
            text="Hozircha raqiblar topilmadi! Botga yangi foydalanuvchilar taklif qiling va birgalikda bellashuvni "
                 "davom ettiring!", show_alert=True
        )
        await call.message.delete()
    else:
        if random_user is None:
            await call.answer(
                text="Bellashish uchun raqib topilmadi! Barcha foydalanuvchilar band! Bellashish uchun botga yangi "
                     "foydalanuvchilar taklif qilishingiz yoki foydalanuvchilar bellashuvlarni yakunlashini kutishingiz"
                     " mumkin!", show_alert=True
            )
            await call.message.delete()
        else:
            markup = to_offer_ibuttons(
                agree_text="Qabul qilish", agree_id=user_id, refusal_text="Rad qilish", book_id=book_id
            )
            if random_user['telegram_id'] == user_id:
                other_random = await db.select_user_random()
                c = 0
                while other_random['telegram_id'] == random_user['telegram_id']:
                    other_random = await db.select_user_random()
                    c += 1

                    if c == 4:
                        await call.answer(
                            text="Bellashish uchun raqib topilmadi! Barcha foydalanuvchilar band! Bellashish uchun botga yangi "
                                 "foydalanuvchilar taklif qilishingiz yoki foydalanuvchilar bellashuvlarni yakunlashini kutishingiz"
                                 " mumkin!", show_alert=True
                        )
                        await call.message.delete()
                        break

                await bot.send_message(
                    chat_id=other_random['telegram_id'],
                    text=f"Foydalanuvchi {full_name} Sizni {book_name} kitobi bo'yicha bellashuvga taklif qilmoqda!",
                    reply_markup=markup
                )
                await call.answer(
                    text="Raqibingizga bellashuv taklifi yuborildi!"
                )
                await call.message.edit_text(
                    text="Raqibingizdan javob kelmasa qayta <b>Tasodifiy raqib bilan</b> tugmasini bosing!"
                )
            else:
                await bot.send_message(
                    chat_id=random_user['telegram_id'],
                    text=f"Foydalanuvchi {full_name} Sizni {book_name} kitobi bo'yicha bellashuvga taklif qilmoqda!",
                    reply_markup=markup
                )

                await call.answer(
                    text="Raqibingizga bellashuv taklifi yuborildi!"
                )
                await call.message.edit_text(
                    text="Raqibingizdan javob kelmasa qayta <b>Tasodifiy raqib bilan</b> tugmasini bosing!"
                )


@router.callback_query(StartPlayingCallback.filter())
async def start_playing(call: types.CallbackQuery, callback_data: StartPlayingCallback, state: FSMContext):
    book_id = callback_data.book_id
    battle_id = callback_data.battle_id
    first_player_id = call.from_user.id

    await db.update_gaming_status(
        status=True, telegram_id=first_player_id
    )

    c_one = 1
    await generate_question(
        book_id=book_id, counter=c_one, call=call, battle_id=battle_id
    )
    await state.update_data(
        c_one=c_one
    )


@router.callback_query(F.data.startswith("question:a"))
async def get_question_first_a(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_one']
    book_id = call.data.split(":")[2]
    battle_id = int(call.data.split(":")[3])
    first_player_id = call.from_user.id

    if c == 10:
        await db.add_answer_first_(
            first_player=first_player_id, battle_id=battle_id, question_number=c, answer="✅", game_status="OVER"
        )
        await db.update_all_game_status(
            game_status="OVER", column_name="first_player", column_value=first_player_id
        )
        second_battler = await db.get_battle_second(
            battle_id=battle_id
        )
        first_results = await db.select_first_player(
            first_player=first_player_id
        )
        first_send = send_result(
            results=first_results, second_text="Raqibingiz natijasi", second_player=True
        )
        bot_send = send_result(
            results=first_results, first_text="Sizning natijangiz", first_player=True
        )

        if not second_battler:
            await call.message.edit_text(
                text=f"{first_send}"
                     f"Raqibingiz hali o'yinni boshlamadi! O'yinni boshlaganidan so'ng raqibingiz natijalari ham "
                     f"yuboriladi!"
            )
        else:
            second_player_id = second_battler[0]['second_player']
            second_results = await db.select_second_player(
                second_player=second_player_id
            )
            second_send = send_result(
                results=second_results, first_text="Sizning natijangiz", first_player=True
            )
            bot_send_ = send_result(
                results=second_results, second_text="Raqibingiz natijasi", second_player=True
            )
            if second_battler[0]['game_status'] == "ON":
                await call.message.edit_text(
                    text=f"{first_send}"
                         f"Raqibingiz hali o'yinni tugatmadi! Tugatganidan so'ng raqibingiz natijalari ham yuboriladi!"
                )
            else:
                await call.message.edit_text(
                    text=f"{first_send}\n{second_send}"
                )
                await bot.send_message(
                    chat_id=second_player_id,
                    text=f"{bot_send}\n{bot_send_}"
                )
        await state.clear()
    else:
        c += 1
        await generate_question(
            book_id=book_id, counter=c, call=call, battle_id=battle_id
        )
        await state.update_data(
            c_one=c
        )
        await db.add_answer_first_(
            first_player=first_player_id, battle_id=battle_id, question_number=c - 1, answer="✅", game_status="ON"
        )


first_answer_filter = (F.data.startswith("question:b") | F.data.startswith("question:c") |
                       F.data.startswith("question:d"))


@router.callback_query(first_answer_filter)
async def get_question_first(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c = data['c_one']
    book_id = call.data.split(":")[2]
    battle_id = int(call.data.split(":")[3])
    first_player = call.from_user.id

    if c == 10:
        await db.add_answer_first_(
            first_player=first_player, battle_id=battle_id, question_number=c, answer="❌", game_status="OVER"
        )
        await db.update_all_game_status(
            game_status="OVER", column_name="first_player", column_value=first_player
        )
        first_results = await db.select_first_player(
            first_player=first_player
        )
        second_battler = await db.get_battle_second(
            battle_id=battle_id
        )
        first_message = send_result(
            results=first_results
        )

        if not second_battler:
            await call.message.edit_text(
                text=f"{first_message}"
                     f"Raqibingiz hali o'yinni boshlamadi! O'yinni boshlaganidan so'ng raqibingiz natijalari ham "
                     f"yuboriladi!"
            )
        else:
            if second_battler['game_status'] == "ON":
                await call.message.edit_text(
                    text=f"{first_message}"
                         f"Raqibingiz hali o'yinni tugatmadi! Tugatganidan so'ng raqibingiz natijalari ham yuboriladi!"
                )
            else:
                print(f"{second_battler} second battler")
        await state.clear()
    else:
        c += 1
        await generate_question(
            book_id=book_id, counter=c, call=call, battle_id=battle_id
        )
        await state.update_data(
            c_one=c
        )
        await db.add_answer_first_(
            first_player=first_player, battle_id=battle_id, question_number=c - 1, answer="❌", game_status="ON"
        )
