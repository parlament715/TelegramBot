from functools import wraps
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from typing import List
from app.keyboard import take_changed_keyboard
from icecream import ic


def dc_change_keyboard(previous_name: str):
    def function2(func):
        @wraps(func)
        async def call_function1(call: CallbackQuery, state: FSMContext):
            data = await state.get_data()
            new_kb = None
            kb_text = None
            if "last_kb" in data.keys():
                if data["last_kb"] is None:
                    Exception("last_kb is none")
                old_kb = take_changed_keyboard(data["last_kb"], call.data)
                await call.message.edit_reply_markup(reply_markup=old_kb)
            res = await func(call, state)
            return res

        if previous_name == "call":
            return call_function1
        else:
            raise Exception("previous_name only call or message")
    return function2
