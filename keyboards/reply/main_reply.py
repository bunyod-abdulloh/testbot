from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_button(competition: str, rating: str, manual: str):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"⚔️ {competition}")
            ],
            [
                KeyboardButton(text=f"📊 {rating}"),
                KeyboardButton(text=f"ℹ️ {manual}")
            ]
        ],
        resize_keyboard=True
    )
    return markup
