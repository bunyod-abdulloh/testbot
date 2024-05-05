from aiogram import Router, F, types

from handlers.admin.main import books_menu

router = Router()


@router.message(F.text == "Kitob nomini o'zgartirish")
async def admin_edit_book_name(message: types.Message):
    await message.answer(
        text="O'zgartirmoqchi bo'lgan kitobingizni tanlang",
        reply_markup=await books_menu(
            callback_text="edit_book"
        )
    )
