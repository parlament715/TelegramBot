import sqlite3
from icecream import ic
from typing import Union, Optional
import logging
from docxtpl import DocxTemplate
# from app.database.table import dataframe_to_png_with_subcolumns


def to_create(date):
    pass


def to_write(my_dict: dict):
    pass


def from_dict_to_name_column(dict: dict) -> list:
    pass


def to_read_db(table_name: str, columns: str, where: Optional[str] = None) -> list:
    pass


def check_on_exist(my_dict: dict) -> Union[list, None]:
    pass
# def to_create(date):
#     global cursor, conn
#     conn = sqlite3.connect('request.db')

#     cursor = conn.cursor()

#     cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{date}"
#                     (who TEXT,
#                     breakfast_dorm INTEGER,
#                     breakfast_city INTEGER,
#                     lunch_dorm INTEGER,
#                     lunch_city INTEGER,
#                     snack_dorm INTEGER,
#                     snack_city INTEGER,
#                     dinner_dorm INTEGER,
#                     role TEXT)
#                     ''')


# def to_write(my_dict: dict):
#     name = my_dict["user_name"]
#     role = my_dict["user_role"]
#     my_date = my_dict['date']
#     num = my_dict["num"].split()
#     to_create(str(my_date))
#     for (index, column_name) in enumerate(from_dict_to_name_column(my_dict)):
#         res = cursor.execute(
#             f''' SELECT {column_name} FROM "{str(my_date)}" WHERE who = "{name}" ''').fetchone()
#         if res == None:
#             cursor.execute(f'''
#                         INSERT INTO "{str(my_date)}"
#                         (who, role, {column_name}) VALUES
#                         ("{name}","{role}",{num[index]})
#                             ''')  # если записи ещё не было то добавляем
#         else:
#             cursor.execute(
#                 f''' UPDATE "{str(my_date)}" SET {column_name} = "{num[index]}" WHERE who = "{name}" ''')  # если была то уже обновляем то что было
#     conn.commit()
#     conn.close()


# def from_dict_to_name_column(dict: dict) -> list:
#     listik = []  # приводим в порядок данные перед записью
#     time = dict["time"]
#     role = dict["user_role"]
#     column_names = {
#         "Завтрак Классный советник": "breakfast_city",
#         "Завтрак Воспитатель": "breakfast_dorm",
#         "Обед Классный советник": "lunch_city",
#         "Обед Классный советник dorm": "lunch_dorm",
#         "Обед Воспитатель": "lunch_dorm",
#         "Полдник Классный советник": "snack_city",
#         "Полдник Классный советник dorm": "snack_dorm",
#         "Полдник Воспитатель": "snack_dorm",
#         "Ужин Воспитатель": "dinner_dorm",
#     }  # меняем здесь
#     _column_name = time + " " + role
#     if role == 'Классный советник' and time == 'Завтрак':
#         column_name = column_names[_column_name]
#         listik.append(column_name)
#     elif role == "Классный советник" and (time == "Обед" or time == "Полдник"):
#         column_name = column_names[_column_name]
#         listik.append(column_name)
#         # to_to_write(my_date,column_name,name,class_num,num.split()[0])
#         _column_name += " dorm"
#         column_name = column_names[_column_name]
#         listik.append(column_name)
#         # to_to_write(my_date,column_name,name,class_num,num.split()[1])
#     elif role == "Воспитатель":
#         listik.append(column_names[_column_name])
#     return listik


# def to_read_db(table_name: str, columns: str, where: Optional[str] = None) -> list:
#     to_create(table_name)
#     if where != None:
#         cursor.execute(
#             f'''SELECT {columns} FROM "{table_name}" WHERE {where}''')
#     else:
#         cursor.execute(f'''SELECT {columns} FROM "{table_name}"''')
#     a = cursor.fetchall()
#     b = []
#     for i in a:
#         b.append(str(i[0]))  # преобразовываем в массив из кортежа для красоты
#     return b


# def check_on_exist(my_dict: dict) -> Union[list, None]:
#     name = my_dict["user_name"]
#     my_date = my_dict["date"]
#     time = my_dict["time"]
#     res = []
#     to_create(my_date)
#     ic(from_dict_to_name_column(my_dict), my_dict)
#     for time in from_dict_to_name_column(my_dict):
#         a = cursor.execute(
#             f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}"''').fetchone()
#         if a != None and a != (None,):
#             res.append(a[0])

#     if res != []:
#         return res
#     return None


