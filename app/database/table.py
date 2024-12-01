import pandas as pd
from icecream import ic
from typing import Union
import matplotlib.pyplot as plt
from app.database.request import to_read_db
# from config import today


def get_png(table_name) -> Union[list]:
    # Создание данных для таблицы
    listik = []
    data_name_dorm = to_read_db(
        table_name, "who", where='role = "Воспитатель"')
    data_name_class = to_read_db(
        table_name, "who", where='role = "Классный советник"')

    if data_name_class != []:
        listik.append("table_class.png")
        data_breakfast_city = to_read_db(
            table_name, "breakfast_city", where='"role" = "Классный советник"')
        data_lunch_dorm = to_read_db(
            table_name, "lunch_dorm", where='"role" = "Классный советник"')
        data_lunch_city = to_read_db(
            table_name, "lunch_city", where='"role" = "Классный советник"')
        data_snack_dorm = to_read_db(
            table_name, "snack_dorm", where='"role" = "Классный советник"')
        data_snack_city = to_read_db(
            table_name, "snack_city", where='"role" = "Классный советник"')
        data_class = {'Название': data_name_class,
                      'Завтрак город': data_breakfast_city,
                      'Обед город': data_lunch_city,
                      'Обед общ.': data_lunch_dorm,
                      'Полдник город': data_snack_city,
                      'Полдник общ.': data_snack_dorm, }

    if data_name_dorm != []:
        listik.append("table_dorm.png")
        data_breakfast_dorm = to_read_db(
            table_name, "breakfast_dorm", where='role = "Воспитатель"')
        data_dinner_dorm = to_read_db(
            table_name, "dinner_dorm", where='role = "Воспитатель"')
        data_dorm = {'Название': data_name_dorm,
                     'Завтрак': data_breakfast_dorm,
                     'Ужин': data_dinner_dorm, }
        # Если таблица пустая то return Error

    # Создание DataFrame из данных
    if "table_class.png" in listik:
        ic(data_class)
        df_class = pd.DataFrame(data_class)
        # Создание изображения таблицы и сохранение в формате PNG
        fig, ax = plt.subplots()
        ax.axis('off')  # Убираем оси координат
        tabla = ax.table(cellText=df_class.values,
                         colLabels=df_class.columns, loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(12)
        tabla.scale(1.8, 1.5)
        plt.savefig('table_class.png', bbox_inches='tight', pad_inches=0.05)

    if "table_dorm.png" in listik:
        df_dorm = pd.DataFrame(data_dorm)

        # Создание изображения таблицы и сохранение в формате PNG
        fig, ax = plt.subplots()
        ax.axis('off')  # Убираем оси координат
        tabla = ax.table(cellText=df_dorm.values,
                         colLabels=df_dorm.columns, loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(12)
        tabla.scale(1.8, 1.5)
        plt.savefig('table_dorm.png', bbox_inches='tight', pad_inches=0.05)

    return listik
