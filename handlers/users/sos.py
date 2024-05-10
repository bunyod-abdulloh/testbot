from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import ADMINS
from loader import db, bot
from states.test import UserSOS

router = Router()


@router.message(F.text == "❓ Savol va takliflar")
async def savol_va_takliflar(message: types.Message, state: FSMContext):
    await message.answer(
        text="Savol va takliflaringizni yuborishingiz mumkin! Faqat matnli habarlar qabul qilinadi!"
    )
    await state.set_state(UserSOS.one)


@router.message(UserSOS.one)
async def savol_va_takliflar_qabul(message: types.Message, state: FSMContext):
    await state.update_data(
        user_message=message.text
    )
    await message.answer(
        text="Habaringiz qabul qilindi! Tasdiqlaysizmi?"
    )


@router.callback_query(F.data == "sos_yes")
async def savol_va_takliflar_tasdiq(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_message = data.get('user_message')
    await db.add_question_sos(
        telegram_id=callback_query.from_user.id, question=user_message
    )
    for admin in ADMINS:
        await bot.send_message(
            chat_id=admin,
            text="Botga yangi habar qabul qilindi! Ko'rish uchun /view buyrug'ini kiriting!"
        )
    await callback_query.message.edit_text(
        text="Habaringiz qabul qilindi! Adminlarimiz tez orada javob berishga harakat qiladilar!"
    )
    await state.clear()


@router.callback_query(F.data == "sos_again")
async def savol_va_takliflar_qayta(message: types.Message, state: FSMContext):
    pass
