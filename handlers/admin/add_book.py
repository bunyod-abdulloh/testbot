import os

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from filters import IsBotAdminFilter
from loader import bot, db
from states import AdminState

router = Router()


async def download_and_save_file(file_id: str, save_path: str):
    file_info = await bot.get_file(file_id)
    file_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    await bot.download_file(file_info.file_path, file_path)

    return file_path


@router.message(IsBotAdminFilter(ADMINS), F.text == "Kitob qo'shish")
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
            text=f"Kitob {book_name} ma'lumotlar omboriga qo'shildi"
        )
        await state.clear()
    except Exception as err:
        await message.answer(
            text=f"{err}"
        )
