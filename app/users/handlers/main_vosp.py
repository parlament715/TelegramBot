from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from app.keyboard import create_main_vosp_date_keyboard, kb_check_other_date
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from app.database.table import get_png
from aiogram.types import FSInputFile
from loader import bot, rq
from app.users.filter_class import FilterId
from app.users.objects_class import ID_MAIN_VOSP
from icecream import ic
from app.users.main_class import Form

router = Router()


@router.message(CommandStart(), FilterId(ID_MAIN_VOSP))
async def first_keyboard_reaction(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=create_main_vosp_date_keyboard())

    await state.set_state("give_data")


@router.message(F.text == "Посмотреть другую дату", FilterId(ID_MAIN_VOSP))
async def first_keyboard_reaction(message: Message, state: FSMContext):
    await message.answer('Для просмотра данных нажмите на предложенные варианты или введите их самостоятельно в таком формате : год-месяц-число.', reply_markup=create_main_vosp_date_keyboard())

    await state.set_state("give_data")


@router.message(StateFilter("give_data"), FilterId(ID_MAIN_VOSP))
async def state_give_data_reaction(message: Message, state: FSMContext):
    await state.clear()
    if message.text[0].isalpha():
        message_text = message.text.split()[1]
    else:
        message_text = message.text
    list_png = get_png(message_text)
    with rq:
        res_docx = rq.get_data_for_docx(message_text)
    file = FSInputFile("docx.docx", f"Приказ от {message_text}.docx")
    for path in list_png:
        if path == list_png[-1]:
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(path), reply_markup=kb_check_other_date)
        else:
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(path))
    if res_docx != "Error":
        await bot.send_document(chat_id=message.chat.id, document=file)
    else:
        await message.answer("Не получилось сформировать документ, недостаточно записей")
