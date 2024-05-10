from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard

from data.config import ADMINS
from filters import IsBotAdminFilter
from handlers.users.start import uz_start_buttons
from keyboards.reply.admin_buttons import admin_tugmalari
from loader import db

router = Router()


async def books_menu(callback_text):
    all_books = await db.select_all_tables()

    builder = keyboard.InlineKeyboardBuilder()

    for book in all_books:
        builder.add(
            types.InlineKeyboardButton(
                text=f"{book['table_name']}", callback_data=f"{callback_text}:{book['id']}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()


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
    await message.answer(
        text="Kerakli bo'limni tanlang", reply_markup=admin_tugmalari
    )


@router.message(F.text == "🔙 Bosh sahifa")
async def back_admin_main(message: types.Message, state: FSMContext):
    await message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )
    await state.clear()
