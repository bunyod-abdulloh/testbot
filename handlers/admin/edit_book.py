from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from handlers.admin.main import books_menu
from loader import db
from states import AdminState

router = Router()


@router.message(F.text == "♻️ Kitob nomini o'zgartirish")
async def admin_edit_book_name(message: types.Message):
    await message.answer(
        text="O'zgartirmoqchi bo'lgan kitobingizni tanlang",
        reply_markup=await books_menu(
            callback_text="edit_book"
        )
    )


@router.callback_query(F.data.startswith("edit_book:"))
async def edit_book(call: types.CallbackQuery, state: FSMContext):
    kitob_id = int(call.data.split(":")[1])
    await state.update_data(
        edit_book_id=kitob_id
    )
    kitob_nomi = await db.select_book_by_id(
        id_=kitob_id
    )
    print(kitob_nomi)
    await call.message.edit_text(
        text=f"Tanlangan kitob: {kitob_nomi['table_name']}"
             f"\n\nKitob uchun yangi nom kiriting"
    )
    await state.set_state(AdminState.edit_book)


@router.message(AdminState.edit_book)
async def edit_book_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    kitob_id = data.get('edit_book_id')
    yangi_nom = message.text

    await db.update_book_name(
        book_id=kitob_id, new_name=yangi_nom
    )
    await message.answer(
        text=f"Kitob {yangi_nom} ga o'zgartirildi"
    )
    await state.clear()
