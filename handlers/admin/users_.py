from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from filters import IsBotAdminFilter
from keyboards.inline.buttons import are_you_sure_markup
from loader import db, bot
from states import AdminState

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
        text=message.text, reply_markup=buttons
    )


@router.message(F.text == "🕶 Foydalanuvchilar soni")
async def admin_users_count(message: types.Message):
    count = await db.count_users()
    await message.answer(
        text=f"Foydalanuvchilar soni: {count} ta"
    )


@router.message(F.text == "❌ Nofaol foydalanuvchilarni o'chirish")
async def admin_delete_users(message: types.Message):
    nofaollar_soni = await db.nofaollarni_sana()

    await db.nofaollarni_ochir()

    await message.answer(
        text=f"{nofaollar_soni} ta nofaol foydalanuvchilar ma'lumotlar omboridan o'chirildi"
    )


@router.message(F.text == "✉️ Habar yuborish")
async def admin_send_message(message: types.Message):
    pass


@router.message(F.text == "🔙 Ortga")
async def back_admin_main(message: types.Message):
    pass


@router.message(Command('reklama'), IsBotAdminFilter(ADMINS))
async def ask_ad_content(message: types.Message, state: FSMContext):
    await message.answer("Reklama uchun post yuboring")
    await state.set_state(AdminState.ask_ad_content)


@router.message(AdminState.ask_ad_content, IsBotAdminFilter(ADMINS))
async def send_ad_to_users(message: types.Message, state: FSMContext):
    users = await db.select_all_users()
    count = 0
    for user in users:
        user_id = user[-1]
        try:
            await message.send_copy(chat_id=user_id)
            count += 1
            await asyncio.sleep(0.05)
        except Exception as error:
            logging.info(f"Ad did not send to user: {user_id}. Error: {error}")
    await message.answer(text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi.")
    await state.clear()


@router.message(Command('cleandb'), IsBotAdminFilter(ADMINS))
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
        await db.delete_users()
        text = "Baza tozalandi!"
    elif call.data == 'no':
        text = "Bekor qilindi."
    await bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=msg_id)
    await state.clear()
