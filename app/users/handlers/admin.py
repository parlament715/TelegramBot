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
from icecream import ic
from app.users.objects_class import find_user_name_by_id
from app.users.main_class import Form
from config import ADMIN
router = Router()


@router.message(CommandStart(), FilterId(ADMIN))
async def admin_panel_reaction(message: Message, state: FSMContext):
    await message.answer('Админ панель', reply_markup=kb1)


@router.message(F.text == "Я старший воспитатель", FilterId(ADMIN))
async def first_keyboard_reaction(message: Message, state: FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all)

    await state.set_state("give_data")


@router.message(FilterId(ADMIN), F.text == "Я воспитатель")
async def second_keyboard_reaction(message: Message, state: FSMContext):
    await state.set_state("промежуточный выбор имени")
    await state.update_data(user_role="Воспитатель")

    await message.answer('Введите имя', reply_markup=remove)


@router.message(FilterId(ADMIN), F.text == "Я классный советник")
async def second_keyboard_reaction(message: Message, state: FSMContext):
    await state.set_state("промежуточный выбор номера класса")
    await state.update_data(user_role="Классный советник")
    await message.answer("Выберете класс", reply_markup=kb6)


@router.message(StateFilter("промежуточный выбор номера класса"))
async def select_num_class(message: Message, state: FSMContext):
    if message.text == "10":
        await state.set_state("промежуточный выбор имени")
        await state.update_data(classroom_number=10)
        await message.answer('Введите имя', reply_markup=remove)
    elif message.text == "11":
        await state.set_state("промежуточный выбор имени")
        await state.update_data(classroom_number=11)
        await message.answer('Введите имя', reply_markup=remove)


@router.message(StateFilter("промежуточный выбор имени"))
async def select_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await state.set_state(Form.date)
    data = await state.get_data()
    if data["user_role"] == "Классный советник":
        await message.answer('Выберете дату', reply_markup=kb_date_for_teacher)
    elif data["user_role"] == "Воспитатель":
        await message.answer('Выберете дату', reply_markup=kb_date_all)
