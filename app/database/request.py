import sqlite3
from icecream import ic
from typing import Union, Optional
import logging
from docxtpl import DocxTemplate
# from app.database.table import dataframe_to_png_with_subcolumns


def to_create(date):
    global cursor, conn
    conn = sqlite3.connect('request.db')

    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{date}"
                    (who TEXT,
                    breakfast_dorm INTEGER,
                    breakfast_city INTEGER,
                    lunch_dorm INTEGER,
                    lunch_city INTEGER,
                    snack_dorm INTEGER,
                    snack_city INTEGER,
                    dinner_dorm INTEGER,
                    role TEXT)
                    ''')


def to_write(my_dict: dict):
    name = my_dict["user_name"]
    role = my_dict["user_role"]
    my_date = my_dict['date']
    ic(name, role, my_date, my_dict.keys(), my_dict)
    num_list = my_dict["num"].split()
    to_create(str(my_date))
    for (index, column_name) in enumerate(from_dict_to_name_column(my_dict)):
        num = num_list[index]
        res = cursor.execute(
            f''' SELECT {column_name} FROM "{str(my_date)}" WHERE who = "{name}" ''').fetchone()
        if res == None:
            cursor.execute(f'''
                        INSERT INTO "{str(my_date)}"
                        (who, role, {column_name}) VALUES
                        ("{name}","{role}",{num})
                            ''')  # если записи ещё не было то добавляем
        else:
            cursor.execute(
                f''' UPDATE "{str(my_date)}" SET {column_name} = "{num}" WHERE who = "{name}" ''')  # если была то уже обновляем то что было
    conn.commit()
    conn.close()


def from_dict_to_name_column(dict: dict) -> list:
    listik = []  # приводим в порядок данные перед записью
    time = dict["time"]
    role = dict["user_role"]
    ic(dict)
    column_names = {
        "Завтрак Классный советник": "breakfast_city",
        "Завтрак Воспитатель": "breakfast_dorm",
        "Обед Классный советник": "lunch_city",
        "Обед Воспитатель": "lunch_dorm",
        "Полдник Классный советник": "snack_city",
        "Полдник Воспитатель": "snack_dorm",
        "Ужин Воспитатель": "dinner_dorm",
    }
    ic(time, role)
    _column_name = time + " " + role
    if role == 'Классный советник' and time == 'Завтрак':
        column_name = column_names[_column_name]
        listik.append(column_name)
    elif role == "Классный советник" and (time == "Обед" or time == "Полдник"):
        column_name = column_names[_column_name]
        listik.append(column_name)
        # to_to_write(my_date,column_name,name,class_num,num.split()[0])
        _column_name += " dorm"
        column_name = column_names[_column_name]
        listik.append(column_name)
        # to_to_write(my_date,column_name,name,class_num,num.split()[1])
    elif role == "Воспитатель":
        listik.append(column_names[_column_name])
        listik.append(column_names[_column_name])
    return listik


def to_read_db(table_name: str, columns: str, where: Optional[str] = None) -> list:
    to_create(table_name)
    if where != None:
        cursor.execute(
            f'''SELECT {columns} FROM "{table_name}" WHERE {where}''')
    else:
        cursor.execute(f'''SELECT {columns} FROM "{table_name}"''')
    a = cursor.fetchall()
    b = []
    for i in a:
        b.append(str(i[0]))  # преобразовываем в массив из кортежа для красоты
    return b


def check_on_exist(my_dict: dict) -> Union[list, None]:
    name = my_dict["user_name"]
    my_date = my_dict["date"]
    time = my_dict["time"]
    role = my_dict["user_role"]
    res = []

    to_create(my_date)
    ic(from_dict_to_name_column(my_dict), my_dict)
    for time in from_dict_to_name_column(my_dict):
        a = cursor.execute(
            f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}"''').fetchone()
        if a != None and a != (None,):
            res.append(a[0])

    if res != []:
        return res
    return None


def fill_template(template_path: str, output_path: str, context: dict):
    # Загрузка шаблона
    doc = DocxTemplate(template_path)
    # Замена плейсхолдеров
    doc.render(context)
    # Сохранение документа
    doc.save(output_path)


def get_data_for_docx(date: str) -> dict:
    to_create(date)
    try:
        breakfast_city_11 = sum([int(x) for x in to_read_db(
            date, "breakfast_city_11", where="class_num=11")])
        lunch_dorm_11 = sum([int(x) for x in to_read_db(
            date, "lunch_dorm_11", where="class_num=11")])
        lunch_city_11 = sum([int(x) for x in to_read_db(
            date, "lunch_city_11", where="class_num=11")])
        snack_dorm_11 = sum([int(x) for x in to_read_db(
            date, "snack_dorm_11", where="class_num=11")])
        snack_city_11 = sum([int(x) for x in to_read_db(
            date, "snack_city_11", where="class_num=11")])

        breakfast_city_10 = sum([int(x) for x in to_read_db(
            date, "breakfast_city_10", where="class_num=10")])
        lunch_dorm_10 = sum([int(x) for x in to_read_db(
            date, "lunch_dorm_10", where="class_num=10")])
        lunch_city_10 = sum([int(x) for x in to_read_db(
            date, "lunch_city_10", where="class_num=10")])
        snack_dorm_10 = sum([int(x) for x in to_read_db(
            date, "snack_dorm_10", where="class_num=10")])
        snack_city_10 = sum([int(x) for x in to_read_db(
            date, "snack_city_10", where="class_num=10")])

        breakfast_dorm_11 = sum([int(x) for x in to_read_db(
            date, "breakfast_dorm_11", where='role = "Воспитатель"')])
        breakfast_dorm_10 = sum([int(x) for x in to_read_db(
            date, "breakfast_dorm_10", where='role = "Воспитатель"')])
        dinner_dorm_10 = sum([int(x) for x in to_read_db(
            date, "dinner_dorm_10", where='role = "Воспитатель"')])
        dinner_dorm_11 = sum([int(x) for x in to_read_db(
            date, "dinner_dorm_11", where='role = "Воспитатель"')])
    except ValueError:
        return "Error"

    # разбиваем дату
    year, month, day = map(int, date.split('-'))
    months_genitive = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    month = months_genitive[month - 1]
    content = {
        "data_num": str(day),
        "data_month": month,
        "data_year": str(year),
        "a": str(breakfast_city_10 + breakfast_city_11),
        "b": str(breakfast_dorm_10 + breakfast_dorm_11),
        "c": str(lunch_city_10 + lunch_city_11),
        "d": str(lunch_dorm_10 + lunch_dorm_11),
        "e": str(snack_city_10 + snack_city_11),
        "f": str(snack_dorm_10 + snack_dorm_11),
        "g": "0",
        "h": str(dinner_dorm_10 + dinner_dorm_11),
        "i": str(breakfast_city_10),
        "j": str(breakfast_dorm_10),
        "k": str(breakfast_city_11),
        "l": str(breakfast_dorm_11),
        "m": str(lunch_city_10),
        "n": str(lunch_dorm_10),
        "o": str(lunch_city_11),
        "p": str(lunch_dorm_11),
        "q": str(snack_city_10),
        "r": str(snack_dorm_10),
        "s": str(snack_city_11),
        "t": str(snack_dorm_11),
        "u": "0",
        "v": str(dinner_dorm_10),
        "w": "0",
        "x": str(dinner_dorm_11),
    }
    fill_template("example.docx", "docx.docx", content)
