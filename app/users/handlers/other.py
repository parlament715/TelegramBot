from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.users.filter_class import FilterId
from icecream import ic
from app.users.objects_class import ID_TEACHER, ID_VOSP, ID_MAIN_VOSP

router = Router()


############################ router #####################
async def rewrite_state_data(state: FSMContext, param: str):
    data = await state.get_data()
    date = data["date"]
    user_name = data["user_name"]
    user_role = data["user_role"]
    await state.clear()
    await state.update_data(user_name=user_name, user_role=user_role)
    if param == "same":
        await state.update_data(date=date)
