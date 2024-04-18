import pandas as pd
from icecream import ic
from typing import Union
import matplotlib.pyplot as plt
from app.database.request import to_read_db
# from config import today
def get_png(table_name) -> Union[None,str] :
  # Создание данных для таблицы
  data_name = to_read_db(table_name,"who")
  data_breakfast = to_read_db(table_name,"breakfast")
  data_snack = to_read_db(table_name,"snacks")
  data_lunch = to_read_db(table_name,"lunch")
  data_dinner = to_read_db(table_name,"dinner")
  data = {'Название': data_name,
          'Завтрак': data_breakfast,
          'Обед': data_lunch,
          'Полдник': data_snack,
          'Ужин' : data_dinner,}
  # if today == 6:  # today is Sunday
  #   data['Обед'] = data_lunch_dormitory
  ic(data)
  if data['Название'] == []: ### Если таблица пустая то return none
    return "Error"

  # Создание DataFrame из данных
  df = pd.DataFrame(data)

  # Создание изображения таблицы и сохранение в формате PNG
  fig, ax = plt.subplots()
  ax.axis('off')  # Убираем оси координат
  tabla = ax.table(cellText=df.values, colLabels=df.columns, loc='center')
  tabla.auto_set_font_size(False)
  tabla.set_fontsize(12)
  tabla.scale(1.5, 1.5)
  plt.savefig('table.png', bbox_inches='tight', pad_inches=0.05)
  return None
  # plt.show()




