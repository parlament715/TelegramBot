if __name__ == "__main__":
    from pathlib import Path
    import sys
    from icecream import ic
    # icecream.ic(str(Path(__file__).resolve().parents[2]))
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from loader import bot, rq
from app.users.objects_class import ID_TEACHER, ID_MAIN_VOSP, ID_VOSP
import datetime
from app.database.table import get_png
from aiogram.types import FSInputFile
from app.keyboard import is_full_day
from app.users.objects_class import find_user_name_by_id
from config import time_to
from icecream import ic


async def send_to_teacher(text):
    for ID in ID_TEACHER:
        await bot.send_message(ID, text)


async def send_to_vosp(text):
    for ID in ID_VOSP:
        await bot.send_message(ID, text)


async def send_document():
    day = (datetime.datetime.now() + datetime.timedelta(1)).strftime("%d.%m.%Y")
    list_png = get_png(day)
    with rq:
        res_docx = rq.get_data_for_docx(day)
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


def check_all_users(date: str):
    passed_users = []
    date = datetime.datetime.strptime(date, "%d.%M.%Y")
    weekday = date.weekday()
    listik = [(weekday, date)]
    for id in ID_TEACHER:
        name = find_user_name_by_id(id)
        my_dict = {"user_name": name,
                   "user_role": "Классный советник",
                   }
        if is_full_days(my_dict, listik) != True:
            passed_users.append(name)
    for id in ID_VOSP:
        name = find_user_name_by_id(id)
        my_dict = {"user_name": name,
                   "user_role": "Воспитатель",
                   }
        if is_full_days(my_dict, listik) != True:
            passed_users.append(name)
    return passed_users


async def send_notifications():
    await send_notifications_vosp()
    await send_notifications_teacher()


async def send_notifications_teacher():
    date = datetime.datetime.now().date()
    weekday_now = date.weekday()
    if not (0 <= weekday_now <= 5):
        return
    weekdays = {
        0: [("Среда", date + datetime.timedelta(2))],
        1: [("Четверг",  date + datetime.timedelta(2))],
        2: [("Пятница",  date + datetime.timedelta(2))],
        3: [("Суббота",  date + datetime.timedelta(2))],
        4: [("Понедельник",  date + datetime.timedelta(3))],
        5: [("Вторник",  date + datetime.timedelta(3))],
    }
    listik = weekdays[weekday_now]
    for id in ID_TEACHER:
        my_dict = {"user_name": find_user_name_by_id(id),
                   "user_role": "Классный советник",
                   }
        a = is_full_days(my_dict, listik)
        if a != True:  # если не полный день
            await bot.send_message(id, f"У вас не заполнены дни :\n{" ".join(a)}\nПожалуйста заполните до {time_to.hour:02}:{time_to.minute:02}")


async def send_notifications_vosp():
    date = datetime.datetime.now().date()
    weekday_now = date.weekday()
    if not (0 <= weekday_now <= 5):
        return
    weekdays = {
        0: [("Среда", date + datetime.timedelta(2))],
        1: [("Четверг",  date + datetime.timedelta(2))],
        2: [("Пятница",  date + datetime.timedelta(2))],
        3: [("Суббота",  date + datetime.timedelta(2)),
            ("Воскресенье", date + datetime.timedelta(3))],
        4: [("Понедельник",  date + datetime.timedelta(3))],
        5: [("Вторник",  date + datetime.timedelta(3))],
    }
    listik = weekdays[weekday_now]
    for id in ID_VOSP:
        my_dict = {"user_name": find_user_name_by_id(id),
                   "user_role": "Воспитатель",
                   }
        a = is_full_days(my_dict, listik)
        if a != True:  # если не полный день
            await bot.send_message(id, f"У вас не заполнены дни :\n{" ".join(a)}\nПожалуйста заполните до {time_to.hour:02}:{time_to.minute:02}")


def is_full_days(my_dict: dict, listik: list):
    c = []
    # print(listik)
    for weekday, date in listik:
        if is_full_day(my_dict, date.strftime("%d.%M.%Y")) == "❌ ":
            c.append(weekday)
    if not c:
        return True
    else:
        return c


if __name__ == "__main__":
    import asyncio
    asyncio.run(send_notifications_teacher())
