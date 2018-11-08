import logging
import sys
import yarl

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import (
    MemoryStorage,
)
from aiogram.contrib.fsm_storage.redis import (
    RedisStorage2,
)
from envparse import env

__version__ = "0.0.1"

env.read_envfile()
BOT_TOKEN = env.str("BOT_TOKEN")
LOGGING_LEVEL = env(
    "LOGGING_LEVEL", postprocessor=str.upper
)

MEMORY_TYPE = env.str("MEMORY_TYPE")
REDIS_URL = yarl.URL(env.str("CACHE"))

storage = (
    MemoryStorage()
    if MEMORY_TYPE == "in_memory"
    else RedisStorage2(
        REDIS_URL.host,
        REDIS_URL.port,
        db=int(REDIS_URL.path[1:]),
    )
)
bot = Bot(token=BOT_TOKEN, parse_mode="markdown")
dp = Dispatcher(bot, storage=storage)


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
