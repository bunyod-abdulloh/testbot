from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from filters import ChatTypeFilter
from filters.is_group import IsAdmin
from keyboards.inline.sos import questions_main, get_questions_by_user
from loader import db, bot
from states.test import AdminSOS

router = Router()
router.message.filter(ChatTypeFilter(["supergroup"]), IsAdmin())


@router.message(Command("view"))
async def savollar_view(message: types.Message, state: FSMContext):
    await state.clear()
    get_questions = await db.select_distinct_sos()
    if not get_questions:
        await message.answer(
            text="Hozircha savollar mavjud emas!"
        )
    else:
        await message.answer(
            text="Savollar bo'limi", reply_markup=await questions_main()
        )


@router.callback_query(F.data.startswith("get_question:"))
async def savollar_view_(callback_query: types.CallbackQuery):
    telegram_id = callback_query.data.split(":")[1]
    questions = await db.select_questions_sos(
        telegram_id=telegram_id
    )
    await callback_query.message.delete()
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
    await callback_query.message.edit_text(
        text=f"<b>Savol:</b>\n\n{question['question']}"
             f"\n\nJavobingizni kiriting"
    )
    await state.update_data(
        question_id=question_id
    )
    await state.set_state(state=AdminSOS.one)


@router.message(StateFilter(AdminSOS.one))
async def admin_javobi(message: types.Message, state: FSMContext):
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
    telegram_id = get_id['telegram_id']
    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>Sizning savolingiz:</b>\n\n{get_id['question']}\n\n<b>Admin javobi:</b>\n\n{admin_answer}"
        )
        await callback_query.answer(
            text="Javob foydalanuvchiga yuborildi!", show_alert=True
        )
        await db.delete_from_sos(
            id_=question_id
        )
        questions = await db.select_questions_sos(
            telegram_id=telegram_id
        )
        await callback_query.message.delete()
        if questions:
            for question in questions:
                await callback_query.message.answer(
                    text=f"Sana: {question['created_at']}\n\n{question['question']}",
                    reply_markup=await get_questions_by_user(
                        question_id=question['id']
                    )
                )
        else:
            get_questions = await db.select_distinct_sos()
            if not get_questions:
                await callback_query.message.answer(
                    text="Hozircha savollar mavjud emas!"
                )
            else:
                await callback_query.message.answer(
                    text="Savollar bo'limi", reply_markup=await questions_main()
                )
        await state.clear()
    except Exception as err:
        await callback_query.message.answer(
            text=f"{err}"
        )


@router.callback_query(F.data == "admin_repeat_")
async def qayta_kiritish(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    question_id = int(data['question_id'])
    question = await db.select_questions_by_id(
        id_=question_id
    )
    await callback_query.message.edit_text(
        text=f"<b>Savol:</b>\n\n{question['question']}"
             f"\n\nJavobingizni kiriting"
    )
    await state.set_state(state=AdminSOS.one)


@router.callback_query(F.data.startswith("delete_question:"))
async def admin_delete_question(callback_query: types.CallbackQuery):
    question_id = int(callback_query.data.split(":")[1])
    await db.delete_from_sos(
        id_=question_id
    )
    await callback_query.answer(
        text="Savol bazadan o'chirildi!", show_alert=True
    )
    await callback_query.message.delete()
    get_questions = await db.select_distinct_sos()
    if not get_questions:
        await callback_query.message.answer(
            text="Hozircha savollar mavjud emas!"
        )


@router.callback_query(F.data == "back_questions")
async def admin_back_questions(callback_query: types.CallbackQuery):
    get_questions = await db.select_distinct_sos()
    if not get_questions:
        await callback_query.message.edit_text(
            text="Hozircha savollar mavjud emas!"
        )
    else:
        await callback_query.message.edit_text(
            text="Savollar bo'limi", reply_markup=await questions_main()
        )
