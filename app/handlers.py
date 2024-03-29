from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import kb1, kb_time_for_teacher, kb_date_all,kb_date_for_teacher, kb4, remove,gen_keyboard_time_for_vosp
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.database.request import to_write,check_on_exist
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot
from app.users.filter_class import FilterId
from app.users.objects_class import read_list,write_list
from icecream import ic
from app.users.objects_class import find_user_name_by_id, find_user_role_by_id
from app.users.main_class import Form
from config import ADMIN



list_info = []

router = Router( )
########################## Админ панель ########################
@router.message(CommandStart(),FilterId(ADMIN))
async def admin_panel_reaction(message : Message):
    await message.answer('Админ панель', reply_markup=kb1)

@router.message(F.text == "Я старший воспитатель",FilterId(ADMIN))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all )
    
    await state.set_state("give_data")

@router.message(FilterId(ADMIN), F.text == "Я воспитатель" )
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state(Form.date)
    await state.update_data(user_name = 'ADMIN')
    await message.answer('Выберете дату',reply_markup=kb_date_all)





########################## Просмотр ########################
@router.message(CommandStart(),FilterId(read_list))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all )
    
    await state.set_state("give_data")

@router.message(StateFilter("give_data"))
async def state_give_data_reaction(message : Message, state : FSMContext):
    await state.clear()
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    if get_png(message_text) == "Error":
        await message.answer('Ошибка этой таблицы скорее всего пустая')
    else:
        photo = FSInputFile("table.png")
        await bot.send_photo(chat_id=message.chat.id,photo=photo)

########################## Запись ###############

@router.message(FilterId(write_list), F.text == "/start" )
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state(Form.date)
    await state.update_data(user_name = find_user_name_by_id(message.from_user.id),
                            user_role = find_user_role_by_id(message.from_user.id))
    data = await state.get_data()
    if data['user_role'] == 'Классный советник':
        await message.answer('Выберете дату',reply_markup=kb_date_for_teacher)
    elif data['user_role'] == 'Воспитатель':
        await message.answer('Выберете дату',reply_markup=kb_date_all)


@router.message(StateFilter('step 1'))
async def step_1_reaction(message : Message, state : FSMContext):
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    await state.update_data(date = message_text)
    data = await state.get_data()
    ic(data)
    if data['user_role'] == 'Классный советник': 
        await message.answer("Выберете время",reply_markup=kb_time_for_teacher) 
    elif data["user_role"] == 'Воспитатель':
        kb = gen_keyboard_time_for_vosp(data["date"])
        await message.answer("Выберете время",reply_markup=kb)
    await state.set_state(Form.time)


@router.message(StateFilter("step 2"))
async def step_2_reaction(message : Message, state : FSMContext):
    await state.update_data(time = message.text)
    res = check_on_exist(await state.get_data())
    if res == None: 
        await message.answer("Сколько человек (Напишите числом)",reply_markup=remove)
        await state.set_state("step 3")
    else:
        await state.set_state("step 2 / already exist")
        await message.answer(f'Эта запись уже существует "{res[0]}" \nВы хотите её заменить?',reply_markup=kb4)

@router.callback_query(F.data == "No")
async def call_back_data_reaction_No(call : CallbackQuery):
    global list_info
    await call.message.edit_text("Пожалуйста введите команду /start заново для записи")
    list_info = []
    await call.answer()


@router.callback_query(F.data == "Yes")
async def call_back_data_reaction_Yes(call : CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.answer()
    await call.message.answer("Сколько человек (Напишите числом)")
    await state.set_state("step 3")
        




@router.message(StateFilter('step 3'))
async def step_3_reaction(message : Message, state : FSMContext):
    global list_info
    await message.answer("Успешно сохранено")
    await state.clear()
    list_info.append(message.text)
    ic(list_info)
    to_write(list_info)
    
    list_info = [] 





    

