import asyncio
import logging
from app.users.handlers import router
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from loader import bot, dp



async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s :%(name)s -%(asctime)s'
                        ,level=logging.DEBUG)
    logging.getLogger('matplotlib').setLevel(logging.WARNING) ## отключает matplolib
    asyncio.run(main())