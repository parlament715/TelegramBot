import sqlite3
from icecream import ic
# from app.database.table import dataframe_to_png_with_subcolumns

def to_create(date):
    global cursor, conn
    conn = sqlite3.connect('request.db')

    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS 
"{date}" (who TEXT, breakfast_city TEXT, lunch_city TEXT, snacks_city TEXT, breakfast_dormitory TEXT, lunch_dormitory TEXT, snacks_dormitory TEXT,  dinner_dormitory TEXT, second_dinner_dormitory TEXT)''')
                
    
def to_write(dict : dict):
    name = dict["user_name"]                  ### приводим в порядок данные 
    my_date = dict["date"]  ### перед записью
    time = dict["time"]
    number = dict["num"]
    if dict["user_role"] == "Классный советник":
        match time:
            case "Завтрак":
                time = "breakfast_city"
            case "Обед":
                time = 'lunch_city'
            case "Полдник":
                time = "snacks_city"
    elif dict["user_role"] == "Воспитатель":
        match time:
            case "Завтрак":
                time = "breakfast_dormitory"
            case "Обед":
                time = 'lunch_dormitory'
            case "Полдник":
                time = "snacks_dormitory"
            case "Ужин":
                time = 'dinner_dormitory'
            case "Второй ужин":
                time = 'second_dinner_dormitory'
    # ic(time )
    to_create(str(my_date))
    res = cursor.execute(f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}" ''' ).fetchone()
    if res == None:
        cursor.execute(f''' INSERT INTO "{str(my_date)}" 
                       (who, {time}) VALUES ("{name}","{number}")''') ### если записи ещё не было то добавляем
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
def check_on_exist(dict : dict) -> int:
    name = dict["user_name"]                  ### приводим в порядок данные 
    my_date = dict["date"]    ### перед записью
    time = dict["time"]
    to_create(my_date)
    if dict["user_role"] == "Классный советник":
        match time:
            case "Завтрак":
                time = "breakfast_city"
            case "Обед":
                time = 'lunch_city'
            case "Полдник":
                time = "snacks_city"
    elif dict["user_role"] == "Воспитатель":
        match time:
            case "Завтрак":
                time = "breakfast_dormitory"
            case "Обед":
                time = 'lunch_dormitory'
            case "Полдник":
                time = "snacks_dormitory"
            case "Ужин":
                time = 'dinner_dormitory'
            case "Второй ужин":
                time = 'second_dinner_dormitory'
    res = cursor.execute(f''' SELECT {time} FROM "{str(my_date)}" WHERE who = "{name}"''' ).fetchone()

    if res != (None,) or None:
        return res
    return None
    