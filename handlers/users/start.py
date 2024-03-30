from aiogram import Router, types, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, chat_member_updated, LEFT
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger

from keyboards.inline.buttons import check_user_ibuttons
from keyboards.reply.main_reply import main_button
from loader import db, bot
from data.config import ADMINS, GROUP_ID
from utils.extra_datas import make_title

router = Router()
uz_start_buttons = main_button(
    competition="Bellashuv", rating="Reyting", manual="Qo'llanma"
)

uz_check_buttons = check_user_ibuttons(
    status="Obunani tekshirish"
)


@router.message(CommandStart())
async def do_start(message: types.Message):
    # telegram_id = message.from_user.id
    # full_name = message.from_user.full_name
    # username = message.from_user.username
    # user = None
    # try:
    #     user = await db.add_user(telegram_id=telegram_id, full_name=full_name, username=username)
    # except Exception as error:
    #     logger.info(error)
    # if user:
    #     count = await db.count_users()
    #     msg = (f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    # else:
    #     msg = f"[{make_title(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
    # for admin in ADMINS:
    #     try:
    #         await bot.send_message(
    #             chat_id=admin,
    #             text=msg,
    #             parse_mode=ParseMode.MARKDOWN_V2
    #         )
    #     except Exception as error:
    #         logger.info(f"Data did not send to admin: {admin}. Error: {error}")
    await message.answer(text=f"Assalomu alaykum! Botdan foydalanish uchun guruhimizga a'zo bo'ling!",
                         reply_markup=uz_check_buttons)


@router.callback_query(F.data == "status")
async def check_user_status(call: types.CallbackQuery):
    user_id = call.from_user.id

    user_channel_status = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
    print(user_channel_status)
    await call.message.delete()
    if user_channel_status.status != ChatMemberStatus.LEFT:
        await call.message.answer(
            text="Assalomu alaykum!",
            reply_markup=uz_start_buttons
        )
    else:
        await call.message.answer(
            text="Siz guruhga a'zo bo'lmagansiz! Botdan foydalanish uchun iltimos guruhga a'zo bo'ling! Guruh "
                 "havolasini admindan olishingiz mumkin!",
            reply_markup=types.ReplyKeyboardRemove()
        )


@router.chat_member(F.chat.func(lambda chat: chat.id == GROUP_ID))
async def join_member(event: types.ChatMemberUpdated):
    user_id = event.from_user.id
    print(event.chat.type)
    try:
        await bot.send_message(
            chat_id=user_id,
            text="Siz bot guruhiga qo'shildingiz! Botdan foydalanishingiz mumkin!",
            reply_markup=uz_start_buttons
        )
    except Exception:
        pass


@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def leave_member(event: types.ChatMemberUpdated):
    user_id = event.from_user.id
    try:
        await bot.send_message(
            chat_id=user_id,
            text="Siz bot guruhidan chiqdingiz! Botdan foydalanish imkoniyati cheklandi!",
            reply_markup=types.ReplyKeyboardRemove()
        )
    except Exception:
        pass
