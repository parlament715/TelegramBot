from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton as KButton
from aiogram.types import InlineKeyboardMarkup as InlKB
from aiogram.types import InlineKeyboardButton as InKButton

from datetime import  datetime, timedelta 

kb1 = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=
                         [[KButton(text = 'Я старший воспитатель')],
                          [KButton(text = 'Я воспитатель')]])

today = datetime.now().date() + timedelta(days=2)

keyboard_0x000 = [[KButton(text=f'Сегодня {str(today)}')],
                  [KButton(text = f'Завтра {str(today + timedelta(days = 1))}')],
                  [KButton(text = f'Послезавтра {str(today + timedelta(days= 2))}')]
                  ]

if today.weekday() >= 4:
  if today.weekday() == 4:
    keyboard_0x002 = [[KButton(text=f'Сегодня {str(today)}')],
                  [KButton(text = f'Завтра {str(today + timedelta(days = 1))}')],
                  ]
  elif today.weekday() == 5:
    keyboard_0x002 = [[KButton(text=f'Сегодня {str(today)}')],
                  [KButton(text = f'Послезавтра {str(today + timedelta(days= 2))}')],
                  ]
  elif today.weekday() == 6:
    keyboard_0x002 = [[KButton(text = f'Завтра {str(today + timedelta(days = 1))}')],
                  [KButton(text = f'Послезавтра {str(today + timedelta(days= 2))}')]
                  ]
else:
  keyboard_0x002 = keyboard_0x000


kb_date_all = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard_0x000)

kb_date_for_teacher = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard_0x002)



def gen_keyboard_time_for_vosp(date:str):
  date_obj = datetime.strptime(date,'%Y-%m-%d')
  if date_obj.weekday() == 6:
    keyboard_0x002 = [[KButton(text='Завтрак'),KButton(text='Обед')],
                      [KButton(text='Полдник'),KButton(text = 'Ужин')],
                      [KButton(text = 'Второй ужин')]
                     ]
  else:
    keyboard_0x002 = [[KButton(text='Завтрак')],
                      [KButton(text = 'Ужин')],
                      [KButton(text = 'Второй ужин')]
                     ]
    
  return ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard_0x002)

  
keyboard_0x001 = [[KButton(text='Завтрак')],
                  [KButton(text = 'Обед')],
                  [KButton(text = 'Полдник')]
                  ]

kb_time_for_teacher = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=keyboard_0x001)



kb4 = InlKB(inline_keyboard=[
  [InKButton(text="Да",callback_data="Yes"),
  InKButton(text="Нет",callback_data="No")]
])

remove = ReplyKeyboardRemove()



