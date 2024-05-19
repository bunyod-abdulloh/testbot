from typing import Dict, Any

from aiogram import Router, types, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, chat_member_updated, LEFT

from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from filters import ChatTypeFilter
from keyboards.inline.buttons import check_user_ibuttons
from keyboards.reply.main_reply import main_button
from loader import db, bot
from data.config import ADMINS, GROUP_ID
from states.test import UserSOS

router = Router()
router.message.filter(ChatTypeFilter(["private"]))

uz_start_buttons = main_button(
    competition="Bellashuv", rating="Reyting", manual="Qo'llanma", questions="Savol va takliflar"
)

uz_check_buttons = check_user_ibuttons(
    status="Obunani tekshirish"
)


@router.message(CommandStart())
async def main_start(message: types.Message, state: FSMContext):
    await state.clear()
    telegram_id = message.from_user.id
    full_name = message.from_user.full_name
    check_from_db = await db.select_user(
        telegram_id=telegram_id
    )
    # Users jadvalidan game_on ustunini FALSE holatiga tushirish
    await db.edit_status_users(
        game_on=False, telegram_id=telegram_id
    )
    try:
        if check_from_db:
            pass
        else:
            await db.add_user(telegram_id=telegram_id, full_name=full_name)
    except Exception as error:
        logger.info(error)
    await message.answer(
        text="Assalomu alaykum!",
        reply_markup=uz_start_buttons
    )
    # await message.answer(text="Assalomu alaykum! Botdan foydalanish uchun guruhimizga a'zo bo'ling!",
    #                      reply_markup=uz_check_buttons)
#
#
# @router.callback_query(F.data == "status")
# async def check_user_status(call: types.CallbackQuery):
#     user_id = call.from_user.id
#
#     user_status = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
#
#     await call.message.delete()
#     if user_status.status != ChatMemberStatus.LEFT:
#         await call.message.answer(
#             text="Assalomu alaykum!",
#             reply_markup=uz_start_buttons
#         )
#     else:
#         await call.message.answer(
#             text="Siz guruhga a'zo bo'lmagansiz! Botdan foydalanish uchun iltimos guruhga a'zo bo'ling! Guruh "
#                  "havolasini admindan olishingiz mumkin!",
#             reply_markup=types.ReplyKeyboardRemove()
#         )
#
#
# @router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def join_member(event: types.ChatMemberUpdated):
#     user_id = event.from_user.id
#
#     CHAT_ID = str(event.chat.id)
#
#     if CHAT_ID == GROUP_ID:
#         try:
#             await bot.send_message(
#                 chat_id=user_id,
#                 text="Siz bot guruhiga qo'shildingiz! Botdan foydalanishingiz mumkin!",
#                 reply_markup=uz_start_buttons
#             )
#         except Exception:
#             pass
#
#
# @router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
# async def leave_member(event: types.ChatMemberUpdated):
#     user_id = event.from_user.id
#
#     CHAT_ID = str(event.chat.id)
#
#     if CHAT_ID == GROUP_ID:
#         try:
#             await bot.send_message(
#                 chat_id=user_id,
#                 text="Siz bot guruhidan chiqdingiz! Botdan foydalanish imkoniyati cheklandi!",
#                 reply_markup=types.ReplyKeyboardRemove()
#             )
#         except Exception:
#             pass
