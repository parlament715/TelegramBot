from loader import bot, dp, scheduler
from app.scheduler.notifications import add_job_scheduler
import asyncio
import logging
from app.middelwares import CheckerOnCallbackData, CheckerSubscriptionsOnChannel
from app.users.handlers import teacher
from app.users.handlers import vosp
from app.users.handlers import main_vosp
from app.users.handlers import other
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


async def main():
    add_job_scheduler(scheduler)
    scheduler.start()
    dp.message.outer_middleware.register(CheckerSubscriptionsOnChannel())
    dp.callback_query.outer_middleware.register(CheckerOnCallbackData())
    dp.include_router(vosp.router)
    dp.include_router(main_vosp.router)
    dp.include_router(teacher.router)
    dp.include_router(other.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        format='%(message)s :%(name)s -%(asctime)s', level=logging.DEBUG)
    logging.getLogger('matplotlib').setLevel(
        logging.WARNING)  # отключает matplolib
    asyncio.run(main())
