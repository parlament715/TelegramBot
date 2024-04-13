from aiogram.filters import BaseFilter
from typing import Union, Any
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from icecream import ic
class FilterId(BaseFilter):  # [1]
    def __init__(self, my_id: Union[str, list]): # [2]
        self.my_id = my_id

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.my_id, str):
            return str(message.from_user.id) == self.my_id
        else:
            return str(message.from_user.id) in self.my_id
class Filter_data(BaseFilter):
    def __init__(self, key : str, value : Union[str,int]):
        self.value = value
        self.key = key
    async def __call__(self, event: Any, state: FSMContext) -> bool:
        data = await state.get_data()
        try:
            return data[self.key] == self.value
        except KeyError:
            ic("Ошибка : неправильно передан ключ в фильтр")
            return False
  