from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
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


def create_date_keyboard_for_vosp(my_dict: dict) -> InlKB:
    date = datetime.datetime.now().date()
    weekday = date.weekday()
    if not (0 <= weekday <= 5):
        return
    weekdays = {
        0: ["Среда " + str(date + datetime.timedelta(2))],
        1: ["Четверг " + str(date + datetime.timedelta(2))],
        2: ["Пятница " + str(date + datetime.timedelta(2))],
        3: ["Суббота " + str(date + datetime.timedelta(2)),
            "Воскресенье " + str(date + datetime.timedelta(3))],
        4: ["Понедельник " + str(date + datetime.timedelta(3))],
        5: ["Вторник " + str(date + datetime.timedelta(3))],
    }
    builder = InlineKeyboardBuilder()
    for elem in weekdays[weekday]:
        builder.button(text=is_full_day(my_dict, elem.split()[-1]) + elem,
                       callback_data=elem.split()[-1])
    builder.adjust(1)
    return builder.as_markup()


def create_date_keyboard_for_teacher(my_dict: dict) -> InlKB:
    date = datetime.datetime.now().date()
    weekday = date.weekday()
    if not (0 <= weekday <= 5):
        return
    weekdays = {
        0: ["Среда " + str(date + datetime.timedelta(2))],
        1: ["Четверг " + str(date + datetime.timedelta(2))],
        2: ["Пятница " + str(date + datetime.timedelta(2))],
        3: ["Суббота " + str(date + datetime.timedelta(2))],
        4: ["Понедельник " + str(date + datetime.timedelta(3))],
        5: ["Вторник " + str(date + datetime.timedelta(3))],
    }
    builder = InlineKeyboardBuilder()
    for elem in weekdays[weekday]:
        builder.button(text=is_full_day(my_dict, elem.split()
                       [-1]) + elem, callback_data=elem.split()[-1])
    builder.adjust(1)
    return builder.as_markup()


kb_check_other_date = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
                                          [KButton(text='Посмотреть другую дату')]])


def gen_keyboard_time_for_teacher(my_dict: dict) -> InlKB:
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


def is_full_day(my_dict: dict, date: str) -> str:
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    my_dict["date"] = date
    if my_dict["user_role"] == "Воспитатель":
        if date_obj.weekday() == 6:
            listik = ['Завтрак', 'Обед', 'Полдник', 'Ужин']
        else:
            listik = ["Завтрак", "Ужин"]
    elif my_dict["user_role"] == "Классный советник":
        listik = ["Завтрак", "Обед", "Полдник"]
    else:
        raise Exception("user_role must be Классный советник or Воспитатель")
    request.to_create(my_dict["date"])
    for time in listik:
        if is_full_time(my_dict, time) == "":
            return ""
    return "♻️ "


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


def flatten(nested_list):
    """Уплощает вложенный список."""
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            # Рекурсивный вызов для вложенных списков
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


def take_changed_keyboard(keyboard: InlKB, call_data: CallbackQuery) -> InlKB:
    listik = []
    keyboard = flatten(keyboard.inline_keyboard)
    builder = InlineKeyboardBuilder()
    for elem in keyboard:
        if elem.callback_data == call_data:
            builder.button(text=elem.text + " ✅",
                           callback_data=elem.callback_data)
        else:
            builder.add(elem)
    builder.adjust(1)
    return builder.as_markup()
