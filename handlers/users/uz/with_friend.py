from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from handlers.users.uz.start import uz_start_buttons
from keyboards.inline.buttons import to_offer_ibuttons, bot_offer_ibuttons
from keyboards.reply.main_reply import rival_offer_cbutton
from loader import db, bot

router = Router()


@router.callback_query(F.data.startswith("with_friend:"))
async def with_friend_query(call: types.CallbackQuery, state: FSMContext):
    book_id = call.data.split(":")[1]
    await state.update_data(
        friend_book_id=book_id
    )

    await call.message.answer(
        text="Diqqat qiling!!! \n\nSiz taklif qilmoqchi bo'lgan do'stingiz botimiz foydalanuvchisi bo'lishi lozim! "
             "Faqat bitta do'stingizni taklif qilishingiz mumkin! Agar do'stingizdan javob kelmasa qayta "
             "<b>⚔️ Bellashuv</b> tugmasini bosib boshqa do'stingizni bellashuvga taklif qilishingiz "
             "mumkin!",
        reply_markup=rival_offer_cbutton(
            opponent_text="Do'stga taklif yuborish", back_text="Ortga"
        )
    )
    await call.message.delete()


@router.message(F.user_shared)
async def friend_shared(message: types.Message, state: FSMContext):
    data = await state.get_data()
    book_id = int(data['friend_book_id'])
    book_name = await db.select_book_by_id(
        id_=book_id
    )

    opponent_id = int(message.user_shared.user_id)
    user_id = message.from_user.id
    user_fullname = message.from_user.full_name

    select_opponent = await db.select_user(
        telegram_id=opponent_id
    )

    if select_opponent:
        opponent_status = await db.select_user(telegram_id=opponent_id)
        if opponent_status['game_on']:
            await message.answer(
                text="Taklif qilinayotgan foydalanuvchi hozirda bellashuvda ishtirok etmoqda! Birozdan so'ng qayta "
                     "taklif habarini yuborishingiz mumkin!"
            )
        else:
            markup = to_offer_ibuttons(
                agree_text="Qabul qilish", agree_id=user_id, refusal_text="Rad qilish", book_id=book_id
            )
            await bot.send_message(
                chat_id=opponent_id,
                text=f"Foydalanuvchi {user_fullname} Sizni {book_name['table_name']} kitobi bo'yicha ilmiy bellashuvga "
                     f"taklif qilmoqda!",
                reply_markup=markup
            )
            await message.answer(
                text=f"Bellashuv taklifi foydalanuvchiga yuborildi!", reply_markup=uz_start_buttons
            )
    else:
        await message.answer(
            text=f"Taklif qilinayotgan foydalanuvchi botimiz a'zolari safida mavjud emas!",
            reply_markup=bot_offer_ibuttons(
                full_name=user_fullname, bot_link="@IqtisodchiRobot"
            )
        )
