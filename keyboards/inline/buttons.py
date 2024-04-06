from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


class BattleCallback(CallbackData, prefix="battle"):
    book_name: str
    random: str
    # offer: str


class OfferCallback(CallbackData, prefix="random_opponent"):
    agree_id: int
    book_id: str


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


def battle_ibuttons(random_opponent: str, offer_opponent: str, playing_alone: str, alone_callback: str,
                    back: str, back_callback: str, book_id: str):

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"😎 {random_opponent}", callback_data=f"book_id:{book_id}")
            ],
            [
                InlineKeyboardButton(text=f"😊 {offer_opponent}", callback_data="da")
            ],
            [
                InlineKeyboardButton(text=f"🥷 {playing_alone}", callback_data=f"alone:{alone_callback}")
            ],
            [
                InlineKeyboardButton(text=f"⬅️ {back}", callback_data=f"{back_callback}")
            ]
        ]
    )
    return markup


def to_offer_ibuttons(agree_text: str, agree_id: int, refusal_text: str, book_id: str):

    callback_factory = OfferCallback(agree_id=agree_id, book_id=book_id)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🎮 {agree_text}", callback_data=callback_factory.pack())
            ],
            [
                InlineKeyboardButton(text=f"❌ {refusal_text}", callback_data=callback_factory.pack())
            ]
        ]
    )
    return markup
