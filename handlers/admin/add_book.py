import os

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from filters import IsBotAdminFilter
from keyboards.inline.admin_book import admin_yes_no
from loader import bot, db
from states import AdminState

router = Router()


async def download_and_save_file(file_id: str, save_path: str):
    file_info = await bot.get_file(file_id)
    file_path = os.path.join(save_path, file_info.file_path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    await bot.download_file(file_info.file_path, file_path)

    return file_path


@router.message(IsBotAdminFilter(ADMINS), F.text == "➕ Kitob qo'shish")
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
        await state.update_data(
            book_id=add_to_table['id']
        )
        await message.answer(
            text=f"Kitob {book_name} ma'lumotlar omboriga qo'shildi! Kitobga izoh kiritasizmi?",
            reply_markup=admin_yes_no
        )
        await state.set_state(AdminState.comment_main)
    except Exception as err:
        await message.answer(
            text=f"{err}"
        )
        await state.clear()


@router.callback_query(AdminState.comment_main)
async def comment_one(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yesadmin":
        await callback_query.message.edit_text(
            text="Izohingizni kiriting"
        )
        await state.set_state(AdminState.comment_one)
    elif callback_query.data == "noadmin":
        await callback_query.message.edit_text(
            text="Rahmat!"
        )
        await state.clear()


@router.message(AdminState.comment_one)
async def comment_two(message: types.Message, state: FSMContext):
    await state.update_data(
        comment_one=message.text
    )
    await message.answer(
        text="Izohingiz qabul qilindi! Yana izoh kiritasizmi?", reply_markup=admin_yes_no
    )
    await state.set_state(AdminState.comment_two)


@router.callback_query(AdminState.comment_two)
async def comment_three(callback_query: types.CallbackQuery, state: FSMContext):

    if callback_query.data == "yesadmin":
        await callback_query.message.edit_text(
            text="Izohingiz qabul qilindi! Yana izoh kiritasizmi?", reply_markup=admin_yes_no
        )
        await state.set_state(AdminState.comment_three)
    elif callback_query.data == "noadmin":
        data = await state.get_data()
        comment_one_ = data.get('comment_one')
        book_id = data.get('book_id')
        await db.update_book_comments(
            comment_one=comment_one_, comment_two=None, comment_three=None, book_id=book_id
        )
        await callback_query.message.edit_text(
            text="Izohingiz qabul qilindi va kitobga biriktirildi!"
        )
        await state.clear()


@router.message(AdminState.comment_three)
async def comment_three_func(message: types.Message, state: FSMContext):
    await state.update_data(
        comment_two=message.text
    )
    await message.answer(
        text="Izohingiz qabul qilindi! Yana izoh kiritasizmi?", reply_markup=admin_yes_no
    )
    await state.set_state(AdminState.comment_four)


@router.callback_query(AdminState.comment_four)
async def comment_four(callback_query: types.CallbackQuery, state: FSMContext):

    if callback_query.data == "yesadmin":
        await callback_query.message.edit_text(
            text="Izohingiz qabul qilindi! Yana izoh kiritasizmi?", reply_markup=admin_yes_no
        )
        await state.set_state(AdminState.comment_five)
    elif callback_query.data == "noadmin":
        data = await state.get_data()
        comment_one_ = data.get('comment_one')
        comment_two_ = data.get('comment_two')
        book_id = data.get('book_id')
        await db.update_book_comments(
            comment_one=comment_one_, comment_two=comment_two_, comment_three=None, book_id=book_id
        )
        await callback_query.message.edit_text(
            text="Izohingiz qabul qilindi va kitobga biriktirildi!"
        )
        await state.clear()


@router.message(AdminState.comment_five)
async def comment_five(message: types.Message, state: FSMContext):
    data = await state.get_data()
    comment_one_ = data.get('comment_one')
    comment_two_ = data.get('comment_two')
    comment_three_ = message.text
    book_id = data.get('book_id')
    await db.update_book_comments(
        comment_one=comment_one_, comment_two=comment_two_, comment_three=comment_three_, book_id=book_id
    )
    await message.answer(
        text="Izohingiz qabul qilindi va kitobga biriktirildi!"
    )
    await state.clear()
