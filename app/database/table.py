import pandas as pd
from icecream import ic
from typing import Union
import matplotlib.pyplot as plt
from loader import rq
from datetime import datetime
# from config import today


def get_png(date) -> Union[list]:
    # Создание данных для таблицы
    listik = []
    with rq:
        if datetime.strptime(date, "%d.%m.%Y").weekday() == 6:
            vosp_table_name = "vosp_sunday"
        else:
            vosp_table_name = "vosp"
        data_name_dorm = rq.to_read_db(vosp_table_name, date, "name")
        data_name_class = rq.to_read_db("teacher", date, "name")

        if data_name_class != []:
            listik.append("table_class.png")
            data_breakfast_city = rq.to_read_db("teacher", date, "breakfast")
            data_lunch_dorm = rq.to_read_db("teacher", date, "lunch_dorm")
            data_lunch_city = rq.to_read_db("teacher", date, "lunch_city")
            data_snack_dorm = rq.to_read_db("teacher", date, "snack_dorm")
            data_snack_city = rq.to_read_db("teacher", date, "snack_city")
            data_class = {'Название': data_name_class,
                          'Завтрак город': data_breakfast_city,
                          'Обед город': data_lunch_city,
                          'Обед общ.': data_lunch_dorm,
                          'Полдник город': data_snack_city,
                          'Полдник общ.': data_snack_dorm, }

        if data_name_dorm != []:
            listik.append("table_dorm.png")
            data_breakfast_dorm = rq.to_read_db(
                vosp_table_name, date, "breakfast")
            data_dinner_dorm = rq.to_read_db(vosp_table_name, date, "dinner")
            data_last_dinner_dorm = rq.to_read_db(
                vosp_table_name, date, "last_dinner")
            if datetime.strptime(date, "%d.%m.%Y").weekday() == 6:
                data_lunch_dorm = rq.to_read_db(vosp_table_name, date, "lunch")
                data_snack_dorm = rq.to_read_db(vosp_table_name, date, "snack")
                data_dorm = {'Название': data_name_dorm,
                             'Завтрак': data_breakfast_dorm,
                             "Обед": data_breakfast_dorm,
                             "Полдник": data_snack_dorm,
                             'Ужин': data_dinner_dorm,
                             "Паужин": data_last_dinner_dorm}
            else:
                data_dorm = {'Название': data_name_dorm,
                             'Завтрак': data_breakfast_dorm,
                             'Ужин': data_dinner_dorm,
                             "Паужин": data_last_dinner_dorm}
        # Если таблица пустая то return Error

    # Создание DataFrame из данных
    if "table_class.png" in listik:
        df_class = pd.DataFrame(data_class).replace(
            "None", "Отсутствует")
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
        df_dorm = pd.DataFrame(data_dorm).replace(
            "None", "Отсутствует")

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


def get_png_history(user_name: str, user_role: str, date: datetime):
    with rq:
        if user_role == "Воспитатель":
            if datetime.strptime(date, "%d.%m.%Y").weekday() == 6:
                if len(rq.to_read_db("vosp_sunday", date, "name", f'name = "{user_name}"')) == 0:
                    return
                data_breakfast = rq.to_read_db(
                    "vosp_sunday", date, "breakfast", f'name = "{user_name}"')
                data_lunch = rq.to_read_db(
                    "vosp_sunday", date, "lunch", f'name = "{user_name}"')
                data_snack = rq.to_read_db(
                    "vosp_sunday", date, "snack", f'name = "{user_name}"')
                data_dinner = rq.to_read_db(
                    "vosp_sunday", date, "dinner", f'name = "{user_name}"')
                data_last_dinner = rq.to_read_db(
                    "vosp_sunday", date, "last_dinner", f'name = "{user_name}"')
                data_hist = {'Завтрак': data_breakfast,
                             'Обед': data_lunch,
                             'Полдник': data_snack,
                             'Ужин': data_dinner,
                             "Паужин": data_last_dinner}
            else:
                if len(rq.to_read_db("vosp", date, "name", f'name = "{user_name}"')) == 0:
                    return
                data_breakfast_dorm = rq.to_read_db(
                    "vosp", date, "breakfast", f'name = "{user_name}"')
                data_dinner_dorm = rq.to_read_db(
                    "vosp", date, "dinner", f'name = "{user_name}"')
                data_last_dinner = rq.to_read_db(
                    "vosp", date, "last_dinner", f'name = "{user_name}"')
                data_hist = {'Завтрак': data_breakfast_dorm,
                             'Ужин': data_dinner_dorm,
                             "Паужин": data_last_dinner}
        elif user_role == "Классный советник":
            if len(rq.to_read_db("teacher", date, "name", f'name = "{user_name}"')) == 0:
                return
            data_breakfast_city = rq.to_read_db(
                "teacher", date, "breakfast", f'name = "{user_name}"')
            data_lunch_dorm = rq.to_read_db(
                "teacher", date, "lunch_dorm", f'name = "{user_name}"')
            data_lunch_city = rq.to_read_db(
                "teacher", date, "lunch_city", f'name = "{user_name}"')
            data_snack_dorm = rq.to_read_db(
                "teacher", date, "snack_dorm", f'name = "{user_name}"')
            data_snack_city = rq.to_read_db(
                "teacher", date, "snack_city", f'name = "{user_name}"')
            data_hist = {'Завтрак город': data_breakfast_city,
                         'Обед город': data_lunch_city,
                         'Обед общ.': data_lunch_dorm,
                         'Полдник город': data_snack_city,
                         'Полдник общ.': data_snack_dorm, }
        else:
            raise Exception(
                "usee_role must be Воспитатель or Классный советник")
        df = pd.DataFrame(data_hist).replace("None", "Отсутствует")
        fig, ax = plt.subplots()
        ax.axis('off')  # Убираем оси координат
        tabla = ax.table(cellText=df.values,
                         colLabels=df.columns, loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(12)
        tabla.scale(1.8, 1.5)
        plt.savefig('table_history.png', bbox_inches='tight', pad_inches=0.05)
        return 0
