from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database.request import Request

scheduler = AsyncIOScheduler()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
rq = Request("request.db")
