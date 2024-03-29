from aiogram.fsm.state import State, StatesGroup
class my_user:
  def __init__(self,id,role,name,func):
    self.name = name
    self.id = id
    self.role = role ##### классный воспитатель
    self.func = func

class Form(StatesGroup):
  user_role = State()
  user_name = State()
  date = State()
  time = State()
  num = State()

    










    
    
    
