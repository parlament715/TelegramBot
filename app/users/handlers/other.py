from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import kb1, kb_time_for_teacher, kb_date_all, kb_date_for_teacher, kb4, remove, gen_keyboard_time_for_vosp, kb_check_other_date, kb5, kb6
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from app.database.request import to_write, check_on_exist, get_data_for_docx
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot
from app.users.filter_class import FilterId, Filter_data
from app.users.objects_class import read_list, write_list
from icecream import ic
from app.users.objects_class import find_user_name_by_id, find_user_role_by_id, find_user_classroom_number_by_id
from app.users.main_class import Form
from config import ADMIN

router = Router()


##################### /help ################
@router.message(F.text == "/help", FilterId(read_list))
async def help_reaction_for_read(message: Message):
    await message.answer(
        'Для того чтобы посмотреть данные введите /start далее следуйте инструкциям. На этапе выбора даты можете ввести свою дату так и выбрать вариант из предложенных, в случае отсутствия записи вы получи сообщение : "Ошибка, этой таблицы скорее всего пустая". После каждого просмотра придётся вводить команду /start заново. Если возникли трудности обращайтесь в лс @paralment'
    )


@router.message(F.text == "/help", FilterId(write_list))
async def help_reaction_for_read(message: Message):

    await message.answer(
        'Для того чтобы занести данные вам нужно написать команду /start далее следовать согласно инструкциям, после каждой записи нужно заново прописывать команду /start'
    )


############################ router #####################
async def rewrite_state_data(state: FSMContext, param: str):
    data = await state.get_data()
    date = data["date"]
    user_name = data["user_name"]
    user_role = data["user_role"]
    if data["user_role"] == "Классный советник":
        classroom_number = data["classroom_number"]
    await state.clear()
    if data["user_role"] == "Классный советник":
        await state.update_data(user_name=user_name, classroom_number=classroom_number, user_role=user_role)
    elif data["user_role"] == "Воспитатель":
        await state.update_data(user_name=user_name, user_role=user_role)
    if param == "same":
        await state.update_data(date=date)
