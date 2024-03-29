from icecream import ic
def split_2d_array_more_units(arr):
    """
    Функция для разбиения двумерного массива на большее количество единиц.
    
    :param arr: Исходный двумерный массив
    :return: Двумерный массив с большим количеством единиц
    """
    result = []
    for row in arr:
        new_row = []
        for element in row:
            new_row.extend([element]*2)  # Увеличиваем количество единиц в каждом подмассиве
        result.extend([new_row]*2)  # Повторяем подмассивы для увеличения количества единиц
    return result
def convert_mapl_list(arr):
    value = 1
    y = 0
    for columns in arr:
        arr[y] =columns[::value]
        y += 1
        value *=-1
    return arr
a = convert_mapl_list([[2, 1, 7], [1, 1, 1], [1, 1, 1], [6, 1, 4]])
# ic(a)
# Пример использования функции
# original_array = [[2, 1, 7], [1, 1, 1], [1, 1, 1], [6, 1, 1]]
result_array = split_2d_array_more_units(a)
ic(result_array)
