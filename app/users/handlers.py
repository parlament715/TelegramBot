from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import kb1, kb_time_for_teacher, kb_date_all,kb_date_for_teacher, kb4, remove,gen_keyboard_time_for_vosp, kb_check_other_date
from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from app.database.request import to_write,check_on_exist
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot
from app.users.filter_class import FilterId,Filter_data
from app.users.objects_class import read_list,write_list
from icecream import ic
from app.users.objects_class import find_user_name_by_id, find_user_role_by_id, find_user_classroom_number_by_id
from app.users.main_class import Form
from config import ADMIN

router = Router()






########################## Админ панель ########################
@router.message(CommandStart(),FilterId(ADMIN))
async def admin_panel_reaction(message : Message):
    await message.answer('Админ панель', reply_markup=kb1)

@router.message(F.text == "Я старший воспитатель",FilterId(ADMIN))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all )
    
    await state.set_state("give_data")


@router.message(FilterId(ADMIN),F.text == "Я воспитатель")
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state(Form.date)
    await state.update_data(user_name = "ADMIN",
                            user_role = "Воспитатель")
    await message.answer('Выберете дату',reply_markup=kb_date_all)


@router.message(FilterId(ADMIN),F.text == "Я классный советник")
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state(Form.date)
    await state.update_data(user_name = "ADMIN",
                            user_role = "Классный советник")
    await message.answer('Выберете дату',reply_markup=kb_date_for_teacher)





########################## Просмотр ########################
@router.message(CommandStart(),FilterId(read_list))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all )
    
    await state.set_state("give_data")

@router.message(F.text == "Посмотреть другую дату",FilterId(ADMIN))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all )
    
    await state.set_state("give_data")

@router.message(F.text == "Посмотреть другую дату",FilterId(read_list))
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
        await message.answer('Ошибка, этой таблицы скорее всего пустая', reply_markup=kb_check_other_date)
    else:
        photo = FSInputFile("table.png")
        await bot.send_photo(chat_id=message.chat.id,photo=photo,reply_markup=kb_check_other_date)

########################## Запись ###############

@router.message(FilterId(write_list),CommandStart())
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state(Form.date)
    await state.update_data(user_name = find_user_name_by_id(message.from_user.id),
                            user_role = find_user_role_by_id(message.from_user.id))
    data = await state.get_data()
    if data['user_role'] == 'Классный советник':
        await message.answer('Выберете дату',reply_markup=kb_date_for_teacher)
    elif data['user_role'] == 'Воспитатель':
        await message.answer('Выберете дату',reply_markup=kb_date_all)
      

@router.callback_query(F.data == "No")
async def call_back_data_reaction_No(call : CallbackQuery, state : FSMContext):
    await call.message.edit_text("Пожалуйста введите команду /start заново для записи")
    await state.clear()
    await call.answer()


@router.callback_query(F.data == "Yes")
async def call_back_data_reaction_Yes(call : CallbackQuery, state : FSMContext):
    await call.message.delete()
    await call.answer()
    data = await state.get_data()
    if data["user_role"] == "Классный советник":
        await call.message.answer("Сколько человек (Напишите числом)")
    elif data["user_role"] == "Воспитатель":
        await call.message.answer('Сколько человек (количество 11-классников, через пробел количество 10-классников)')
    await state.set_state(Form.num)



########################### Воспитатель ########################
@router.message(StateFilter(Form.date),Filter_data("user_role","Воспитатель"))
async def step_1_reaction(message : Message, state : FSMContext):
  if message.text[0].isalpha():
      message_text = message.text.split()[1]
  else:
      message_text = message.text
  await state.update_data(date = message_text)
  data = await state.get_data()
  ic(data)
  kb = gen_keyboard_time_for_vosp(data["date"])
  await message.answer("Выберете время",reply_markup=kb)
  # await send_time() 
  await state.set_state(Form.time)

@router.message(StateFilter(Form.time),Filter_data("user_role","Воспитатель"))
async def step_2_reaction(message : Message, state : FSMContext):
    await state.update_data(time = message.text)
    data = await state.get_data()
    res = check_on_exist(data)
    if res == None: 
        await message.answer('Сколько человек (количество 11-классников, через пробел количество 10-классников)',reply_markup=remove)
        await state.set_state(Form.num)
    else:
        await state.set_state("already exist")
        await message.answer(f'Эта запись уже существует "{res[0]}" \nВы хотите её заменить?',reply_markup=kb4)

