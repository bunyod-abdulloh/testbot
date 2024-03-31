from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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

