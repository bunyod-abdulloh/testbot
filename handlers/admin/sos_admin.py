from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils import keyboard

from data.config import GROUP_ID
from filters import ChatTypeFilter
from filters.is_group import IsAdmin
from keyboards.inline.sos import questions_main, get_questions_by_user
from loader import db, bot
from states.test import AdminSOS

router = Router()
router.message.filter(ChatTypeFilter(["supergroup"]), IsAdmin())


@router.message(Command("view"))
async def savollar_view(message: types.Message):
    await message.answer(
        text="Savollar bo'limi", reply_markup=await questions_main()
    )


@router.callback_query(F.data.startswith("get_question:"))
async def savollar_view_(callback_query: types.CallbackQuery):
    telegram_id = callback_query.data.split(":")[1]
    questions = await db.select_questions_sos(
        telegram_id=telegram_id
    )
    for question in questions:
        await callback_query.message.answer(
            text=f"Sana: {question['created_at']}\n\n{question['question']}",
            reply_markup=await get_questions_by_user(
                question_id=question['id']
            )
        )


@router.callback_query(F.data.startswith("admin_question:"))
async def foydalanuvchi_savoli(callback_query: types.CallbackQuery, state: FSMContext):
    question_id = int(callback_query.data.split(':')[1])
    question = await db.select_questions_by_id(
        id_=question_id
    )
    await callback_query.message.answer(
        text=f"Savol: {question['question']}"
             f"\n\nJavobingizni kiriting"
        )
    await state.update_data(
        question_id=question_id
    )
    await state.set_state(state=AdminSOS.one)


@router.message(StateFilter(AdminSOS.one))
async def admin_javobi(message: types.Message, state: FSMContext):
    print("message 56")
    await state.update_data(
        admin_answer=message.text
    )
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(
                text="✅ Tasdiqlash", callback_data="admin_check_"
            ),
            types.InlineKeyboardButton(
                text="♻️ Qayta kiritish", callback_data="admin_repeat_"
            )
        ]]
    )
    await message.answer(
        text="Javobingiz qabul qilindi! Tasdiqlaysizmi?", reply_markup=markup
    )


@router.callback_query(F.data == "admin_check_")
async def tasdiqlash_va_yuborish(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    question_id = int(data['question_id'])
    admin_answer = data['admin_answer']
    get_id = await db.select_questions_by_id(
        id_=question_id
    )
    try:
        await bot.send_message(
            chat_id=get_id['telegram_id'],
            text=f"Sizning savolingiz: {get_id['question']}\n\nAdmin javobi: {admin_answer}"
        )
        await callback_query.message.answer(
            text="Javob foydalanuvchiga yuborildi!"
        )
    except Exception as err:
        await callback_query.message.answer(
            text=f"{err}"
        )



