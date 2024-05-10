from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

sos_check = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(
                text="✅ Ha", callback_data="sos_yes"
            ),
        InlineKeyboardButton(
            text="🔁 Yo'q qayta", callback_data="sos_again"
        )
    ]]
)
