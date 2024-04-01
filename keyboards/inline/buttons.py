from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class OfferCallback(CallbackData, prefix="offer"):
    offer_id: str = None
    recipient_id: str = None
    refusal: str = None


def check_user_ibuttons(status: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🧐 {status}", callback_data="status")
            ]
        ]
    )
    return markup


def battle_ibuttons(random_opponent: str, opponent_callback: str, rival_offer: str, offer_callback: str,
                    playing_alone: str, alone_callback: str, back: str, back_callback: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"😎 {random_opponent}", callback_data=f"{opponent_callback}")
            ],
            [
                InlineKeyboardButton(text=f"😊 {rival_offer}", callback_data=f"{offer_callback}")
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


def to_offer_ibuttons(playing: str, offer_id: str, refusal: str, callback_refusal: str):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"🎮 {playing}", callback_data=OfferCallback(offer_id=offer_id))
            ],
            [
                InlineKeyboardButton(text=f"❌ {refusal}", callback_data=f"{callback_refusal}")
            ]
        ]
    )
    return markup
