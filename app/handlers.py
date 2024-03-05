from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import kb1, kb2, kb3, remove
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.database.request import to_write
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot
from app.users.filter_class import FilterId
from app.users.objects_class import read_list,write_list
from icecream import ic
from app.users.objects_class import find_user_name_by_id
from config import ADMIN



list_info = []

router = Router( )
########################## Админ панель ########################
@router.message(CommandStart(),FilterId(ADMIN))
async def admin_panel_reaction(message : Message):
    await message.answer('Админ панель', reply_markup=kb1)

@router.message(F.text == "Я старший воспитатель",FilterId(ADMIN))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb2 )
    
    await state.set_state("give_data")

@router.message(FilterId(ADMIN), F.text == "Я воспитатель" )
async def second_keyboard_reaction(message : Message, state : FSMContext):
    global list_info
    
    await state.set_state('step 1')
    ic(message.from_user.id)
    ic(find_user_name_by_id(str(message.from_user.id)))
    list_info.append(find_user_name_by_id(message.from_user.id))
    await message.answer('Выберете дату',reply_markup=kb2)





########################## Просмотр ########################
@router.message(CommandStart(),FilterId(read_list))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb2 )
    
    await state.set_state("give_data")

@router.message(StateFilter("give_data"))
async def state_give_data_reaction(message : Message, state : FSMContext):
    await state.clear()
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    get_png(message_text)
    photo = FSInputFile("table.png")

    await bot.send_photo(chat_id=message.chat.id,photo=photo)

########################## Запись ###############

@router.message(FilterId(write_list), F.text == "/start" )
async def second_keyboard_reaction(message : Message, state : FSMContext):
    global list_info
    
    await state.set_state('step 1')
    ic(message.from_user.id)
    ic(find_user_name_by_id(str(message.from_user.id)))
    list_info.append(find_user_name_by_id(message.from_user.id))
    await message.answer('Выберете дату',reply_markup=kb2)


@router.message(StateFilter('step 1'))
async def step_1_reaction(message : Message, state : FSMContext):
    await message.answer("Выберете время",reply_markup=kb3)
    list_info.append(message.text)
    await state.clear()
    await state.set_state("step 2")

@router.message(StateFilter("step 2"))
async def step_2_reaction(message : Message, state : FSMContext):
    await message.answer("Сколько человек (Напишите числом)",reply_markup=remove)
    list_info.append(message.text)
    await state.clear()
    await state.set_state("step 3")


@router.message(StateFilter('step 3'))
async def step_3_reaction(message : Message, state : FSMContext):
    global list_info
    await message.answer("Успешно сохранено")
    await state.clear()
    list_info.append(message.text)
    to_write(list_info)
    list_info = [] 





    

