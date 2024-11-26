from aiogram import BaseMiddleware
from aiogram import types
from typing import Callable, Dict, Any, Awaitable, Union
from config import time_from, time_to
from app.users.objects_class import ID_MAIN_VOSP, ID_TEACHER, ID_VOSP
from datetime import datetime
from loader import bot
from icecream import ic
from aiogram.utils.deep_linking import decode_payload


class CheckerSubscriptionsOnChannel(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if str(event.from_user.id) in ID_MAIN_VOSP:
            return await handler(event, data)
        elif str(event.from_user.id) in ID_TEACHER or str(event.from_user.id) in ID_VOSP:
            if time_from <= datetime.now().time() <= time_to:
                return await handler(event, data)


class CheckerOnCallbackData(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: types.TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if str(event.from_user.id) in ID_MAIN_VOSP:
            return await handler(event, data)
        elif str(event.from_user.id) in ID_TEACHER or str(event.from_user.id) in ID_VOSP:
            if time_from <= datetime.now().time() <= time_to:
                return await handler(event, data)
