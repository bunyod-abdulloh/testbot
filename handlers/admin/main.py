from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard

from data.config import ADMINS
from filters import IsBotAdminFilter
from handlers.users.start import uz_start_buttons
from loader import db

router = Router()


def raqamni_ochir(matn):
    print(matn)
    if matn[2].isdigit() and matn[3] == '.':
        matn = matn[5:]
    if matn[1].isdigit() and matn[2] == '.':
        matn = matn[4:]
    if matn[0].isdigit() and matn[1] == '.':
        matn = matn[3:]
    return matn


async def test_qoshish(savollar: list, kitob_nomi: str, kalit_javoblar: list):
    try:
        savol = savollar[0].replace("\nB)", " B)").replace("\nC)", " C)").replace("\nD)", " D)").replace(
            '”\n“', '" "').replace("\nB:", " B:").replace("\nWe _____", " We _____").replace("\nA:", " A:").replace(
            " \nA)", " A)").replace(" \nB)", " B)").replace(" \nC)", " C)").replace(" \nD)", " D)").replace(
            "\n B)", " B)").replace("\n C)", " C)").replace("\n D)", " D)")
        tayyor_savollar = savol.split("\n")

        savollar_ = [question for i, question in enumerate(tayyor_savollar) if i % 2 == 0]
        raqamsiz_savollar = []
        for n in savollar_:
            raqamsiz_savollar.append(raqamni_ochir(n))

        javoblar = [question for i, question in enumerate(tayyor_savollar) if i % 2 == 1]

        answers = kalit_javoblar[0].split()

        # Harflar uchun yangi ro'yxat
        togri_javoblar = []

        # Javoblar ro'yxatidan harflarni ajratish
        for answer in answers:
            letter = answer.split('-')[1]
            togri_javoblar.append(letter)

        savol_javob = []
        for savol, togri_javob, variantlar in zip(raqamsiz_savollar, togri_javoblar, javoblar):
            savol_javob.append((savol, togri_javob, variantlar))

        count = 0

        for savol, togri_javob, variantlar in savol_javob:
            count += 1
            if togri_javob == "A":
                a_ = variantlar.split("A)")
                t_javob = a_[1].split("B)")[0].lstrip()
                b_ = variantlar.split("B)")
                b = b_[1].split("C)")[0].lstrip()
                c_ = variantlar.split("C)")
                c = c_[1].split("D)")[0].lstrip()
                d = variantlar.split("D)")[1].lstrip()
                await db.add_question(
                    table_name=kitob_nomi, question=savol,
                    a_correct=t_javob, b=b, c=c, d=d
                )

            if togri_javob == "B":
                a_ = variantlar.split("A)")
                a = a_[1].split("B)")[0].lstrip()
                b_ = variantlar.split("B)")
                t_javob = b_[1].split("C)")[0].lstrip()
                c_ = variantlar.split("C)")
                c = c_[1].split("D)")[0].lstrip()
                d = variantlar.split("D)")[1].lstrip()
                await db.add_question(
                    table_name=kitob_nomi, question=savol,
                    a_correct=t_javob, b=a, c=c, d=d
                )

            if togri_javob == "C":
                a_ = variantlar.split("A)")
                a = a_[1].split("B)")[0].lstrip()
                b_ = variantlar.split("B)")
                b = b_[1].split("C)")[0].lstrip()
                c_ = variantlar.split("C)")
                t_javob = c_[1].split("D)")[0].lstrip()
                d = variantlar.split("D)")[1].lstrip()
                await db.add_question(
                    table_name=kitob_nomi, question=savol,
                    a_correct=t_javob, b=b, c=a, d=d
                )

            if togri_javob == "D":
                a_ = variantlar.split("A)")
                a = a_[1].split("B)")[0].lstrip()
                b_ = variantlar.split("B)")
                b = b_[1].split("C)")[0].lstrip()
                c_ = variantlar.split("C)")
                c = c_[1].split("D)")[0].lstrip()
                t_javob = variantlar.split("D)")[1].lstrip()
                await db.add_question(
                    table_name=kitob_nomi, question=savol,
                    a_correct=t_javob, b=b, c=c, d=a
                )
        return count
    except Exception as e:
        print(e)


async def books_menu(callback_text):
    all_books = await db.select_all_tables()

    builder = keyboard.InlineKeyboardBuilder()

    for book in all_books:
        builder.add(
            types.InlineKeyboardButton(
                text=f"{book['table_name']}", callback_data=f"{callback_text}:{book['id']}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()


@router.message(IsBotAdminFilter(ADMINS), Command("admins"))
async def admins_main(message: types.Message):
    telegram_id = message.from_user.id
    # Users jadvalidan game_on ustunini FALSE holatiga tushirish
    await db.edit_status_users(
        game_on=False, telegram_id=telegram_id
    )
    # Results jadvalidan user ma'lumotlarini tozalash
    await db.delete_from_results(
        telegram_id=telegram_id
    )
    # Temporary answers jadvalidan user ma'lumotlarini tozalash
    await db.delete_from_temporary(
        telegram_id=telegram_id
    )
    # Counter jadvalidan hisoblagichni tozalash
    await db.delete_from_counter(
        telegram_id=telegram_id
    )
    buttons = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="Kitob qo'shish"),
                types.KeyboardButton(text="Savollar qo'shish")
            ],
            [
                types.KeyboardButton(text="Kitob nomini o'zgartirish")
            ],
            [
                types.KeyboardButton(text="🔙 Bosh sahifa")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer(
        text="Kerakli bo'limni tanlang", reply_markup=buttons
    )


@router.message(F.text == "🔙 Bosh sahifa")
async def back_admin_main(message: types.Message, state: FSMContext):
    await message.answer(
        text="Bosh sahifa", reply_markup=uz_start_buttons
    )
    await state.clear()
