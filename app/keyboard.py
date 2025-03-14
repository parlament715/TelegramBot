from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from aiogram.types import KeyboardButton as KButton
from aiogram.types import InlineKeyboardMarkup as InlKB
from aiogram.types import InlineKeyboardButton as InKButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import datetime
from loader import rq
from app.database import request
from icecream import ic


def create_main_vosp_date_keyboard():
    today = datetime.datetime.now().date()
    weekday = today.weekday()
    if weekday == 6:
        weekday = 5
    builder = ReplyKeyboardBuilder()
    for i in range(5, -1, -1):
        builder.add(KButton(text=weekday_date(
            today+datetime.timedelta(4)-datetime.timedelta(i))))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


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
    return weekday_str + " " + datetime_object.strftime("%d.%m.%Y")


def create_date_keyboard_for_vosp(my_dict: dict) -> InlKB:
    date = datetime.datetime.now().date()
    weekday = date.weekday()
    if not (0 <= weekday <= 5):
        return
    weekdays = {
        0: ["Среда " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        1: ["Четверг " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        2: ["Пятница " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        3: ["Суббота " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y"),
            "Воскресенье " + (date + datetime.timedelta(3)).strftime("%d.%m.%Y")],
        4: ["Понедельник " + (date + datetime.timedelta(3)).strftime("%d.%m.%Y")],
        5: ["Вторник " + (date + datetime.timedelta(3)).strftime("%d.%m.%Y")],
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
        0: ["Среда " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        1: ["Четверг " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        2: ["Пятница " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        3: ["Суббота " + (date + datetime.timedelta(2)).strftime("%d.%m.%Y")],
        4: ["Понедельник " + (date + datetime.timedelta(3)).strftime("%d.%m.%Y")],
        5: ["Вторник " + (date + datetime.timedelta(3)).strftime("%d.%m.%Y")],
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
    breakfast = is_full_time(my_dict, "Завтрак")
    lunch = is_full_time(my_dict, "Обед")
    snack = is_full_time(my_dict, "Полдник")
    kb_time_for_teacher = InlKB(inline_keyboard=[[InKButton(text="✅  Завтрак "+breakfast if breakfast != "❌ " else "❌ Завтрак", callback_data='Завтрак')],
                                                 [InKButton(text="✅  Обед "+lunch if lunch !=
                                                            "❌ " else "❌ Обед", callback_data='Обед')],
                                                 [InKButton(text="✅  Полдник "+snack if snack !=
                                                            "❌ " else "❌ Полдник", callback_data='Полдник')]
                                                 ])
    return kb_time_for_teacher


def gen_keyboard_time_for_vosp(my_dict: dict) -> InlKB:
    date_obj = datetime.datetime.strptime(my_dict["date"], '%d.%m.%Y')
    if date_obj.weekday() == 6:
        breakfast = is_full_time(my_dict, "Завтрак")
        lunch = is_full_time(my_dict, "Обед")
        snack = is_full_time(my_dict, "Полдник")
        dinner = is_full_time(my_dict, "Ужин")
        last_dinner = is_full_time(my_dict, "Паужин")
        keyboard_0x002 = [[InKButton(text="✅  Завтрак "+breakfast if breakfast != "❌ " else "❌ Завтрак", callback_data='Завтрак')],
                          [InKButton(text="✅  Обед "+lunch if lunch !=
                                     "❌ " else "❌ Обед", callback_data='Обед')],
                          [InKButton(text="✅  Полдник "+snack if snack !=
                                     "❌ " else "❌ Полдник", callback_data='Полдник')],
                          [InKButton(text="✅  Ужин "+dinner if dinner !=
                                     "❌ " else "❌ Ужин", callback_data='Ужин')],
                          [InKButton(text="✅  Паужин " + last_dinner if last_dinner !=
                                     "❌ " else "❌ Паужин", callback_data='Паужин')]
                          ]
    else:
        breakfast = is_full_time(my_dict, "Завтрак")
        dinner = is_full_time(my_dict, "Ужин")
        last_dinner = is_full_time(my_dict, "Паужин")
        keyboard_0x002 = [[InKButton(text="✅  Завтрак "+breakfast if breakfast != "❌ " else "❌ Завтрак", callback_data='Завтрак')],
                          [InKButton(text="✅  Ужин " + dinner if dinner !=
                                     "❌ " else "❌ Ужин", callback_data='Ужин')],
                          [InKButton(text="✅  Паужин " + last_dinner if last_dinner !=
                                     "❌ " else "❌ Паужин", callback_data='Паужин')]
                          ]

    return InlKB(inline_keyboard=keyboard_0x002)


def is_full_day(my_dict: dict, date: str) -> str:
    date_obj = datetime.datetime.strptime(date, '%d.%m.%Y')
    my_dict["date"] = date
    if my_dict["user_role"] == "Воспитатель":
        if date_obj.weekday() == 6:
            listik = ['Завтрак', 'Обед', 'Полдник', 'Ужин', "Паужин"]
        else:
            listik = ["Завтрак", "Ужин", "Паужин"]
    elif my_dict["user_role"] == "Классный советник":
        if date_obj.weekday() == 6:
            listik = []
        else:
            listik = ['Завтрак', 'Обед', 'Полдник']
    else:
        raise Exception("user_role must be Классный советник or Воспитатель")
    for time in listik:
        if is_full_time(my_dict, time) == "❌ ":
            return "❌ "
    return "✅ "


def is_full_time(my_dict: dict, time: str) -> str:
    date = my_dict["date"]
    name = my_dict["user_name"]
    my_dict["time"] = time
    with rq:
        res = rq.check_on_exist(my_dict)
        if res:
            return f"({"/".join(map(str, res))})"
    return "❌ "


kb5 = InlKB(
    inline_keyboard=[[InKButton(text='Записать на ЭТУ ЖЕ дату', callback_data="same date")],
                     [InKButton(text="Записать на ДРУГУЮ дату", callback_data="another date")]])

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
            builder.button(text=elem.text + " 🔸",
                           callback_data=elem.callback_data)
        else:
            builder.add(elem)
    builder.adjust(1)
    return builder.as_markup()
