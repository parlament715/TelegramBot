import sqlite3
# from app.database.table import dataframe_to_png_with_subcolumns

def to_create(date):
    global cursor, conn
    conn = sqlite3.connect('request.db')

    cursor = conn.cursor()

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS 
"{date}" (who TEXT, breakfast_dormitory INTEGER, breakfast_city INTEGER, lunch_dormitory INTEGER, lunch_city INTEGER,  dinner_dormitory INTEGER, dinner_city INTEGER )''')
                
    
def to_write(list : list):
    name = list[0]                  ### приводим в порядок данные 
    my_date = list[1].split()[1]    ### перед записью
    time = list[2]
    number = int(list[3])
    if time == "Ужин":
        time = 'dinner_dormitory'
    if time == "Обед":
        time = 'lunch_dormitory'
    if time == "Завтрак": 
        time = "breakfast_dormitory"
    to_create(str(my_date))
    cursor.execute(f''' INSERT INTO "{str(my_date)}" (who, {time}) VALUES ("{name}",{number})''')
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