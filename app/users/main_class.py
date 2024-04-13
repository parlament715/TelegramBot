from aiogram.fsm.state import State, StatesGroup
class my_user:
  def __init__(self,id,func,**kwargs):
    dict_kwargs = {}
    for key,value in kwargs.items():
      dict_kwargs[key] = value
    self.id = id
    self.func = func
    if func == "write":
      self.name = dict_kwargs["name"]
      self.role = dict_kwargs["role"] ##### классный воспитатель
      if self.role == "Классный советник":
        self.classroom_number = dict_kwargs["classroom_number"] ## цифра класса для классных советников

class Form(StatesGroup):
  user_role = State()
  user_name = State()
  date = State()
  time = State()
  num = State()



    










    
    
    
