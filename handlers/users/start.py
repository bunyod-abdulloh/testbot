from typing import Dict, Any

from aiogram import Router, types, F
from aiogram.enums import ChatMemberStatus
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER, chat_member_updated, LEFT, \
    CommandObject

from aiogram.client.session.middlewares.request_logging import logger
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload

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
