from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.config import BOT_TOKEN

dp = Dispatcher()
# Initialize Bot instance with a default parse mode which will be passed to all API calls
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)


async def clean_table_temporary():
    print("Sending message of Bunyod")


scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
scheduler.add_job(clean_table_temporary, trigger="cron", hour=21, minute=49, start_date=datetime.now())
