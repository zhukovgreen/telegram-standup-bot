from aiogram import types

from ..app import dp
from ..handlers.utils import get_target_chat
from ..structs import User


async def settings_handler(msg: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        *[
            types.InlineKeyboardButton(
                "deactivate",
                callback_data="deactivate",
            ),
            types.InlineKeyboardButton(
                "activate", callback_data="activate"
            ),
        ]
    )

    await msg.reply(
        "Bot settings for daily reminders",
        reply_markup=markup,
        reply=False,
    )


async def deactivate(
    callback_query: types.CallbackQuery
):
    user = callback_query.from_user
    target_chat = await get_target_chat(user.id)
    users_data = await dp.storage.get_data(
        chat=target_chat, user=user.id
    )
    user_data: User = users_data["attrs"]
    user_data.active = False
    await callback_query.answer("Standup is on hold")


async def activate(
    callback_query: types.CallbackQuery
):
    user = callback_query.from_user
    target_chat = await get_target_chat(user.id)

    users_data = await dp.storage.get_data(
        chat=target_chat, user=user.id
    )
    user_data: User = users_data["attrs"]
    user_data.active = True
    await callback_query.answer("Standup is active")
