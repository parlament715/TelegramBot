import sqlite3
from icecream import ic
from typing import Union, Optional
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
                    second_dinner TEXT, 
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
            "Второй ужин": "second_dinner",
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
    user_role = dict["user_role"]

    table_columns = {
            "Завтрак": "breakfast",
            "Обед": "lunch",
            "Полдник": "snacks",
            "Ужин": "dinner",
            "Второй ужин": "second_dinner",
        }

    time = table_columns[time_]
    to_create(my_date)

    res = cursor.execute(f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}"''' ).fetchone()

    if res != (None,) or None:
        return res
    return None


# def get_data_for_docx(date:str) -> dict:
#     to_create(date)

#     cursor.execute(f'''SELECT "breakfast" FROM "{date}" WHERE "role" = "Воспитатель" ''')
#     breakfast_class_10_dorm = 
#     breakfast_class_10_city = 
#     breakfast_class_11_dorm = 
#     breakfast_class_11_city = 
#     lunch_class_10_dorm = 
#     lunch_class_10_city = 
#     lunch_class_11_dorm = 
#     lunch_class_11_city = 
#     dinner_class_10_dorm = 
#     dinner_class_10_city = 
#     dinner_class_11_dorm = 
#     dinner_class_11_city = 

    