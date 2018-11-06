import asyncio
import logging
from typing import Optional

from aiogram import types, Dispatcher
from aiogram.utils import executor

from .app import bot, dp
from .handlers.process_new_members import (
    new_member_welcome,
    add_me,
)
from .handlers.start_bot import start_bot, help_bot
from .handlers.user_report import (
    report_handler,
    process_today,
    process_yesterday,
    process_block,
    process_absences,
    process_thanks,
)
from .handlers.user_settings import (
    settings_handler,
    deactivate,
    activate,
)
from .structs import BotStates, User

__version__ = "0.0.1"

logger = logging.getLogger()


async def register_handlers():
    dp.register_message_handler(
        start_bot,
        commands=["start"],
        custom_filters=[types.ChatType.is_private],
    )
    dp.register_message_handler(
        start_bot,
        commands=["help"],
        custom_filters=[types.ChatType.is_private],
    )

    dp.register_message_handler(
        new_member_welcome,
        content_types=types.ContentType.NEW_CHAT_MEMBERS,
    )
    dp.register_callback_query_handler(
        add_me, func=lambda c: c.data == "add_me"
    )

    dp.register_message_handler(
        settings_handler,
        commands=["settings"],
        state=BotStates.STANDBY,
        custom_filters=[types.ChatType.is_private],
    )
    dp.register_callback_query_handler(
        deactivate,
        state=BotStates.STANDBY,
        func=lambda c: c.data == "deactivate",
    )
    dp.register_callback_query_handler(
        activate,
        state=BotStates.STANDBY,
        func=lambda c: c.data == "activate",
    )
    dp.register_message_handler(
        report_handler,
        state=BotStates.STANDBY,
        commands=["report"],
        custom_filters=[types.ChatType.is_private],
    )
    dp.register_message_handler(
        process_today, state=BotStates.TODAY
    )
    dp.register_message_handler(
        process_yesterday, state=BotStates.YESTERDAY
    )
    dp.register_message_handler(
        process_block, state=BotStates.BLOCK
    )
    dp.register_message_handler(
        process_absences, state=BotStates.ABSENCES
    )
    dp.register_message_handler(
        process_thanks, state=BotStates.THANKS
    )


async def send_reminders(user_id: int):
    while True:
        try:
            await bot.send_message(
                user_id,
                r"Hi! A friendly reminder to submit a report."
                r" Use `\report` command for this. If you want"
                r"to deactivate the reminder, go to `\settings`",
            )
        except asyncio.CancelledError:
            return
        else:
            await asyncio.sleep(1 * 24 * 3600)


async def user_participate_in_standup(
    standup_chat_id: int, user_id: int
) -> Optional[User]:
    users_data = await dp.storage.get_data(
        chat=standup_chat_id, user=user_id
    )
    if "attrs" in users_data:
        return users_data["attrs"]
    return None


async def reminders_manager():
    loop = asyncio.get_event_loop()
    while True:
        for (
            chat_id,
            users_data,
        ) in dp.storage.data.items():
            for user_id in users_data.keys():
                user = await user_participate_in_standup(
                    chat_id, user_id
                )
                if not user:
                    break
                if user.active and not user.task:
                    user.task = loop.create_task(
                        send_reminders(user_id)
                    )
                    logger.info(
                        f"user {user_id} were added to standup"
                    )
                if not user.active and user.task:
                    user.task.cancel()
                    user.task = None
                    logger.info(
                        f"user {user_id} were removed from standup"
                    )
        await asyncio.sleep(5)


async def on_startup(_):
    await register_handlers()
    loop = asyncio.get_event_loop()
    loop.create_task(reminders_manager())


async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await bot.close()
    await asyncio.sleep(0.250)


def initialize_bot():
    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
    )
