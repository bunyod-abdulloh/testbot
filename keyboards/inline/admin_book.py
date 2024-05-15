from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_yes_no = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="✅ Yes", callback_data="yesadmin"),
        InlineKeyboardButton(text="❌ No", callback_data="noadmin")
    ]]
)
