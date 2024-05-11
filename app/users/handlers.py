from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import kb1, kb_time_for_teacher, kb_date_all,kb_date_for_teacher, kb4, remove,gen_keyboard_time_for_vosp, kb_check_other_date,kb5,kb6
from aiogram import F,Router
from aiogram.fsm.context import FSMContext
from app.database.request import to_write,check_on_exist,get_data_for_docx
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
async def admin_panel_reaction(message : Message,state : FSMContext):
    await message.answer('Админ панель', reply_markup=kb1)

@router.message(F.text == "Я старший воспитатель",FilterId(ADMIN))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all )
    
    await state.set_state("give_data")


@router.message(FilterId(ADMIN),F.text == "Я воспитатель")
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state("промежуточный выбор имени")
    await state.update_data(user_role = "Воспитатель")
    
    await message.answer('Введите имя',reply_markup=remove)

@router.message(FilterId(ADMIN),F.text == "Я классный советник")
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.set_state("промежуточный выбор номера класса")
    await state.update_data(user_role = "Классный советник")
    await message.answer("Выберете класс",reply_markup=kb6)

@router.message(StateFilter("промежуточный выбор номера класса"))
async def select_num_class(message: Message,state: FSMContext):
    if message.text == "10":
        await state.set_state("промежуточный выбор имени")
        await state.update_data(classroom_number = 10)
        await message.answer('Введите имя',reply_markup=remove)
    elif message.text == "11":
        await state.set_state("промежуточный выбор имени")
        await state.update_data(classroom_number = 11)
        await message.answer('Введите имя',reply_markup=remove)

@router.message(StateFilter("промежуточный выбор имени"))
async def select_name(message : Message, state : FSMContext):
    await state.update_data(user_name = message.text)
    await state.set_state(Form.date)
    data = await state.get_data()
    if data["user_role"] == "Классный советник":
        await message.answer('Выберете дату',reply_markup=kb_date_for_teacher)
    elif data["user_role"] == "Воспитатель":
        await message.answer('Выберете дату',reply_markup=kb_date_all)








########################## Просмотр ########################
@router.message(CommandStart(),FilterId(read_list))
async def first_keyboard_reaction(message : Message, state : FSMContext):
    await state.clear()
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
    get_data_for_docx(message_text)
    if get_png(message_text) == "Error":
        await message.answer('Ошибка, этой таблицы скорее всего пустая или недостаточно заполнена', reply_markup=kb_check_other_date)
    else:
        png_class_10 = FSInputFile("table_class_10.png")
        png_class_11 = FSInputFile("table_class_11.png")
        png_dorm = FSInputFile("table_dorm.png")
        file = FSInputFile("docx.docx")
        await bot.send_photo(chat_id=message.chat.id,photo=png_class_10)
        await bot.send_photo(chat_id=message.chat.id,photo=png_class_11)
        await bot.send_photo(chat_id=message.chat.id,photo=png_dorm,reply_markup=kb_check_other_date)
        await bot.send_document(chat_id=message.chat.id,document=file)

########################## Запись ###############

@router.message(FilterId(write_list),CommandStart())
async def second_keyboard_reaction(message : Message, state : FSMContext):
    await state.clear()
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
        if data["time"] == "Завтрак":
            await call.message.answer("Сколько человек (Напишите числом)")
        elif data["time"] in ("Обед","Полдник"):
            await call.message.answer('Сколько человек (количество городских, через пробел количество интернатных)')
    elif data["user_role"] == "Воспитатель":
        await call.message.answer('Сколько человек (количество 11-классников, через пробел количество 10-классников)')
    await state.set_state(Form.num)

@router.message(F.text == "Записать на ЭТУ ЖЕ дату",StateFilter("chose"))
async def same_date_reaction_teacher(message : Message, state : FSMContext):
    await rewrite_state_data(state,"same")
    data = await state.get_data()
    if data["user_role"] == "Воспитатель":
        kb = gen_keyboard_time_for_vosp(data["date"])
    elif data["user_role"] == "Классный советник":
        kb = kb_time_for_teacher
    await message.answer("Выберете время",reply_markup=kb)
    await state.set_state(Form.time)

@router.message(F.text == "Записать на ДРУГУЮ дату",StateFilter("chose"))
async def other_date_reaction_teacher(message : Message, state : FSMContext):
    await rewrite_state_data(state,"other")
    data = await state.get_data()
    if data['user_role'] == 'Классный советник':
        await message.answer('Выберете дату',reply_markup=kb_date_for_teacher)
    elif data['user_role'] == 'Воспитатель':
        await message.answer('Выберете дату',reply_markup=kb_date_all)
    await state.set_state(Form.date)

########################### Воспитатель ########################
@router.message(StateFilter(Form.date),Filter_data("user_role","Воспитатель"))
async def step_1_reaction(message : Message, state : FSMContext):
  if message.text[0].isalpha():
      message_text = message.text.split()[1]
  else:
      message_text = message.text
  await state.update_data(date = message_text)
  data = await state.get_data()
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
        await message.answer(f'Эта запись уже существует : \n11 класс : {res[0]}\n10 класс : {res[1]} \nВы хотите её заменить?',reply_markup=kb4)
 
            

