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
from app.users.objects_class import ID_MAIN_VOSP
from icecream import ic
from app.users.objects_class import find_user_name_by_id, find_user_classroom_number_by_id
from app.users.main_class import Form
from config import ADMIN

router = Router()


@router.message(CommandStart(), FilterId(ID_MAIN_VOSP))
async def first_keyboard_reaction(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all)

    await state.set_state("give_data")


@router.message(F.text == "Посмотреть другую дату", FilterId(ADMIN))
async def first_keyboard_reaction(message: Message, state: FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all)

    await state.set_state("give_data")


@router.message(F.text == "Посмотреть другую дату", FilterId(ID_MAIN_VOSP))
async def first_keyboard_reaction(message: Message, state: FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=kb_date_all)

    await state.set_state("give_data")


@router.message(StateFilter("give_data"))
async def state_give_data_reaction(message: Message, state: FSMContext):
    await state.clear()
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    list_png = get_png(message_text)
    res_docx = get_data_for_docx(message_text)
    file = FSInputFile("docx.docx")
    for path in list_png:
        if path == list_png[-1]:
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(path), reply_markup=kb_check_other_date)
        else:
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(path))
    if res_docx != "Error":
        await bot.send_document(chat_id=message.chat.id, document=file)
    else:
        await message.answer("Не получилось сформировать документ, недостаточно записей")
