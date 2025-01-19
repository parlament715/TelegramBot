from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.users.filter_class import FilterId
from icecream import ic
from app.users.objects_class import ID_TEACHER, ID_VOSP, ID_MAIN_VOSP

router = Router()


# ##################### /help ################
# @router.message(F.text == "/help", FilterId(ID_TEACHER + ID_VOSP))
# async def help_reaction_for_read(message: Message):
#     await message.answer(
#         'Для того чтобы посмотреть данные введите /start далее следуйте инструкциям. На этапе выбора даты можете ввести свою дату так и выбрать вариант из предложенных, в случае отсутствия записи вы получи сообщение : "Ошибка, этой таблицы скорее всего пустая". После каждого просмотра придётся вводить команду /start заново. Если возникли трудности обращайтесь в лс @paralment'
#     )


# @router.message(F.text == "/help", FilterId(ID_MAIN_VOSP))
# async def help_reaction_for_read(message: Message):
#     await message.answer(
#         'Для того чтобы занести данные вам нужно написать команду /start далее следовать согласно инструкциям, после каждой записи нужно заново прописывать команду /start'
#     )


############################ router #####################
async def rewrite_state_data(state: FSMContext, param: str):
    data = await state.get_data()
    date = data["date"]
    user_name = data["user_name"]
    user_role = data["user_role"]
    await state.clear()
    await state.update_data(user_name=user_name, user_role=user_role)
    if param == "same":
        await state.update_data(date=date)
