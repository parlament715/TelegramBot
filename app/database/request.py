import sqlite3
from icecream import ic
from typing import Union, Optional
import logging
from docxtpl import DocxTemplate
import datetime


class Request:
    table_selector = {"Воспитатель в": "vosp_sunday",
                      "Воспитатель": "vosp", "Классный советник": "teacher"}

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
        conn.execute('''
        CREATE TABLE IF NOT EXISTS "vosp_sunday"(
        name STRING,
        breakfast INTEGER,
        lunch INTEGER,
        snack INTEGER,
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
            "Обед Воспитатель": "lunch",
            "Полдник Классный советник": "snack_city",
            "Полдник Классный советник dorm": "snack_dorm",
            "Полдник Воспитатель": "snack",
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
        my_date = my_dict['date']
        p = ""
        if datetime.datetime.strptime(my_date, "%d.%m.%Y").weekday() == 6:
            p = " в"
        table_name = Request.table_selector[my_dict["user_role"]+p]
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
        p = ""
        if datetime.datetime.strptime(my_date, "%d.%m.%Y").weekday() == 6 and my_dict["user_role"] == "Воспитатель":
            p = " в"
        table_name = Request.table_selector[my_dict["user_role"]+p]
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
        day, month, year = map(int, date.split('.'))
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
