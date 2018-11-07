from aiogram import types

from ..app import dp
from ..structs import User, BotStates


async def add_me(msg: types.Message):

    bot = msg.bot
    chat = msg.chat
    user_data: dict = await dp.storage.get_data(
        chat=chat.id, user=msg.from_user.id
    )
    user = user_data["attrs"] = User()
    user.active = True

    state = dp.current_state(
        user=msg.from_user.id, chat=msg.from_user.id
    )
    await state.set_state(BotStates.STANDBY[0])

    await bot.send_message(
        msg.from_user.id,
        r"You were added to the standup! Use `/report` command to start "
        r"the standup",
    )


async def remove_me(msg: types.Message):

    bot = msg.bot
    chat = msg.chat
    user_data: dict = await dp.storage.get_data(
        chat=chat.id, user=msg.from_user.id
    )
    user: User = user_data["attrs"]
    user.active = False
    if user.task:
        user.task.cancel()
    await dp.storage.reset_data(
        chat=chat.id, user=msg.from_user.id
    )
    state = dp.current_state(
        user=msg.from_user.id, chat=msg.from_user.id
    )
    await state.reset_state()

    await bot.send_message(
        msg.from_user.id,
        r"You were removed from the standup! "
        r"Use `/add_me` command to add you back ",
    )


async def new_member_welcome(msg: types.Message):
    user = msg.from_user

    await msg.reply(
        f"Hi, {user.first_name}!\n\n"
        f"I am TBE standup bot\n"
        f"If you want me to add you to the"
        f" standup then type `/add_me` command",
        reply=False,
    )
