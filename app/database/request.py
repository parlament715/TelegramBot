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
                    breakfast TEXT, 
                    lunch TEXT, 
                    snacks TEXT, 
                    dinner TEXT,  
                    role TEXT)
                    ''')
                
    
def to_write(dict : dict):
    name = dict["user_name"]                  ### приводим в порядок данные 
    my_date = dict["date"]  ### перед записью
    time_ = dict["time"]
    try:
        number = dict["num"].replace(" ","/")
    except:
        number = dict["num"]
    user_role = dict["user_role"]
    table_columns = {
            "Завтрак": "breakfast",
            "Обед": "lunch",
            "Полдник": "snacks",
            "Ужин": "dinner",
        }

    time = table_columns[time_]
    # ic(time )
    to_create(str(my_date))
    res = cursor.execute(f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}" ''' ).fetchone()
    if res == None:
        cursor.execute(f''' INSERT INTO "{str(my_date)}" 
                       (who, role, {time}) VALUES ("{name}","{user_role}","{number}")''') ### если записи ещё не было то добавляем
    else:
        cursor.execute(f''' UPDATE "{str(my_date)}" SET {time} = "{number}" WHERE who = "{name}" ''') ### если была то уже обновляем то что было 
    conn.commit()
    conn.close()

def to_read_db(table_name : str,columns : str) -> list:
    to_create(table_name)
    cursor.execute(f'''SELECT {columns} FROM "{table_name}"''')
    a = cursor.fetchall()
    b = []
    for i in a:
        b.append(str(i[0]))
    return b
def check_on_exist(dict: dict) -> Optional[tuple]:
    name = dict["user_name"]
    my_date = dict["date"]
    time_ = dict["time"]

    table_columns = {
            "Завтрак": "breakfast",
            "Обед": "lunch",
            "Полдник": "snacks",
            "Ужин": "dinner",
        }

    time = table_columns[time_]
    to_create(my_date)

    res = cursor.execute(f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}"''' ).fetchone()

    if res != (None,) or None:
        return res
    return None


def sql_call_read(date : str, column : str, role: str):
    column11 = []
    column10 = []
    try:
        temp = cursor.execute(f'''SELECT "{column}" FROM "{date}" WHERE "role" = "{role}" ''').fetchall()
        for i in temp:
            if i[0] != None:
                column11.append(int((i[0]).split("/")[0]))
                column10.append(int((i[0]).split("/")[1]))
    except:
        logging.error("request error", exc_info=True)
    return column11, column10

def fill_template(template_path : str, output_path : str, context : dict):
    # Загрузка шаблона
    doc = DocxTemplate(template_path)
    # Замена плейсхолдеров
    doc.render(context)
    # Сохранение документа
    doc.save(output_path)

def get_data_for_docx(date:str) -> dict:
    to_create(date)
    breakfast_class_11_dorm, breakfast_class_10_dorm = sql_call_read(date, "breakfast", "Воспитатель")      
    breakfast_class_11_city, breakfast_class_10_city = sql_call_read(date, "breakfast", "Классный советник")
    sum_breakfast_class_11_dorm = sum(breakfast_class_11_dorm)
    sum_breakfast_class_10_dorm = sum(breakfast_class_10_dorm)
    sum_breakfast_class_10_city = sum(breakfast_class_10_city)
    sum_breakfast_class_11_city = sum(breakfast_class_11_city)

    dinner_class_11_dorm,dinner_class_10_dorm = sql_call_read(date, "dinner", "Воспитатель")
    sum_dinner_class_11_dorm = sum(dinner_class_11_dorm)
    sum_dinner_class_10_dorm = sum(dinner_class_10_dorm)

    _temp_lunch_class_11, _temp_lunch_class_10 = sql_call_read(date, "lunch", "Классный советник")
    sum_lunch_class_11 = sum(_temp_lunch_class_11)
    sum_lunch_class_10 = sum(_temp_lunch_class_10)
    sum_lunch_class_10_city = sum_lunch_class_10 - sum_dinner_class_10_dorm
    sum_lunch_class_11_city = sum_lunch_class_11 - sum_dinner_class_11_dorm
    sum_lunch_class_10_dorm = sum_dinner_class_10_dorm
    sum_lunch_class_11_dorm = sum_dinner_class_11_dorm

    _temp_snacks_class_11, _temp_snacks_class_10 = sql_call_read(date, "snacks", "Классный советник")
    sum_snacks_class_11 = sum(_temp_snacks_class_11)
    sum_snacks_class_10 = sum(_temp_snacks_class_10)
    sum_snacks_class_10_city = sum_snacks_class_10 - sum_dinner_class_10_dorm
    sum_snacks_class_11_city = sum_snacks_class_11 - sum_dinner_class_11_dorm
    sum_snacks_class_10_dorm = sum_dinner_class_10_dorm
    sum_snacks_class_11_dorm = sum_dinner_class_11_dorm
    
    dinner_class_11_dorm,dinner_class_10_dorm = sql_call_read(date, "dinner", "Воспитатель")

    #### разбиваем дату 
    year,month,day = map(int, date.split('-'))
    months_genitive = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]
    month = months_genitive[month - 1]
    content = {
        "data_num" : str(day),
        "data_month" : month,
        "data_year" : str(year),
        "a" : str(sum_breakfast_class_10_city + sum_breakfast_class_11_city),
        "b" : str(sum_breakfast_class_10_dorm + sum_breakfast_class_11_dorm),
        "c" : str(sum_lunch_class_10_city + sum_lunch_class_11_city),
        "d" : str(sum_lunch_class_10_dorm + sum_lunch_class_11_dorm),
        "e" : str(sum_snacks_class_10_city + sum_snacks_class_11_city),
        "f" : str(sum_snacks_class_10_dorm + sum_snacks_class_11_dorm),
        "g" : "0",
        "h" : str(sum_dinner_class_10_dorm + sum_dinner_class_11_dorm),
        "i" : str(sum_breakfast_class_10_city),
        "j" : str(sum_breakfast_class_10_dorm),
        "k" : str(sum_breakfast_class_11_city),
        "l" : str(sum_breakfast_class_11_dorm),
        "m" : str(sum_lunch_class_10_city),
        "n" : str(sum_lunch_class_10_dorm),
        "o" : str(sum_lunch_class_11_city),
        "p" : str(sum_lunch_class_11_dorm),
        "q" : str(sum_snacks_class_10_city),
        "r" : str(sum_snacks_class_10_dorm),
        "s" : str(sum_snacks_class_11_city),
        "t" : str(sum_snacks_class_11_dorm),
        "u" : "0",
        "v" : "0",
        "w" : str(sum_dinner_class_10_dorm),
        "x" : str(sum_dinner_class_11_dorm),
    }
    fill_template("example.docx","docx.docx",content)

    