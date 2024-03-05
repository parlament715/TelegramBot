from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton as KButton
from aiogram.types import InlineKeyboardMarkup as InlKB
from aiogram.types import InlineKeyboardButton as InKButton

from datetime import  datetime, timedelta 

kb1 = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=
                         [[KButton(text = 'Я старший воспитатель')],
                          [KButton(text = 'Я воспитатель')]])

today = datetime.now().date()

keyboard_0x000 = [[KButton(text=f'Сегодня {str(today)}')],
                  [KButton(text = f'Завтра {str(today + timedelta(days = 1))}')],
                  [KButton(text = f'Послезавтра {str(today + timedelta(days= 2))}')]
                  ]

kb2 = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard_0x000)

keyboard_0x001 = [[KButton(text='Завтрак')],
                  [KButton(text = 'Обед')],
                  [KButton(text = 'Ужин')]
                  ]

kb3 = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard_0x001)

kb4 = InlKB(inline_keyboard=[
  [InKButton(text="Да",callback_data="Yes"),
  InKButton(text="Нет",callback_data="No")]
])

remove = ReplyKeyboardRemove()



