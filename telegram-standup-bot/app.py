import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import (
    MemoryStorage,
)
from envparse import env

__version__ = "0.0.1"

env.read_envfile()
BOT_TOKEN = env.str("BOT_TOKEN")
LOGGING_LEVEL = env(
    "LOGGING_LEVEL", postprocessor=str.upper
)

bot = Bot(token=BOT_TOKEN, parse_mode="markdown")
dp = Dispatcher(bot, storage=MemoryStorage())


def setup_logger():
    logging.basicConfig(
        format="%(asctime)s | "
        "%(name)s:%(lineno)d | "
        "%(levelname)s | %(message)s",
        level=LOGGING_LEVEL,
        stream=sys.stdout,
    )

    logging.getLogger("aiohttp").setLevel(
        logging.WARNING
    )
    logging.getLogger().setLevel(LOGGING_LEVEL)


setup_logger()
