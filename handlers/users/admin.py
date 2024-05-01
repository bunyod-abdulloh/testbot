import logging
import asyncio
import os

import pandas as pd
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.inline.buttons import battle_main_ibuttons
from loader import db, bot
from states.test import AdminState
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.pgtoexcel import export_to_excel

# from utils.pgtoexcel import export_to_excel

router = Router()

admin = int(ADMINS[0])


@router.message(Command('allusers'), IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    users = await db.select_all_users()

    file_path = f"data/users_list.xlsx"
    await export_to_excel(data=users, headings=['ID', 'Full Name', 'Username', 'Telegram ID'], filepath=file_path)

    await message.answer_document(types.input_file.FSInputFile(file_path))


# @router.message(Command('reklama'), IsBotAdminFilter(ADMINS))
# async def ask_ad_content(message: types.Message, state: FSMContext):
#     await message.answer("Reklama uchun post yuboring")
#     await state.set_state(AdminState.ask_ad_content)
#
#
# @router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
# async def send_ad_to_users(message: types.Message, state: FSMContext):
#     users = await db.select_all_users()
#     count = 0
#     for user in users:
#         user_id = user[-1]
#         try:
#             await message.send_copy(chat_id=user_id)
#             count += 1
#             await asyncio.sleep(0.05)
#         except Exception as error:
#             logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
#     await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
#     await state.clear()


# @router.message(Command('cleandb'), IsBotAdminFilter(ADMINS))
# async def ask_are_you_sure(message: types.Message, state: FSMContext):
#     msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?")
#     await state.update_data(msg_id=msg.message_id)
#     await state.set_state(AdminState.are_you_sure)
#
#
# @router.callback_query(AdminState.are_you_sure, IsBotAdminFilter(ADMINS))
# async def clean_db(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     msg_id = data.get('msg_id')
#     text = str()
#     if call.data == 'yes':
#         await db.delete_users()
#         text = "Baza tozalandi!"
#     elif call.data == 'no':
#         text = "Bekor qilindi."
#     await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
#     await state.clear()


async def download_and_save_file(file_id: str, save_path: str):
    file_info = await bot.get_file(file_id)
    file_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    await bot.download_file(file_info.file_path, file_path)

    return file_path


@router.message(IsBotAdminFilter(ADMINS), Command("admins"))
async def admins_main(message: types.Message):
    telegram_id = message.from_user.id
    # Users jadvalidan game_on ustunini FALSE holatiga tushirish
    await db.edit_status_users(
        game_on=False, telegram_id=telegram_id
    )
    # Results jadvalidan user ma'lumotlarini tozalash
    await db.delete_from_results(
        telegram_id=telegram_id
    )
    # Temporary answers jadvalidan user ma'lumotlarini tozalash
    await db.delete_from_temporary(
        telegram_id=telegram_id
    )
    # Counter jadvalidan hisoblagichni tozalash
    await db.delete_from_counter(
        telegram_id=telegram_id
    )
    buttons = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Savollar qo'shish")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(
        text="Kerakli bo'limni tanlang", reply_markup=buttons
    )


@router.message(IsBotAdminFilter(ADMINS), F.text == "Savollar qo'shish")
async def start_state_add_db(message: types.Message, state: FSMContext):
    await message.answer(
        text="Savol qo'shmoqchi bo'lgan kitobingizni tanlang",
        reply_markup=await battle_main_ibuttons(
            back_text="Ortga", back_callback="back_admin_main"
        )
    )
    await state.set_state(AdminState.add_question_one)


@router.callback_query(AdminState.add_question_one)
async def add_question(call: types.CallbackQuery, state: FSMContext):
    book_name = call.data
    await state.update_data(
        book_name=book_name
    )
    await call.message.edit_text(
        text="Savollar jamlangan excel hujjatni yuboring"
    )
    await state.set_state(AdminState.add_data_to_db)


@router.message(AdminState.add_data_to_db, F.document)
async def download_document(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        book_name = data['book_name']

        file_path = await download_and_save_file(
            file_id=message.document.file_id, save_path="downloads/"
        )
        df = pd.read_excel(file_path, sheet_name=0)
        c = 0
        for row in df.values:
            c += 1

            if c == 500:
                await asyncio.sleep(60)

            await db.add_question(
                table_number=book_name,
                question=row[0],
                a_correct=row[1],
                b=row[2],
                c=row[3],
                d=row[4]
            )
        await message.answer(
            text=f"Ma'lumotlar qabul qilindi!\n\nQabul qilingan savollar soni: {c} ta"
        )
        os.remove(file_path)

    except Exception as err:
        await message.answer(
            text=f"{err}"
        )
    await state.clear()


@router.message(IsBotAdminFilter(ADMINS), F.text == "Add book")
async def add_book(message: types.Message, state: FSMContext):
    await message.answer(
        text="Savollar beriladigan kitob nomini kiriting"
    )
    await state.set_state(AdminState.add_book_to_db)


@router.message(AdminState.add_book_to_db)
async def add_book_to_db(message: types.Message, state: FSMContext):
    book_name = message.text

    try:
        add_to_table = await db.add_table(table_name=book_name)
        await db.create_table_questions(table_name=f"Table_{add_to_table['id']}")

        await message.answer(
            text=f"Kitob {book_name} qo'shildi"
        )
        await state.clear()
    except Exception as err:
        await message.answer(
            text=f"{err}"
        )
