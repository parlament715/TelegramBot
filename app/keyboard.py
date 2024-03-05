from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton as KButton

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
remove = ReplyKeyboardRemove()


