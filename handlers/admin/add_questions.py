import asyncio
import os

import pandas as pd
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from filters import IsBotAdminFilter
from handlers.admin.add_book import download_and_save_file
from handlers.admin.main import books_menu, test_qoshish
from loader import db
from states import AdminState
from states.test import GetTest

router = Router()


@router.message(IsBotAdminFilter(ADMINS), F.text == "➕ Savollar qo'shish")
async def start_state_add_db(message: types.Message):
    await message.answer(
        text="Savol qo'shmoqchi bo'lgan kitobingizni tanlang",
        reply_markup=await books_menu(
            callback_text="admin"
        )
    )


@router.callback_query(F.data.startswith("admin:"))
async def admin_add_question(call: types.CallbackQuery):
    book_id = call.data.split(':')[1]
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Excel shaklda", callback_data=f"add_excel:{book_id}"
                ),
                types.InlineKeyboardButton(
                    text="PDFdan copy/paste", callback_data=f"add_pdf:{book_id}"
                )
            ]
        ]
    )
    await call.message.edit_text(
        text="Test kiritish turini tanlang", reply_markup=markup
    )


@router.callback_query(F.data.startswith("add_excel:"))
async def add_excel(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(
        book_id=call.data.split(":")[1]
    )
    await call.message.edit_text(
        text="Savollar jamlangan excel hujjatni yuboring"
    )
    await state.set_state(AdminState.add_excel)


@router.message(AdminState.add_excel, F.document)
async def download_document(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        book_id = int(data['book_id'])

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
                table_name=f"table_{book_id}",
                question=row[0],
                a_correct=row[1],
                b=row[2],
                c=row[3],
                d=row[4]
            )
        await db.update_questions_status(
            book_id=book_id
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


@router.callback_query(F.data.startswith("add_pdf:"))
async def admin_add_pdf(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(
        book_id=call.data.split(":")[1]
    )
    await call.message.edit_text(
        text="Test javoblarini yuboring"
    )
    await state.set_state(GetTest.one)


@router.message(GetTest.one)
async def get_test_two(message: types.Message, state: FSMContext):
    test_javoblari = [message.text]

    await state.update_data(
        test_javoblari=test_javoblari
    )
    await message.answer(
        text="Javoblar qabul qilindi! Test savollarini yuboring"
    )
    await state.set_state(GetTest.two)


@router.message(GetTest.two)
async def get_test_three(message: types.Message, state: FSMContext):
    data = await state.get_data()
    test_savollari = [message.text]
    kitob_id = data.get('book_id')

    kalit_javoblar = data.get('test_javoblari')
    add_and_count = await test_qoshish(
        savollar=test_savollari, kitob_nomi=f"table_{kitob_id}", kalit_javoblar=kalit_javoblar
    )
    await message.answer(
        text=f"Jami {add_and_count} ta test savollari qabul qilindi!"
    )
    await state.clear()
