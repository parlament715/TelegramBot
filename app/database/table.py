import pandas as pd
from icecream import ic
from typing import Union
import matplotlib.pyplot as plt
from app.database.request import to_read_db
# from config import today

def get_png(table_name) -> Union[None,str] :
  # Создание данных для таблицы
  data_name_10 = to_read_db(table_name,"who",where="class_num=10")
  data_breakfast_city_10 = to_read_db(table_name,"breakfast_city_10",where="class_num=10")
  data_lunch_dorm_10 = to_read_db(table_name,"lunch_dorm_10",where="class_num=10")
  data_lunch_city_10 = to_read_db(table_name,"lunch_city_10",where="class_num=10")
  data_snack_dorm_10 = to_read_db(table_name,"snack_dorm_10",where="class_num=10")
  data_snack_city_10 = to_read_db(table_name,"snack_city_10",where="class_num=10")
  data_class_10 = {'Название': data_name_10,
          'Завтрак город': data_breakfast_city_10,
          'Обед город': data_lunch_city_10,
          'Обед общ.': data_lunch_dorm_10,
          'Полдник город': data_snack_city_10,
          'Полдник общ.': data_snack_dorm_10,}
  
  data_name_11 = to_read_db(table_name,"who",where="class_num=11")
  data_breakfast_city_11 = to_read_db(table_name,"breakfast_city_11",where="class_num=11")
  data_lunch_dorm_11 = to_read_db(table_name,"lunch_dorm_11",where="class_num=11")
  data_lunch_city_11 = to_read_db(table_name,"lunch_city_11",where="class_num=11")
  data_snack_dorm_11 = to_read_db(table_name,"snack_dorm_11",where="class_num=11")
  data_snack_city_11 = to_read_db(table_name,"snack_city_11",where="class_num=11")
  data_class_11 = {'Название': data_name_11,
          'Завтрак город': data_breakfast_city_11,
          'Обед город': data_lunch_city_11,
          'Обед общ.': data_lunch_dorm_11,
          'Полдник город': data_snack_city_11,
          'Полдник общ.': data_snack_dorm_11,}
  
  data_name_dorm = to_read_db(table_name,"who",where='role = "Воспитатель"')
  data_breakfast_dorm_11 = to_read_db(table_name,"breakfast_dorm_11",where='role = "Воспитатель"')
  data_breakfast_dorm_10 = to_read_db(table_name,"breakfast_dorm_10",where='role = "Воспитатель"')
  data_dinner_dorm_10 = to_read_db(table_name,"dinner_dorm_10",where='role = "Воспитатель"')
  data_dinner_dorm_11 = to_read_db(table_name,"dinner_dorm_11",where='role = "Воспитатель"')
  data_dorm = {'Название': data_name_dorm,
          'Завтрак 11': data_breakfast_dorm_11,
          'Завтрак 10': data_breakfast_dorm_10,
          'Ужин 11': data_dinner_dorm_11,
          'Ужин 10': data_dinner_dorm_10,}
  # if today == 6:  # today is Sunday
  #   data['Обед'] = data_lunch_dormitory
  ic(data_class_10)
  ic(data_class_11)
  ic(data_dorm)
  if data_class_10['Название'] == [] or data_class_11['Название'] == [] or data_dorm['Название'] == []: ### Если таблица пустая то return Error
    return "Error"

  # Создание DataFrame из данных
  df_class_10 = pd.DataFrame(data_class_10)

  # Создание изображения таблицы и сохранение в формате PNG
  fig, ax = plt.subplots()
  ax.axis('off')  # Убираем оси координат
  tabla = ax.table(cellText=df_class_10.values, colLabels=df_class_10.columns, loc='center')
  tabla.auto_set_font_size(False)
  tabla.set_fontsize(12)
  tabla.scale(1.8, 1.5)
  plt.savefig('table_class_10.png', bbox_inches='tight', pad_inches=0.05)

  df_class_11 = pd.DataFrame(data_class_11)

  # Создание изображения таблицы и сохранение в формате PNG
  fig, ax = plt.subplots()
  ax.axis('off')  # Убираем оси координат
  tabla = ax.table(cellText=df_class_11.values, colLabels=df_class_11.columns, loc='center')
  tabla.auto_set_font_size(False)
  tabla.set_fontsize(12)
  tabla.scale(1.8, 1.5)
  plt.savefig('table_class_11.png', bbox_inches='tight', pad_inches=0.05)

  if data_dorm['Название'] != []:
        df_dorm = pd.DataFrame(data_dorm)

        # Создание изображения таблицы и сохранение в формате PNG
        fig, ax = plt.subplots()
        ax.axis('off')  # Убираем оси координат
        tabla = ax.table(cellText=df_dorm.values, colLabels=df_dorm.columns, loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(12)
        tabla.scale(1.8, 1.5)
        plt.savefig('table_dorm.png', bbox_inches='tight', pad_inches=0.05)


  # plt.show()




