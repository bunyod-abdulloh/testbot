from typing import Union

from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message

from data.config import GROUP_ID
from loader import bot


class ChatTypeFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        member = await bot.get_chat_member(message.chat.id, "5801141107")
        print(member)
        return member.status == "administator"
