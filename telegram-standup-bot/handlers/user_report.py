from aiogram import types

from .utils import (
    get_target_chat,
    convert_to_str_report,
)
from ..app import dp
from ..structs import BotStates


async def stop_report(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    state.set_state(BotStates.STANDBY[0])
    await msg.reply("Report skipped!")


async def report_handler(msg: types.Message):
    user = msg.from_user
    state = dp.current_state(user=user.id)

    await dp.storage.set_data(
        user=user.id,
        data={
            "Report by": f"{user.full_name} - @{user.username}"
        },
    )

    await msg.reply(
        "How do you feel today?", reply=False
    )
    await state.set_state(state=BotStates.FEEL[0])


async def process_feel(msg: types.Message):
    user = msg.from_user

    await dp.storage.update_data(
        user=user.id,
        data={BotStates.FEEL[0]: msg.md_text},
    )

    await msg.reply(
        "What have you done yesterday?", reply=False
    )

    state = dp.current_state(user=user.id)
    await state.set_state(
        state=BotStates.YESTERDAY[0]
    )


async def process_yesterday(msg: types.message):
    user = msg.from_user

    await dp.storage.update_data(
        user=user.id,
        data={BotStates.YESTERDAY[0]: msg.md_text},
    )

    await msg.reply(
        "What will you do today?", reply=False
    )

    state = dp.current_state(user=user.id)
    await state.set_state(state=BotStates.TODAY[0])


async def process_today(msg: types.message):
    user = msg.from_user

    await dp.storage.update_data(
        user=user.id,
        data={BotStates.TODAY[0]: msg.md_text},
    )

    await msg.reply(
        "What blocks your progress?", reply=False
    )

    state = dp.current_state(user=user.id)
    await state.set_state(state=BotStates.BLOCK[0])


async def process_block(msg: types.Message):
    user = msg.from_user

    await dp.storage.update_data(
        user=user.id,
        data={BotStates.BLOCK[0]: msg.md_text},
    )

    await msg.reply(
        "Any absences in the nearby future?",
        reply=False,
    )

    state = dp.current_state(user=user.id)
    await state.set_state(state=BotStates.ABSENCES[0])


async def process_absences(msg: types.Message):
    user = msg.from_user
    bot = msg.bot

    await dp.storage.update_data(
        user=user.id,
        data={BotStates.ABSENCES[0]: msg.md_text},
    )

    report: dict = await dp.storage.get_data(
        user=user.id
    )
    target_chat = await get_target_chat(user.id)
    await bot.send_message(
        target_chat, convert_to_str_report(report)
    )

    await dp.storage.reset_data(user=user.id)

    state = dp.current_state(user=user.id)
    await state.set_state(BotStates.STANDBY[0])

    await msg.reply(
        f"Thank you for your time, {user.first_name}",
        reply=False,
    )
