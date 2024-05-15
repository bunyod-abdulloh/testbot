from aiogram import Router, F, types

from handlers.admin.main import books_menu
from loader import db

router = Router()


@router.message(F.text == "🆑 Kitob o'chirish")
async def admin_delete_book(message: types.Message):
    await message.answer(
        text="O'chirmoqchi bo'lgan kitobingizni tanlang",
        reply_markup=await books_menu(
            callback_text="delete_book"
        )
    )


@router.callback_query(F.data.startswith("delete_book:"))
async def delete_book(call: types.CallbackQuery):
    kitob_id = int(call.data.split(':')[1])
    try:
        await db.drop_table_book(
            table_name=f"table_{kitob_id}"
        )
        await db.delete_book_tables(
            id_=kitob_id
        )
        await call.message.edit_text(
            text="Kitob o'chirildi"
        )
    except Exception as e:
        await call.message.edit_text(
            text=f"{e}"
        )

