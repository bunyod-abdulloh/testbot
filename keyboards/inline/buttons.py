import random

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, SwitchInlineQueryChosenChat, CallbackGame
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


class BattleCallback(CallbackData, prefix="battle"):
    book_name: str
    random: str
    # offer: str


class OfferCallback(CallbackData, prefix="random_opponent"):
    agree_id: int
    book_id: int


class StartPlayingCallback(CallbackData, prefix="start_playing"):
    book_id: int
    battle_id: int


class QuestionsCallback(CallbackData, prefix="questions"):
    question_id: int
    a_correct: str
    b: str
    c: str
    d: str


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
                InlineKeyboardButton(text=f"😊 {offer_opponent}",
                                     callback_data="olma")
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


def to_offer_ibuttons(agree_text: str, agree_id: int, refusal_text: str, book_id: int):

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


def play_battle_ibuttons(start_text: str, book_id: int, battle_id: int):
    callback_factory = StartPlayingCallback(book_id=book_id, battle_id=battle_id)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🚀 {start_text}", callback_data=callback_factory.pack())
            ]
        ]
    )
    return markup


def questions_ibuttons():
    questions = ["a_correct", "b", "c", "d"]
    random.shuffle(questions)
    letters = ["A", "B", "C", "D"]

    questions_ = zip(letters, questions)

    builder = InlineKeyboardBuilder()
    for letter, question in questions_:
        builder.add(
            InlineKeyboardButton(
                text=f"{letter}", callback_data=f"question:{question}"
            )
        )
    builder.adjust(2, 2)
    return builder.as_markup()

