from aiogram import types

from ..app import dp
from ..structs import BotStates
from ..utils import cancel_task


async def add_me(msg: types.Message):

    bot = msg.bot
    chat = msg.chat
    await dp.storage.set_data(
        chat=chat.id,
        user=msg.from_user.id,
        data={"active": True, "task_id": None},
    )

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
    if user_data["task_id"]:
        await cancel_task(user_data["task_id"])

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