@router.message(StateFilter(Form.num),Filter_data("user_role","Воспитатель"))
async def step_3_reaction(message : Message, state : FSMContext):
    data = await state.get_data()
    try:
      if type(int(message.text.split()[0])) == int and type(int(message.text.split()[1])) == int:
        await message.answer("Успешно сохранено",reply_markup=kb5)
        await state.update_data(num = message.text)
        data = await state.get_data()
        ic(data)
        to_write(data)
        await state.set_state('chose')
      else:
          await state.set_state(Form.num) 
          await message.answer("Некорректный  формат, пожалуйста введите ещё раз два числа через пробел  в указанном формате",reply_markup=remove)
    except IndexError:
        await state.set_state(Form.num)
        await message.answer("Некорректный  формат, пожалуйста введите ещё раз ДВА числа через ПРОБЕЛ  в указанном формате",reply_markup=remove)
    except ValueError:
        await state.set_state(Form.num) 
        await message.answer("Некорректный  формат, пожалуйста введите еще раз два ЧИСЛА через пробел  в указанном формате",reply_markup=remove)

@router.message(F.text == "Записать на эту же дату",StateFilter("chose_vosp"))
async def same_date_reaction_vosp(message : Message, state : FSMContext):
    await rewrite_state_data(state,"same")
    data = await state.get_data()
    kb = gen_keyboard_time_for_vosp(data["date"])
    await message.answer("Выберете время",reply_markup=kb)
    await state.set_state(Form.time)

@router.message(F.text == "Записать на другую дату",StateFilter("chose_vosp"))
async def other_date_reaction_vosp(message : Message, state : FSMContext):
    await rewrite_state_data(state,"other")
    data = await state.get_data()
    if data['user_role'] == 'Классный советник':
        await message.answer('Выберете дату',reply_markup=kb_date_for_teacher)
    elif data['user_role'] == 'Воспитатель':
        await message.answer('Выберете дату',reply_markup=kb_date_all)
    await state.set_state(Form.date)
    

###################### Классный советник ##############################
@router.message(StateFilter(Form.date),Filter_data("user_role","Классный советник"))
async def step_1_reaction(message : Message, state : FSMContext):
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    await state.update_data(date = message_text)
    data = await state.get_data()
    if "classroom_number" not in data.keys():
        await state.update_data(classroom_number = find_user_classroom_number_by_id(message.from_user.id))
    await message.answer("Выберете время",reply_markup=kb_time_for_teacher) 
    # await send_time() 
    await state.set_state(Form.time)


@router.message(StateFilter(Form.time),Filter_data("user_role","Классный советник"))
async def step_2_reaction(message : Message, state : FSMContext):
    await state.update_data(time = message.text)
    data = await state.get_data()
    res = check_on_exist(data)
    if res == None:
        if message.text == "Обед" or message.text == "Полдник":
            await message.answer('Сколько человек (количество городских, через пробел количество интернатных)',reply_markup=remove)
        else:
            await message.answer("Сколько человек (Напишите числом)",reply_markup=remove)
        await state.set_state(Form.num)
    else:
        await state.set_state("already exist")
        if data["time"] == "Завтрак":
            await message.answer(f'Эта запись уже существует "{res[0]}" \nВы хотите её заменить?',reply_markup=kb4)    
        if data["time"] == "Полдник" or data["time"] == "Обед":
            await message.answer(f'Эта запись уже существует : \nгород : {res[0]}\nинтернат : {res[1]} \nВы хотите её заменить?',reply_markup=kb4)
        



        
    

@router.message(StateFilter(Form.num),Filter_data("user_role","Классный советник"))
async def step_3_reaction(message : Message, state : FSMContext):
    old_data = await state.get_data()
    if old_data["time"] == "Обед" or old_data["time"] == "Полдник":
        try:
            if type(int(message.text.split()[0])) == int and type(int(message.text.split()[1])) == int:
                
                await state.update_data(num = message.text)
                data = await state.get_data()
                # ic(data)
                to_write(data)
                await state.set_state('chose')
                await message.answer("Успешно сохранено",reply_markup=kb5)
            else:
                await state.set_state(Form.num) 
                await message.answer("Некорректный  формат, пожалуйста введите ещё раз два числа через пробел  в указанном формате",reply_markup=remove)
        except IndexError:
            await state.set_state(Form.num)
            await message.answer("Некорректный  формат, пожалуйста введите ещё раз ДВА числа через ПРОБЕЛ  в указанном формате",reply_markup=remove)
        except ValueError:
            await state.set_state(Form.num) 
            await message.answer("Некорректный  формат, пожалуйста введите еще раз два ЧИСЛА через пробел  в указанном формате",reply_markup=remove)
    else:
        try:
            await state.update_data(num = str(int(message.text))) ### проверяем это число или нет
            data = await state.get_data()
            to_write(data)
            await message.answer("Успешно сохранено",reply_markup=kb5)
            await state.set_state('chose')    
        except ValueError:
            await message.answer("Некорректный  формат, пожалуйста введите еще раз ЧИСЛО")


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


############################ other #####################
async def rewrite_state_data(state : FSMContext,param : str):
    data = await state.get_data()
    date = data["date"]
    user_name = data["user_name"]
    user_role = data["user_role"]
    if data["user_role"] == "Классный советник":
        classroom_number = data["classroom_number"]
    await state.clear()
    if data["user_role"] == "Классный советник":
        await state.update_data(user_name = user_name, classroom_number = classroom_number, user_role = user_role)
    elif data["user_role"] == "Воспитатель":
        await state.update_data(user_name = user_name, user_role = user_role)
    if param == "same":
        await state.update_data(date = date)




    

