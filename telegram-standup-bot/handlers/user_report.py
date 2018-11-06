from aiogram import types

from .utils import get_target_chat, convert_to_report
from ..app import dp
from ..structs import BotStates



async def report_handler(msg: types.Message):
    user = msg.from_user
    state = dp.current_state(user=user.id)

    user_data = await dp.storage.get_data(
        user=user.id
    )
    user_data[
        "Report from"
    ] = f"{user.full_name} - @{user.username}"

    await msg.reply(
        "How do you feel today?", reply=False
    )
    await state.set_state(state=BotStates.TODAY[0])


async def process_today(msg: types.Message):
    user = msg.from_user
    state = dp.current_state(user=user.id)

    user_data = await dp.storage.get_data(
        user=user.id
    )
    user_data[BotStates.TODAY[0]] = msg.md_text

    await msg.reply(
        "What have you done yesturday?", reply=False
    )
    await state.set_state(
        state=BotStates.YESTERDAY[0]
    )


async def process_yesterday(msg: types.Message):
    user = msg.from_user
    state = dp.current_state(user=user.id)

    user_data = await dp.storage.get_data(
        user=user.id
    )
    user_data[BotStates.YESTERDAY[0]] = msg.md_text

    await msg.reply(
        "What will you do today?", reply=False
    )
    await state.set_state(state=BotStates.BLOCK[0])


async def process_block(msg: types.Message):
    user = msg.from_user
    state = dp.current_state(user=user.id)
    user_data = await dp.storage.get_data(
        user=user.id
    )
    user_data[BotStates.BLOCK[0]] = msg.md_text

    await msg.reply(
        "Anything blocks your progress?", reply=False
    )
    await state.set_state(state=BotStates.ABSENCES[0])


async def process_absences(msg: types.Message):
    user = msg.from_user
    state = dp.current_state(user=user.id)

    user_data = await dp.storage.get_data(
        user=user.id
    )
    user_data[BotStates.ABSENCES[0]] = msg.md_text

    await msg.reply(
        "Any absences in near future?", reply=False
    )
    await state.set_state(state=BotStates.THANKS[0])


async def process_thanks(msg: types.Message):
    bot = msg.bot
    user = msg.from_user
    state = dp.current_state(user=user.id)

    user_data = await dp.storage.get_data(
        user=user.id
    )

    target_chat = await get_target_chat(user.id)
    await bot.send_message(
        target_chat, convert_to_report(user_data)
    )
    await msg.reply(
        f"Thank you for your time, {user.first_name}",
        reply=False,
    )
    await dp.storage.reset_data(user=user)
    await state.set_state(BotStates.STANDBY[0])
