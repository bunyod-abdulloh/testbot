from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import keyboard

from loader import db

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


async def questions_main():
    get_questions = await db.select_distinct_sos()
    builder = keyboard.InlineKeyboardBuilder()

    for user in get_questions:
        builder.add(
            InlineKeyboardButton(
                text=f"{user['full_name']}", callback_data=f"get_question:{user['telegram_id']}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()


async def get_questions_by_user(question_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"✅ Javob berish", callback_data=f"admin_question:{question_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 O'chirish", callback_data=f"delete_question:{question_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga", callback_data=f"back_questions"
                )
            ]
        ]
    )
    return markup
