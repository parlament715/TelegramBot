import pandas as pd
from icecream import ic
from typing import Union
import matplotlib.pyplot as plt
from app.database.request import to_read_db
# from config import today
def split_foreach(a : list, split : str, num_list_elem : int) -> list:
   b = []
   for elem in a:
      if elem != "None":
        b.append(elem.split(split)[num_list_elem])
      else:
        b.append("None")
   return b

def get_png(table_name) -> Union[None,str] :
  # Создание данных для таблицы
  data_name_class_10 = to_read_db(table_name,"who",where="class_num=10")
  data_breakfast_class_10 = split_foreach(to_read_db(table_name,"breakfast",where="class_num=10"),"/",1)
  data_snack_class_10 = split_foreach(to_read_db(table_name,"snacks",where="class_num = 10"),"/",1)
  data_lunch_class_10 = split_foreach(to_read_db(table_name,"lunch",where="class_num = 10"),"/",1)
  data_dinner_class_10 = split_foreach(to_read_db(table_name,"dinner",where="class_num = 10"),"/",1)
  data_class_10 = {'Название': data_name_class_10,
          'Завтрак': data_breakfast_class_10,
          'Обед': data_lunch_class_10,
          'Полдник': data_snack_class_10,
          'Ужин' : data_dinner_class_10,}
  
  data_name_class_11 = to_read_db(table_name,"who",where="class_num = 11")
  data_breakfast_class_11 = split_foreach(to_read_db(table_name,"breakfast",where="class_num = 11"),"/",0)
  data_snack_class_11 = split_foreach(to_read_db(table_name,"snacks",where="class_num = 11"),"/",0)
  data_lunch_class_11 = split_foreach(to_read_db(table_name,"lunch",where="class_num = 11"),"/",0)
  data_dinner_class_11 = split_foreach(to_read_db(table_name,"dinner",where="class_num = 11"),"/",0)
  data_class_11 = {'Название': data_name_class_11,
          'Завтрак': data_breakfast_class_11,
          'Обед': data_lunch_class_11,
          'Полдник': data_snack_class_11,
          'Ужин' : data_dinner_class_11,}
  
  data_name_dorm = to_read_db(table_name,"who",where='role = "Воспитатель"')
  data_breakfast_dorm = to_read_db(table_name,"breakfast",where='role = "Воспитатель"')
  data_snack_dorm = to_read_db(table_name,"snacks",where='role = "Воспитатель"')
  data_lunch_dorm = to_read_db(table_name,"lunch",where='role = "Воспитатель"')
  data_dinner_dorm = to_read_db(table_name,"dinner",where='role = "Воспитатель"')
  data_dorm = {'Название': data_name_dorm,
          'Завтрак': data_breakfast_dorm,
          'Обед': data_lunch_dorm,
          'Полдник': data_snack_dorm,
          'Ужин' : data_dinner_dorm,}
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
  tabla.scale(1.5, 1.5)
  plt.savefig('table_class_10.png', bbox_inches='tight', pad_inches=0.05)

  df_class_11 = pd.DataFrame(data_class_11)

  # Создание изображения таблицы и сохранение в формате PNG
  fig, ax = plt.subplots()
  ax.axis('off')  # Убираем оси координат
  tabla = ax.table(cellText=df_class_11.values, colLabels=df_class_11.columns, loc='center')
  tabla.auto_set_font_size(False)
  tabla.set_fontsize(12)
  tabla.scale(1.5, 1.5)
  plt.savefig('table_class_11.png', bbox_inches='tight', pad_inches=0.05)

  if data_dorm['Название'] != []:
        df_dorm = pd.DataFrame(data_dorm)

        # Создание изображения таблицы и сохранение в формате PNG
        fig, ax = plt.subplots()
        ax.axis('off')  # Убираем оси координат
        tabla = ax.table(cellText=df_dorm.values, colLabels=df_dorm.columns, loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(12)
        tabla.scale(1.5, 1.5)
        plt.savefig('table_dorm.png', bbox_inches='tight', pad_inches=0.05)


  # plt.show()




