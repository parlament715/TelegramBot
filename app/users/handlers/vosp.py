from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import create_date_keyboard_for_vosp, yes_no_keyboard, remove, gen_keyboard_time_for_vosp, kb_check_other_date, kb5
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from app.database.request import to_write, check_on_exist, get_data_for_docx
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot
from app.users.filter_class import FilterId, Filter_data
from app.users.objects_class import ID_VOSP
from icecream import ic
from app.users.objects_class import find_user_name_by_id, find_user_classroom_number_by_id
from app.users.main_class import Form
from config import ADMIN
from app.users.handlers.other import rewrite_state_data
from app.decorators import dc_change_keyboard

router = Router()


@router.callback_query(F.data == "No")
async def call_back_data_reaction_No(call: CallbackQuery, state: FSMContext):
    print(f"{call.from_user.id} - {call.from_user.full_name} - отказался от записи teacher")
    await call.message.edit_text("Пожалуйста введите команду /start заново для записи")
    await state.clear()
    await call.answer()


@router.callback_query(F.data == "Yes")
async def call_back_data_reaction_Yes(call: CallbackQuery, state: FSMContext):
    print(f"{call.from_user.id} - {call.from_user.full_name} - согласился на запись teacher")
    await call.message.delete()
    await call.answer()
    data = await state.get_data()
    if data["user_role"] == "Классный советник":
        if data["time"] == "Завтрак":
            await call.message.answer("Сколько человек (Напишите числом)")
        elif data["time"] in ("Обед", "Полдник"):
            await call.message.answer('Сколько человек (количество городских, через пробел количество интернатных)')
    elif data["user_role"] == "Воспитатель":
        await call.message.answer('Сколько человек (и 11 классников и 10 классников в сумме)')
    await state.set_state(Form.num)


@router.message(FilterId(ID_VOSP), CommandStart())
async def second_keyboard_reaction(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - начал запись VOSP")
    await state.clear()

    await state.update_data(user_name=find_user_name_by_id(message.from_user.id),
                            user_role='Воспитатель')
    data = await state.get_data()
    keyboard = create_date_keyboard_for_vosp(data)
    if keyboard:
        await message.answer('Выберете дату', reply_markup=keyboard)
        await state.update_data(last_kb=keyboard)
        await state.set_state(Form.date)
    else:
        await message.answer('Сегодня отсутствуют даты для записи')


@router.callback_query(StateFilter(Form.date), Filter_data("user_role", "Воспитатель"))
@dc_change_keyboard(previous_name="call")
async def step_1_reaction(call: CallbackQuery, state: FSMContext):
    print(f"{call.from_user.id} - {call.from_user.full_name} - выбрал дату vosp")
    if call.data[0].isalpha():
        message_text = call.data.split()[1]
    else:
        message_text = call.data
    await state.update_data(date=message_text)
    data = await state.get_data()
    kb = gen_keyboard_time_for_vosp(data)
    await call.message.answer("Выберете время", reply_markup=kb)
    # await send_time()
    await state.set_state(Form.time)
    await state.update_data(last_kb=kb)
    await call.answer()


@router.callback_query(StateFilter(Form.time), Filter_data("user_role", "Воспитатель"))
@dc_change_keyboard(previous_name="call")
async def step_2_reaction(call: CallbackQuery, state: FSMContext):
    print(f"{call.from_user.id} - {call.from_user.full_name} - выбрал время vosp")
    await state.update_data(time=call.data)
    data = await state.get_data()
    res = check_on_exist(data)
    if res == None:
        await call.message.answer('Сколько человек (и 11 классников и 10 классников в сумме)', reply_markup=remove)
        await state.set_state(Form.num)
    else:
        await state.set_state("already exist")
        await call.message.answer(f'Эта запись уже существует : {res[0]}\nВы хотите её заменить?', reply_markup=yes_no_keyboard)
    await call.answer()


@router.message(StateFilter(Form.num), Filter_data("user_role", "Воспитатель"))
async def step_3_reaction(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - ввел количество vosp")
    data = await state.get_data()
    if len(message.text.split()) > 1:
        await state.set_state(Form.num)
        await message.answer("Некорректный  формат, пожалуйста введите ещё раз ОДНО число - общее количество питающихся", reply_markup=remove)
    elif len(message.text.split()) == 1:
        try:
            int(message.text)
            await state.update_data(num=message.text)
            data = await state.get_data()
            to_write(data)
            await state.set_state('chose')
            await message.answer("Успешно сохранено", reply_markup=kb5)
        except ValueError:
            await state.set_state(Form.num)
            await message.answer("Некорректный  формат, пожалуйста введите ещё раз одно ЧИСЛО - общее количество питающихся", reply_markup=remove)


@router.message(F.text == "Записать на ЭТУ ЖЕ дату", StateFilter("chose"), FilterId(ID_VOSP))
async def same_date_reaction_teacher(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - хочет записаться на ту же дату VOSP")
    await rewrite_state_data(state, "same")
    data = await state.get_data()
    kb = gen_keyboard_time_for_vosp(data)
    await state.update_data(last_kb=kb)
    await message.answer("Выберете время", reply_markup=kb)
    await state.set_state(Form.time)


@router.message(F.text == "Записать на ДРУГУЮ дату", StateFilter("chose"), FilterId(ID_VOSP))
async def other_date_reaction_teacher(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - хочет записаться на другую дату VOSP")
    await rewrite_state_data(state, "other")
    data = await state.get_data()
    kb = create_date_keyboard_for_vosp(data)
    await state.update_data(last_kb=kb)
    await message.answer('Выберете дату', reply_markup=kb)
    await state.set_state(Form.date)
