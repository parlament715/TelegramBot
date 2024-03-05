from aiogram.filters import BaseFilter
from typing import Union
from aiogram.types import Message
class FilterId(BaseFilter):  # [1]
    def __init__(self, my_id: Union[str, list]): # [2]
        self.my_id = my_id

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.my_id, str):
            return str(message.from_user.id) == self.my_id
        else:
            return str(message.from_user.id) in self.my_id
  