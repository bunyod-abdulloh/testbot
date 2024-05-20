from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Kitob va savollar qo'shish bo'limi")
        ],
        [
            KeyboardButton(text="👤 Foydalanuvchilar bo'limi")
        ],
        [
            KeyboardButton(text="📊 Natijalar bo'limi")
        ],
        [
            KeyboardButton(text="🔙 Bosh sahifa")
        ]
    ],
    resize_keyboard=True
)

books_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kitob qo'shish"),
            KeyboardButton(text="Savollar qo'shish")
        ],
        [
            KeyboardButton(text="Kitob nomini o'zgartirish"),
            KeyboardButton(text="Kitob o'chirish")
        ],
        [
            KeyboardButton(text="📥 Excel shaklda yuklab olish")
        ],
        [
            KeyboardButton(text="🔙 Ortga")
        ]
    ],
    resize_keyboard=True
)

users_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Foydalanuvchilar soni")
        ],
        [
            KeyboardButton(text="Nofaol foydalanuvchilarni o'chirish")
        ],
        [
            KeyboardButton(text="Foydalanuvchilar omborini tozalash"),
            KeyboardButton(text="Habar yuborish")
        ],
        [
            KeyboardButton(text="Barchani blockdan chiqarish")
        ],
        [
            KeyboardButton(text="🔘 Excel yuklab olish")
        ],
        [
            KeyboardButton(text="🔙 Ortga")
        ]
    ],
    resize_keyboard=True
)


results_main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Kunlik natijalar")
        ],
        [
            KeyboardButton(text="Haftalik natijalar")
        ],
        [
            KeyboardButton(text="Oylik natijalar")
        ],
        [
            KeyboardButton(text="🔙 Ortga")
        ]
    ],
    resize_keyboard=True
)
