from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import gen_keyboard_time_for_teacher, create_date_keyboard_for_teacher, yes_no_keyboard, remove, kb_check_other_date, kb5
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from app.database.request import to_write, check_on_exist, get_data_for_docx
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot
from app.users.filter_class import FilterId, Filter_data
from app.users.objects_class import ID_TEACHER
from icecream import ic
from app.users.objects_class import find_user_name_by_id, find_user_classroom_number_by_id
from app.users.main_class import Form
from app.users.handlers.other import rewrite_state_data
from app.decorators import dc_change_keyboard


router = Router()


@router.message(FilterId(ID_TEACHER), CommandStart())
async def second_keyboard_reaction(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - начал запись teacher")
    await state.clear()

    await state.update_data(user_name=find_user_name_by_id(message.from_user.id),
                            user_role="Классный советник")
    data = await state.get_data()
    keyboard = create_date_keyboard_for_teacher(data)
    if keyboard:
        await state.update_data(last_kb=keyboard)
        await message.answer('Выберете дату', reply_markup=keyboard)
        await state.set_state(Form.date)
    else:
        await message.answer('Сегодня отсутствуют даты для записи')


@router.callback_query(StateFilter(Form.date), FilterId(ID_TEACHER))
@dc_change_keyboard(previous_name="call")
async def step_1_reaction(call: CallbackQuery, state: FSMContext):
    if call.data[0].isalpha():
        message_text = call.data.split()[1]
    else:
        message_text = call.data
    await state.update_data(date=message_text)
    data = await state.get_data()
    kb = gen_keyboard_time_for_teacher(data)
    await state.update_data(last_kb=kb)
    await call.message.answer("Выберете время", reply_markup=kb)
    # await send_time()
    await state.set_state(Form.time)
    await call.answer()


@router.callback_query(StateFilter(Form.time), Filter_data("user_role", "Классный советник"))
@dc_change_keyboard(previous_name="call")
async def step_2_reaction(call: CallbackQuery, state: FSMContext):
    await state.update_data(time=call.data)
    data = await state.get_data()
    res = check_on_exist(data)
    if res == None:
        if call.data == "Обед" or call.data == "Полдник":
            await call.message.answer('Сколько человек (количество городских, через пробел количество интернатных)', reply_markup=remove)
        else:
            await call.message.answer("Сколько человек (Напишите числом)", reply_markup=remove)
        await state.set_state(Form.num)
    else:
        await state.set_state("already exist")
        if data["time"] == "Завтрак":
            await call.message.answer(f'Эта запись уже существует "{res[0]}" \nВы хотите её заменить?', reply_markup=yes_no_keyboard)
        if data["time"] == "Полдник" or data["time"] == "Обед":
            await call.message.answer(f'Эта запись уже существует : \nгород : {res[0]}\nинтернат : {res[1]} \nВы хотите её заменить?', reply_markup=yes_no_keyboard)
    await call.answer()


@router.message(StateFilter(Form.num), Filter_data("user_role", "Классный советник"))
async def step_3_reaction(message: Message, state: FSMContext):
    old_data = await state.get_data()
    if old_data["time"] == "Обед" or old_data["time"] == "Полдник":
        try:
            if type(int(message.text.split()[0])) == int and type(int(message.text.split()[1])) == int:

                await state.update_data(num=message.text)
                data = await state.get_data()
                # ic(data)
                to_write(data)
                await state.set_state('chose Teacher')
                await message.answer("Успешно сохранено", reply_markup=kb5)
            else:
                await state.set_state(Form.num)
                await message.answer("Некорректный  формат, пожалуйста введите ещё раз два числа через пробел  в указанном формате", reply_markup=remove)
        except IndexError:
            await state.set_state(Form.num)
            await message.answer("Некорректный  формат, пожалуйста введите ещё раз ДВА числа через ПРОБЕЛ  в указанном формате", reply_markup=remove)
        except ValueError:
            await state.set_state(Form.num)
            await message.answer("Некорректный  формат, пожалуйста введите еще раз два ЧИСЛА через пробел  в указанном формате", reply_markup=remove)
    else:
        try:
            # проверяем это число или нет
            await state.update_data(num=str(int(message.text)))
            data = await state.get_data()
            to_write(data)
            await message.answer("Успешно сохранено", reply_markup=kb5)
            await state.set_state('chose Teacher')
        except ValueError:
            await message.answer("Некорректный  формат, пожалуйста введите еще раз ЧИСЛО")


@router.callback_query(F.data == "No", Filter_data("user_role", "Классный советник"))
async def call_back_data_reaction_No(call: CallbackQuery, state: FSMContext):
    print(f"{call.from_user.id} - {call.from_user.full_name} - отказался от записи teacher")
    await call.message.edit_text("Пожалуйста введите команду /start заново для записи")
    await state.clear()
    await call.answer()


@router.callback_query(F.data == "Yes", Filter_data("user_role", "Классный советник"))
async def call_back_data_reaction_Yes(call: CallbackQuery, state: FSMContext):
    print(f"{call.from_user.id} - {call.from_user.full_name} - согласился на запись teacher")
    await call.message.delete()
    await call.answer()
    data = await state.get_data()
    if data["time"] == "Завтрак":
        await call.message.answer("Сколько человек (Напишите числом)")
    elif data["time"] in ("Обед", "Полдник"):
        await call.message.answer('Сколько человек (количество городских, через пробел количество интернатных)')
    await state.set_state(Form.num)


@router.message(F.text == "Записать на ЭТУ ЖЕ дату", StateFilter("chose Teacher"))
async def same_date_reaction_teacher(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - хочет записаться на ту же дату teacher")
    await rewrite_state_data(state, "same")
    data = await state.get_data()
    kb = gen_keyboard_time_for_teacher(data)
    await state.update_data(last_kb=kb)
    await message.answer("Выберете время", reply_markup=kb)
    await state.set_state(Form.time)


@router.message(F.text == "Записать на ДРУГУЮ дату", StateFilter("chose Teacher"))
async def other_date_reaction_teacher(message: Message, state: FSMContext):
    print(f"{message.from_user.id} - {message.from_user.full_name} - хочет записаться на другую дату teacher")
    await rewrite_state_data(state, "other")
    data = await state.get_data()
    kb = create_date_keyboard_for_teacher(data)
    await state.update_data(last_kb=kb)
    await message.answer('Выберете дату', reply_markup=kb)
    await state.set_state(Form.date)
