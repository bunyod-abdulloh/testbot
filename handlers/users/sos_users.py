from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from data.config import GROUP_ID
from keyboards.inline.sos import sos_check
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
        text="Habaringiz qabul qilindi! Tasdiqlaysizmi?", reply_markup=sos_check
    )


@router.callback_query(F.data == "sos_yes")
async def savol_va_takliflar_tasdiq(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_message = data.get('user_message')
    await db.add_question_sos(
        telegram_id=callback_query.from_user.id, full_name=callback_query.from_user.full_name, question=user_message
    )
    await bot.send_message(
        chat_id=GROUP_ID,
        text="Botga yangi habar qabul qilindi! Ko'rish uchun /view buyrug'ini kiriting!"
    )
    await callback_query.message.edit_text(
        text="Habaringiz qabul qilindi! Adminlarimiz tez orada javob berishga harakat qiladilar!"
    )
    await state.clear()


@router.callback_query(F.data == "sos_again")
async def savol_va_takliflar_qayta(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(
        text="Habaringizni qayta kiriting"
    )
    await state.clear()
    await state.set_state(UserSOS.one)
