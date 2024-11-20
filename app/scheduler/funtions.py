if __name__ == "__main__":
    from pathlib import Path
    import sys
    from icecream import ic
    # icecream.ic(str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from loader import bot
from app.users.objects_class import ID_TEACHER, ID_MAIN_VOSP, ID_VOSP
import requests
import datetime
from app.database.request import get_data_for_docx
from app.database.table import get_png
from aiogram.types import FSInputFile


async def send_to_teacher(text):
    for ID in ID_TEACHER:
        await bot.send_message(ID, text)


async def send_to_vosp(text):
    for ID in ID_VOSP:
        await bot.send_message(ID, text)


async def send_document():
    day = (datetime.datetime.now() + datetime.timedelta(1)).strftime("%Y-%m-%d")
    list_png = get_png(day)
    res_docx = get_data_for_docx(day)
    file = FSInputFile("docx.docx")
    for ID in ID_MAIN_VOSP:
        for path in list_png:
            if path == list_png[-1]:
                await bot.send_photo(chat_id=ID, photo=FSInputFile(path), reply_markup=kb_check_other_date)
            else:
                await bot.send_photo(chat_id=ID, photo=FSInputFile(path))
        if res_docx != "Error":
            await bot.send_document(chat_id=ID, document=file)
        else:
            await bot.send_message(ID, "Не получилось сформировать документ, недостаточно записей")

if __name__ == "__main__":
    import asyncio
    asyncio.run(send_document())
