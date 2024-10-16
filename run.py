from loader import bot, dp
import asyncio
import logging
from app.users.handlers import admin
from app.users.handlers import teacher
from app.users.handlers import vosp
from app.users.handlers import main_vosp
from app.users.handlers import other
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


async def main():
    dp.include_router(vosp.router)
    dp.include_router(main_vosp.router)
    dp.include_router(teacher.router)
    dp.include_router(admin.router)
    dp.include_router(other.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(message)s :%(name)s -%(asctime)s', level=logging.DEBUG)
    logging.getLogger('matplotlib').setLevel(
        logging.WARNING)  # отключает matplolib
    asyncio.run(main())
