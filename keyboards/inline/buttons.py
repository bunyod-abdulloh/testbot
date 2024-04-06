from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


class BattleCallback(CallbackData, prefix="battle"):
    book_name: str
    random: str
    # offer: str


class OfferCallback(CallbackData, prefix="random_opponent"):
    recipient_id: str
    theme: str


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
                    back: str, back_callback: str, book_name: str):

    # random = BattleCallback(book_name=book_name, random="random")
    # offer = BattleCallback(book_name=book_name, offer="offer", random="0")

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"😎 {random_opponent}", callback_data=f"book_name_{book_name}")
            ],
            [
                InlineKeyboardButton(text=f"😊 {offer_opponent}", callback_data="da")
            ],
            [
                InlineKeyboardButton(text=f"🥷 {playing_alone}", callback_data=f"{alone_callback}")
            ],
            [
                InlineKeyboardButton(text=f"⬅️ {back}", callback_data=f"{back_callback}")
            ]
        ]
    )
    return markup


def to_offer_ibuttons(accedence_text: str, accedence_callback: str, theme: str, cancel_text: str):

    accedence_callback_ = OfferCallback(recipient_id=accedence_callback, theme=theme)
    # cancel_callback_ = OfferCallback(cancel_id=cancel_callback)

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🎮 {accedence_text}", callback_data=accedence_callback_.pack())
            ],
            [
                InlineKeyboardButton(text=f"❌ {cancel_text}", callback_data="sa")
            ]
        ]
    )
    return markup
