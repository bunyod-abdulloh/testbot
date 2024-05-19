from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


def check_user_ibuttons(status: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🧐 {status}", callback_data="status")
            ]
        ]
    )
    return markup


async def battle_main_ibuttons(back_text: str, back_callback: str):
    all_books = await db.select_all_tables()

    builder = InlineKeyboardBuilder()

    for book in all_books:
        if not book['questions']:
            pass
        else:
            builder.add(
                InlineKeyboardButton(
                    text=f"{book['table_name']}", callback_data=f"table_{book['id']}"
                )
            )
    builder.add(
        InlineKeyboardButton(text=f"⬅️ {back_text}", callback_data=f"{back_callback}")
    )
    builder.adjust(1)

    return builder.as_markup()


def battle_ibuttons(random_opponent: str, offer_opponent: str, playing_alone: str, back: str, back_callback: str,
                    book_id: str):

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"😎 {random_opponent}", callback_data=f"book_id:{book_id}")
            ],
            [
                InlineKeyboardButton(text=f"😊 {offer_opponent}", callback_data=f"with_friend:{book_id}")
            ],
            [
                InlineKeyboardButton(text=f"🥷 {playing_alone}", callback_data=f"alone:{book_id}:timer")
            ],
            [
                InlineKeyboardButton(text=f"⬅️ {back}", callback_data=f"{back_callback}")
            ]
        ]
    )
    return markup


def to_offer_ibuttons(agree_text: str, agree_id: int, refusal_text: str, book_id: int):

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🎮 {agree_text}", callback_data=f"agree:{agree_id}:{book_id}")
            ],
            [
                InlineKeyboardButton(text=f"❌ {refusal_text}", callback_data=f"refusal:{agree_id}")
            ]
        ]
    )
    return markup


def play_battle_ibuttons(start_text: str, book_id: int, battle_id: int):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🚀 {start_text}", callback_data=f"play_b:{book_id}:{battle_id}")
            ]
        ]
    )
    return markup


def bot_offer_ibuttons(full_name: str, bot_link: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🤖 Botdan foydalanish taklifini yuborish",
                    switch_inline_query=f"\n\nFoydalanuvchi {full_name} Sizni ilmiy bellashuvga taklif qilmoqda! "
                                        f"Manzil: {bot_link}"
                )
            ]
        ]
    )
    return markup


inline_keyboard = [[
    InlineKeyboardButton(text="✅ Yes", callback_data='yes'),
    InlineKeyboardButton(text="❌ No", callback_data='no')
]]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
