# from datetime import datetime
#
# from aiogram import Bot, Dispatcher
# from aiogram.enums import ParseMode
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
# from data.config import BOT_TOKEN, ADMINS
# from loader import db
#
# dp = Dispatcher()
# # Initialize Bot instance with a default parse mode which will be passed to all API calls
# bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
#
#
# async def clean_tables_scheduler():
#     await db.clean_counter_table()
#     await db.clean_temporary_table()
#     for admin in ADMINS:
#         await bot.send_message(
#             chat_id=admin, text="Counter va temporary tablelar tozalandi!"
#         )
#
#
# scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
# scheduler.add_job(clean_tables_scheduler, trigger="cron", hour=2, minute=20, start_date=datetime.now())
