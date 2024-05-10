from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import keyboard

from loader import db


def rating_main_kb():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Umumiy", callback_data="rating_overall"
                ),
                InlineKeyboardButton(
                    text="📖 Kitob bo'yicha", callback_data="rating_by_book"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Ortga", callback_data="back_battle_main"
                )
            ]
        ]
    )
    return markup


async def rating_books_kb():
    all_books = await db.select_all_tables()

    builder = keyboard.InlineKeyboardBuilder()

    for book in all_books:
        if not book['questions']:
            pass
        else:
            builder.add(
                InlineKeyboardButton(
                    text=f"{book['table_name']}", callback_data=f"rating:{book['id']}"
                )
            )
    builder.add(
        InlineKeyboardButton(
            text="⬅️ Ortga", callback_data="back_rating_main"
        )
    )
    builder.adjust(1)
    return builder.as_markup()


back_rating_main = InlineKeyboardMarkup(
    inline_keyboard=[[
            InlineKeyboardButton(
                text="⬅️ Ortga", callback_data="back_rating_main"
            )
        ]]
)
