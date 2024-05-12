# import pytz
#
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
#
# from data.config import ADMINS
# from loader import bot, db
#
# tz = pytz.timezone('Asia/Tashkent')
#
# job_defaults = {
#     "misfire_grace_time": 3600
# }
#
# jobstores = {
#     "default": SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
#
# scheduler = AsyncIOScheduler(timezone=tz, jobstores=jobstores, job_defaults=job_defaults)
#
#
# async def question_scheduler():
#     print("salom")
#
# scheduler.add_job(question_scheduler(), trigger='interval', hour=1)
