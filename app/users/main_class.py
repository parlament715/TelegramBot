from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    user_role = State()
    user_name = State()
    date = State()
    time = State()
    num = State()