class Request:
    table_selector = {"Воспитатель": "vosp", "Классный советник": "teacher"}

    def __init__(self, path: str):
        self.path = path
        conn = sqlite3.connect(path)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "teacher"(
        name STRING,
        breakfast INTEGER,
        lunch_dorm INTEGER,
        lunch_city INTEGER,
        snack_dorm INTEGER,
        snack_city INTEGER,
        date TEXT
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "vosp"(
        name STRING,
        breakfast INTEGER,
        dinner INTEGER,
        date TEXT
        )
        ''')

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    def from_dict_to_name_column(self, dict: dict) -> list:
        # приводим в порядок данные перед записью
        time = dict["time"]
        role = dict["user_role"]
        column_names = {
            "Завтрак Классный советник": "breakfast",
            "Завтрак Воспитатель": "breakfast",
            "Обед Классный советник": "lunch_city",
            "Обед Классный советник dorm": "lunch_dorm",
            "Обед Воспитатель": "lunch_dorm",
            "Полдник Классный советник": "snack_city",
            "Полдник Классный советник dorm": "snack_dorm",
            "Полдник Воспитатель": "snack_dorm",
            "Ужин Воспитатель": "dinner",
        }  # меняем здесь
        _column_name = time + " " + role
        if time == "Завтрак":
            return ("breakfast",)
        elif role == "Классный советник":
            column_name1 = column_names[_column_name]
            _column_name += " dorm"
            column_name2 = column_names[_column_name]
            return (column_name1, column_name2)
        elif role == "Воспитатель":
            return (column_names[_column_name],)

    def to_write(self, my_dict: dict):
        name = my_dict["user_name"]
        role = my_dict["user_role"]
        table_name = Request.table_selector[role]
        my_date = my_dict['date']
        num = my_dict["num"].split()
        for (index, column_name) in enumerate(self.from_dict_to_name_column(my_dict)):
            res = self.cursor.execute(
                f''' SELECT ? FROM "{table_name}" WHERE name = ? AND date = ? ''', (column_name, name, my_date)).fetchone()
            if res == None:
                self.cursor.execute(f'''
                            INSERT INTO "{table_name}"
                            (name, date, "{column_name}") VALUES
                            (?,?,?)
                                ''', (name, my_date, num[index]))  # если записи ещё не было то добавляем
            else:
                self.cursor.execute(
                    f''' UPDATE "{table_name}" SET "{column_name}" = ? WHERE name = ? AND date = ? ''', (num[index], name, my_date))  # если была то уже обновляем то что было

    def check_on_exist(self, my_dict: dict) -> Union[list, None]:
        name = my_dict["user_name"]
        my_date = my_dict["date"]
        time = my_dict["time"]
        table_name = Request.table_selector[my_dict["user_role"]]
        res = []
        for time in self.from_dict_to_name_column(my_dict):
            a = self.cursor.execute(
                f''' SELECT "{time}" FROM {table_name} WHERE name = ? AND date = ?''', (name, my_date)).fetchone()
            if a != None and a != (None,):
                res.append(a[0])

        if res != []:
            return res
        return None

    def to_read_db(self, table_name, date: str, columns: str, where: Optional[str] = "") -> list:
        if where != "":
            where = "AND " + where
        self.cursor.execute(
            f'''SELECT {columns} FROM "{table_name}" WHERE date = ? {where}''', (date,))
        a = self.cursor.fetchall()
        b = []
        for i in a:
            # преобразовываем в массив из кортежа для красоты
            b.append(str(i[0]))
        return b

    def get_data_for_docx(self, date: str) -> dict:
        breakfast_city = sum([int(x) for x in self.to_read_db(
            "teacher", date, "breakfast") if x != "None"])
        lunch_dorm = sum([int(x) for x in self.to_read_db(
            "teacher", date, "lunch_dorm") if x != "None"])
        lunch_city = sum([int(x) for x in self.to_read_db(
            "teacher", date, "lunch_city") if x != "None"])
        snack_dorm = sum([int(x) for x in self.to_read_db(
            "teacher", date, "snack_dorm") if x != "None"])
        snack_city = sum([int(x) for x in self.to_read_db(
            "teacher", date, "snack_city") if x != "None"])

        breakfast_dorm = sum([int(x) for x in self.to_read_db(
            "vosp", date, "breakfast") if x != "None"])
        dinner_dorm = sum([int(x) for x in self.to_read_db(
            "vosp", date, "dinner") if x != "None"])
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
            "a": str(breakfast_city),
            "b": str(breakfast_dorm),
            "c": str(lunch_city),
            "d": str(lunch_dorm),
            "e": str(snack_city),
            "f": str(snack_dorm),
            "g": "0",
            "h": str(dinner_dorm),
        }
        fill_template("example.docx", "docx.docx", content)


def fill_template(template_path: str, output_path: str, context: dict):
    # Загрузка шаблона
    doc = DocxTemplate(template_path)
    # Замена плейсхолдеров
    doc.render(context)
    # Сохранение документа
    doc.save(output_path)
