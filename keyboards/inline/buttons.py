from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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


def to_offer_ibuttons(accedence_text: str, accedence_callback: str, theme: str, cancel_text: str):

    accedence_callback_ = OfferCallback(recipient_id=accedence_callback, theme=theme)
    # cancel_callback_ = OfferCallback(cancel_id=cancel_callback)
    print(accedence_callback_.pack())
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
