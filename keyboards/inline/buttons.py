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