@router.message(StateFilter(Form.num),Filter_data("user_role","Воспитатель"))
async def step_3_reaction(message : Message, state : FSMContext):
    ic (message.text)
    data = await state.get_data()
    try:
      if type(int(message.text.split()[0])) == int and type(int(message.text.split()[1])) == int:
        await message.answer("Успешно сохранено")
        await state.update_data(num = message.text)
        ic(await state.get_data())
        to_write(await state.get_data())
        await state.clear()
      else:
          await state.set_state(Form.num) 
          await message.answer("Некорректный  формат, пожалуйста введите числа через пробел  в указанном формате",reply_markup=remove)
    except IndexError:
        await state.set_state(Form.num)
        await message.answer("Некорректный  формат, пожалуйста введите ДВА числа через ПРОБЕЛ  в указанном формате",reply_markup=remove)
    except ValueError:
        await state.set_state(Form.num) 
        await message.answer("Некорректный  формат, пожалуйста введите два ЧИСЛА через пробел  в указанном формате",reply_markup=remove)
    # await state.set_state(Form.time)
    # await send_time()

###################### Классный советник ##############################
@router.message(StateFilter(Form.date),Filter_data("user_role","Классный советник"))
async def step_1_reaction(message : Message, state : FSMContext):
    
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    await state.update_data(date = message_text,
                            classroom_number = find_user_classroom_number_by_id(message.from_user.id))
    data = await state.get_data()
    ic(data)
    await message.answer("Выберете время",reply_markup=kb_time_for_teacher) 
    # await send_time() 
    await state.set_state(Form.time)


@router.message(StateFilter(Form.time),Filter_data("user_role","Классный советник"))
async def step_2_reaction(message : Message, state : FSMContext):
    await state.update_data(time = message.text)
    data = await state.get_data()
    res = check_on_exist(data)
    if res == None: 
        await message.answer("Сколько человек (Напишите числом)",reply_markup=remove)
        await state.set_state(Form.num)
    else:
        await state.set_state("already exist")
        await message.answer(f'Эта запись уже существует "{res[0]}" \nВы хотите её заменить?',reply_markup=kb4)


        
    

@router.message(StateFilter(Form.num),Filter_data("user_role","Классный советник"))
async def step_3_reaction(message : Message, state : FSMContext):
    await message.answer("Успешно сохранено")
    data = await state.get_data()
    if data["classroom_number"] == '10':
        await state.update_data(num = f'0 {message.text}')
    elif data["classroom_number"] == '11':
        await state.update_data(num = f'{message.text} 0')
    ic(await state.get_data())
    to_write(await state.get_data())
    await state.clear()
    # await state.set_state(Form.time)
    # await send_time()


##################### /help ################
@router.message(F.text == "/help",FilterId(read_list))
async def help_reaction_for_read(message : Message):
    await message.answer(
    'Для того чтобы посмотреть данные введите /start далее следуйте инструкциям. На этапе выбора даты можете ввести свою дату так и выбрать вариант из предложенных, в случае отсутствия записи вы получи сообщение : "Ошибка, этой таблицы скорее всего пустая". После каждого просмотра придётся вводить команду /start заново. Если возникли трудности обращайтесь в лс @paralment'
                         )
@router.message(F.text == "/help",FilterId(write_list))
async def help_reaction_for_read(message : Message):
    await message.answer(
    'Для того чтобы занести данные вам нужно написать команду /start далее следовать согласно инструкциям, после каждой записи нужно заново прописывать команду /start'
                         )


# async def send_time(message : Message, state : FSMContext):
#     data = await state.get_data()
#     ic(data)
#     if data['user_role'] == 'Классный советник': 
#         await message.answer("Выберете время",reply_markup=kb_time_for_teacher) 
#     elif data["user_role"] == 'Воспитатель':
#         kb = gen_keyboard_time_for_vosp(data["date"])
#         await message.answer("Выберете время",reply_markup=kb)


    

