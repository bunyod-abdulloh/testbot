from aiogram import types

admin_tugmalari = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text="➕ Kitob qo'shish"),
            types.KeyboardButton(text="➕ Savollar qo'shish")
        ],
        [
            types.KeyboardButton(text="♻️ Kitob nomini o'zgartirish"),
            types.KeyboardButton(text="🆑 Kitob o'chirish")
        ],
        [
            types.KeyboardButton(text="📥 Excel shaklda yuklab olish")
        ],
        [
            types.KeyboardButton(text="👤 Foydalanuvchilar bo'limi")
        ],
        [
            types.KeyboardButton(text="🔙 Bosh sahifa")
        ]
    ],
    resize_keyboard=True
)
