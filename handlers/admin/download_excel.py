import asyncpg
from aiogram import Router, types, F

from handlers.admin.main import books_menu
from loader import db
from filters.admin import IsBotAdminFilter
from data.config import ADMINS
from utils.pgtoexcel import export_to_excel

router = Router()

admin = int(ADMINS[0])


@router.message(F.text == '📥 Excel shaklda yuklab olish', IsBotAdminFilter(ADMINS))
async def get_all_users(message: types.Message):
    await message.answer(
        text="Kerakli kitobni tanlang", reply_markup=await books_menu(
            callback_text="download_book"
        )
    )


@router.callback_query(F.data.startswith("download_book:"))
async def download_book(call: types.CallbackQuery):
    kitob_id = int(call.data.split(":")[1])
    kitob_nomi = await db.select_book_by_id(
        id_=kitob_id
    )
    if kitob_nomi['questions'] is False:
        await call.message.edit_text(
            text=f"Kitob {kitob_nomi['table_name']} ga hozircha savollar kiritilmagan!"
        )
    else:
        all_questions = await db.select_all_questions_(
            table_name=f"table_{kitob_id}"
        )
        kitob_nomi_ = kitob_nomi['table_name'].replace("|", "_").replace(" ", "_")
        file_path = f"downloads/documents/{kitob_nomi_}.xlsx"
        await export_to_excel(data=all_questions, headings=[f"{kitob_nomi['table_name']}", "A | CORRECT", "B", "C", "D"],
                              filepath=file_path)

        await call.message.answer_document(types.input_file.FSInputFile(file_path))
