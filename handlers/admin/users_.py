import asyncio
from datetime import datetime
import os

from aiogram import Router, F, types
from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from filters import IsBotAdminFilter
from keyboards.inline.buttons import are_you_sure_markup
from keyboards.reply.admin_buttons import users_main_kb, admin_main_kb
from loader import db, bot
from states import AdminState
from utils.pgtoexcel import export_to_excel

router = Router()


@router.message(F.text == "👤 Foydalanuvchilar bo'limi")
async def admin_users_main(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=users_main_kb
    )


@router.message(F.text == "Foydalanuvchilar soni")
async def admin_users_count(message: types.Message):
    count = await db.count_users()
    await message.answer(
        text=f"Foydalanuvchilar soni: {count} ta"
    )


@router.message(F.text == "Nofaol foydalanuvchilarni o'chirish")
async def admin_delete_users(message: types.Message):
    nofaollar_soni = await db.nofaollarni_sana()

    await db.nofaollarni_ochir()

    await message.answer(
        text=f"{nofaollar_soni} ta nofaol foydalanuvchilar ma'lumotlar omboridan o'chirildi"
    )


@router.message(F.text == "🔙 Ortga")
async def back_admin_main(message: types.Message):
    await message.answer(
        text=message.text, reply_markup=admin_main_kb
    )


@router.message(F.text == "Habar yuborish", IsBotAdminFilter(ADMINS))
async def ask_ad_content(message: types.Message, state: FSMContext):
    await message.answer("Habar uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)


@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
async def send_ad_to_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    all_users = 0
    active = 0
    blocked = 0
    for user in users:
        all_users += 1
        user_id = user['telegram_id']
        try:
            await message.send_copy(chat_id=user_id)
            active += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            blocked += 1
            await db.aktivlikni_yangila(
                status=False, telegram_id=user_id
            )
            logger.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"Habar {active} ta foydalauvchiga muvaffaqiyatli yuborildi."
                              f"\n\nJami foydalanuvchilar soni: {all_users}"
                              f"\nFaol foydalanuvchilar soni: {active}"
                              f"\nNofaol foydalanuvchilar soni: {blocked}")
    await state.clear()


@router.message(F.text == "Foydalanuvchilar omborini tozalash", IsBotAdminFilter(ADMINS))
async def ask_are_you_sure(message: types.Message, state: FSMContext):
    msg = await message.reply("Haqiqatdan ham bazani tozalab yubormoqchimisiz?", reply_markup=are_you_sure_markup)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminState.are_you_sure)


@router.callback_query(AdminState.are_you_sure, IsBotAdminFilter(ADMINS))
async def clean_db(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get('msg_id')
    text = str()
    if call.data == 'yes':
        await db.hamma_userlarni_ochir()
        text = "Baza tozalandi!"
    elif call.data == 'no':
        text = "Bekor qilindi."
    await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
    await state.clear()


@router.message(F.text == "Barchani blockdan chiqarish")
async def unblock_all_users(message: types.Message):
    nofaollar_soni = await db.nofaollarni_sana()
    await db.update_all_active()
    await message.answer(
        text=f"{nofaollar_soni} ta foydalanuvchilar blokdan chiqarildi!"
    )


@router.message(F.text == "🔘 Excel yuklab olish")
async def download_users(message: types.Message):
    date = datetime.now().date()
    all_results = await db.select_all_results()
    file_path = f"downloads/RESULTS_{date}.xlsx"
    send_to_xls = list()
    for n in all_results:
        created_at = str(n['created_at'])
        telegram_id = n['telegram_id']
        get_fullname = await db.select_user(
            telegram_id=n['telegram_id']
        )
        full_name = get_fullname['full_name']
        get_book = await db.select_book_by_id(
            id_=n['book_id']
        )
        book_name = get_book['table_name']
        result = str(n['result'])
        send_to_xls.append([created_at, telegram_id, full_name, book_name, result])
    await export_to_excel(data=send_to_xls, headings=["CREATED_AT", "TELEGRAM_ID", "FULL_NAME", "BOOK_NAME", "RESULT"],
                          filepath=file_path)
    await message.answer_document(document=types.input_file.FSInputFile(file_path),
                                  caption="Foydalanuvchilar va ularning natijalari to'g'risidagi jadval")
    os.remove(file_path)
