import pandas as pd
import matplotlib.pyplot as plt
from app.database.request import to_read_db
def get_png(table_name):
  # Создание данных для таблицы
  data_name = to_read_db(table_name,"who")
  data_breakfast = to_read_db(table_name,"breakfast_dormitory")
  data_lunch = to_read_db(table_name,"lunch_dormitory")
  data_dinner = to_read_db(table_name,"dinner_dormitory")
  data = {'Название': data_name,
          'Завтрак': data_breakfast,
          'Обед': data_lunch,
          'Ужин' : data_dinner}

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
  # plt.show()


