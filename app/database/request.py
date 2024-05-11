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
                    breakfast_dorm_11 INTEGER,
                    breakfast_dorm_10 INTEGER,
                    breakfast_city_11 INTEGER,
                    breakfast_city_10 INTEGER, 
                    lunch_dorm_11 INTEGER,
                    lunch_dorm_10 INTEGER,
                    lunch_city_11 INTEGER,
                    lunch_city_10 INTEGER, 
                    snack_dorm_11 INTEGER,
                    snack_dorm_10 INTEGER,
                    snack_city_11 INTEGER,
                    snack_city_10 INTEGER,
                    dinner_dorm_11 INTEGER,
                    dinner_dorm_10 INTEGER, 
                    role TEXT)
                    ''')
                
def to_write(my_dict:dict):
    name = my_dict["user_name"]
    role = my_dict["user_role"]
    my_date = my_dict['date']
    num_list = my_dict["num"].split()
    to_create(str(my_date))
    for (index,column_name) in  enumerate(from_dict_to_name_column(my_dict)):
        num = num_list[index]
        res = cursor.execute(f''' SELECT {column_name} FROM "{str(my_date)}" WHERE who = "{name}" ''' ).fetchone()
        if res == None:
            cursor.execute(f''' 
                        INSERT INTO "{str(my_date)}" 
                        (who, role, {column_name}) VALUES 
                        ("{name}","{role}",{num})
                            ''') ### если записи ещё не было то добавляем
        else:
            cursor.execute(f''' UPDATE "{str(my_date)}" SET {column_name} = "{num}" WHERE who = "{name}" ''') ### если была то уже обновляем то что было 
    conn.commit()
    conn.close()

def from_dict_to_name_column(dict : dict) -> list:
    listik = []             ### приводим в порядок данные перед записью
    time = dict["time"]
    role = dict["user_role"]
    if role == "Классный советник":
        class_num = dict["classroom_number"]
    else:
        class_num = "None"
    column_names = {
        "Завтрак Классный советник 11": "breakfast_city_11",
        "Завтрак Классный советник 10": "breakfast_city_10",
        "Завтрак Воспитатель 11": "breakfast_dorm_11",
        "Завтрак Воспитатель 10": "breakfast_dorm_10",
        "Обед Классный советник 11": "lunch_city_11",
        "Обед Классный советник 10": "lunch_city_10",
        "Обед Классный советник 11 dorm": "lunch_dorm_11",
        "Обед Классный советник 10 dorm": "lunch_dorm_10",
        "Полдник Классный советник 11": "snack_city_11",
        "Полдник Классный советник 10": "snack_city_10",
        "Полдник Классный советник 11 dorm": "snack_dorm_11",
        "Полдник Классный советник 10 dorm": "snack_dorm_10",
        "Ужин Воспитатель 11" : "dinner_dorm_11",
        "Ужин Воспитатель 10" : "dinner_dorm_10",

    }
    _column_name = time + " "+ role
    if role =='Классный советник' and time == 'Завтрак':
        _column_name += f' {str(class_num)}'
        column_name = column_names[_column_name]
        listik.append(column_name)
    elif role == "Классный советник" and (time == "Обед" or time == "Полдник"):
        _column_name += f' {str(class_num)}'
        column_name = column_names[_column_name]
        listik.append(column_name)
        # to_to_write(my_date,column_name,name,class_num,num.split()[0])
        _column_name += " dorm"
        column_name = column_names[_column_name]
        listik.append(column_name)
        # to_to_write(my_date,column_name,name,class_num,num.split()[1])
    elif role == "Воспитатель":
        listik.append(column_names[_column_name + ' 11'])
        listik.append(column_names[_column_name + ' 10'])
    return listik

def to_read_db(table_name : str,columns : str, where : Optional[str] = None) -> list:
    to_create(table_name)
    if where != None:
        cursor.execute(f'''SELECT {columns} FROM "{table_name}" WHERE {where}''')
    else:
        cursor.execute(f'''SELECT {columns} FROM "{table_name}"''')
    a = cursor.fetchall()
    b = []
    for i in a:
        b.append(str(i[0])) #### преобразовываем в массив из кортежа для красоты
    return b

def check_on_exist(my_dict: dict) -> Union[list,None]:
    name = my_dict["user_name"]
    my_date = my_dict["date"]
    time = my_dict["time"]
    role = my_dict["user_role"]
    res = []


    to_create(my_date)
    for time in from_dict_to_name_column(my_dict):
        a = cursor.execute(f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}"''' ).fetchone()
        if a != None and a != (None,):
            res.append(a[0])

    if res != []:
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
        "v" : str(sum_dinner_class_10_dorm),
        "w" : "0",
        "x" : str(sum_dinner_class_11_dorm),
    }
    fill_template("example.docx","docx.docx",content)

    