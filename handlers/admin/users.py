from aiogram import Router, F, types

router = Router()


@router.message(F.text == "👤 Foydalanuvchilar bo'limi")
async def admin_users_main(message: types.Message):
    buttons = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="🕶 Foydalanuvchilar soni")
            ],
            [
                types.KeyboardButton(text="❌ Nofaol foydalanuvchilarni o'chirish")
            ],
            [
                types.KeyboardButton(text="✉️ Habar yuborish")
            ],
            [
                types.KeyboardButton(text="🔙 Ortga")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(
        text=message.text
    )


@router.message(F.text == "🕶 Foydalanuvchilar soni")
async def admin_users_count(message: types.Message):
    pass


@router.message(F.text == "❌ Nofaol foydalanuvchilarni o'chirish")
async def admin_delete_users(message: types.Message):
    pass


@router.message(F.text == "✉️ Habar yuborish")
async def admin_send_message(message: types.Message):
    pass


@router.message(F.text == "🔙 Ortga")
async def back_admin_main(message: types.Message):
    pass
