from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton as KButton
from aiogram.types import InlineKeyboardMarkup as InlKB
from aiogram.types import InlineKeyboardButton as InKButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import datetime
from app.database import request
from icecream import ic


def create_main_vosp_date_keyboard():
    today = datetime.datetime.now().date()
    kb_date_all = ReplyKeyboardMarkup(
        resize_keyboard=True, keyboard=[[KButton(text=f'Сегодня {str(today)}')],
                                        [KButton(
                                            text=f'Завтра {str(today + datetime.timedelta(days=1))}')],
                                        [KButton(
                                            text=f'Послезавтра {str(today + datetime.timedelta(days=2))}')]])

    return kb_date_all


def weekday_date(datetime_object: datetime) -> str:
    a = datetime_object.weekday()
    weekday_str = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }.get(datetime_object.weekday(), "Unknown")
    return weekday_str + datetime_object.strftime(" %d.%m.%Y")


def create_date_keyboard_for_vosp() -> InlKB:
    date = datetime.datetime.now().date()
    weekday = date.weekday()
    if not (1 <= weekday <= 5):
        return
    weekdays = {
        1: ["Четверг " + str(date + datetime.timedelta(2))],
        2: ["Пятница " + str(date + datetime.timedelta(2))],
        3: ["Суббота " + str(date + datetime.timedelta(2)),
            "Воскресенье " + str(date + datetime.timedelta(3)),
            "Понедельник " + str(date + datetime.timedelta(4))],
        4: ["Вторник " + str(date + datetime.timedelta(2))],
        5: ["Среда " + str(date + datetime.timedelta(2))],
    }
    builder = InlineKeyboardBuilder()
    for elem in weekdays[weekday]:
        builder.button(text=elem, callback_data=elem.split()[-1])
    builder.adjust(1)
    return builder.as_markup()


def create_date_keyboard_for_teacher() -> InlKB:
    date = datetime.datetime.now().date()
    weekday = date.weekday()
    if not (1 <= weekday <= 5):
        return
    weekdays = {
        1: ["Четверг " + str(date + datetime.timedelta(2))],
        2: ["Пятница " + str(date + datetime.timedelta(2))],
        3: ["Суббота " + str(date + datetime.timedelta(2)),
            "Понедельник " + str(date + datetime.timedelta(4))],
        4: ["Вторник " + str(date + datetime.timedelta(2))],
        5: ["Среда " + str(date + datetime.timedelta(2))],
    }
    builder = InlineKeyboardBuilder()
    for elem in weekdays[weekday]:
        builder.button(text=elem, callback_data=elem.split()[-1])
    builder.adjust(1)
    return builder.as_markup()


kb_check_other_date = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                                          [KButton(text='Посмотреть другую дату')]])


def gen_keyboard_time_for_teacher(my_dict):
    kb_time_for_teacher = InlKB(inline_keyboard=[[InKButton(text=is_full_time(my_dict, "Завтрак") + 'Завтрак',                        callback_data="Завтрак")],
                                                 [InKButton(
                                                     text=is_full_time(my_dict, "Обед") + 'Обед', callback_data="Обед")],
                                                 [InKButton(text=is_full_time(my_dict, "Полдник") + 'Полдник',
                                                            callback_data="Полдник")]
                                                 ])
    return kb_time_for_teacher


def gen_keyboard_time_for_vosp(my_dict: dict) -> InlKB:
    date_obj = datetime.datetime.strptime(my_dict["date"], '%Y-%m-%d')
    if date_obj.weekday() == 6:
        keyboard_0x002 = [[InKButton(text=is_full_time(my_dict, "Завтрак") + 'Завтрак', callback_data='Завтрак')],
                          [InKButton(text=is_full_time(my_dict, "Обед") +
                                     'Обед', callback_data='Обед')],
                          [InKButton(text=is_full_time(my_dict, "Полдник") +
                                     'Полдник', callback_data='Полдник')],
                          [InKButton(text=is_full_time(my_dict, "Ужин") +
                                     'Ужин', callback_data='Ужин')],
                          ]
    else:
        keyboard_0x002 = [[InKButton(text=is_full_time(my_dict, "Завтрак") + 'Завтрак', callback_data='Завтрак')],
                          [InKButton(text=is_full_time(my_dict, "Ужин") +
                                     'Ужин', callback_data='Ужин')],
                          ]

    return InlKB(inline_keyboard=keyboard_0x002)


def is_full_time(my_dict: dict, time: str) -> str:
    date = my_dict["date"]
    name = my_dict["user_name"]
    request.to_create(date)
    my_dict["time"] = time
    if request.check_on_exist(my_dict):
        return "♻️ "
    return ""


kb5 = ReplyKeyboardMarkup(resize_keyboard=True,
                          keyboard=[[KButton(text='Записать на ЭТУ ЖЕ дату')],
                                    [KButton(text="Записать на ДРУГУЮ дату")]])

remove = ReplyKeyboardRemove()


yes_no_keyboard = InlKB(inline_keyboard=[
    [InKButton(text="Да", callback_data="Yes"),
     InKButton(text="Нет", callback_data="No")]
])
