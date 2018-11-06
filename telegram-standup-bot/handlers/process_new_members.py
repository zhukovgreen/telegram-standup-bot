from aiogram import types

from ..app import dp
from ..structs import User, BotStates
from .utils import get_target_chat


async def add_me(callback_query: types.CallbackQuery):

    user = callback_query.from_user
    bot = callback_query.bot
    target_chat = await get_target_chat(user.id)
    users_data = await dp.storage.get_data(
        chat=target_chat, user=user.id
    )
    user_data: User = users_data["attrs"]
    user_data.active = True

    state = dp.current_state(user=user.id)
    await state.set_state(BotStates.STANDBY[0])

    await bot.send_message(
        user.id,
        r"Added! Use `/report` command to start "
        r"the standup",
    )


async def new_member_welcome(msg: types.Message):
    user = msg.from_user
    chat = msg.chat
    bot = msg.bot

    markup = types.InlineKeyboardMarkup()
    markup.insert(
        types.InlineKeyboardButton(
            "Add me", callback_data="add_me"
        )
    )

    standup_user_data = await dp.storage.get_data(
        chat=chat.id, user=user.id
    )
    standup_user_data["attrs"] = User()

    await bot.send_message(
        user.id,
        f"Hi, {user.first_name}!\n\n"
        f"I am TBE standup bot\n"
        f"Do you want me to add you to the team standup?",
        reply_markup=markup,
    )
