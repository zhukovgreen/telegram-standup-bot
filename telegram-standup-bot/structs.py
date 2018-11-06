import asyncio
from typing import Optional, Dict

import attr
from aiogram.utils.helper import (
    Helper,
    HelperMode,
    ListItem,
)


@attr.s(auto_attribs=True)
class User:
    active: bool = attr.ib(default=False)
    task: Optional[asyncio.Task] = attr.ib(
        default=None, repr=False
    )


class BotStates(Helper):
    mode = HelperMode.snake_case

    STANDBY = ListItem()
    FEEL = ListItem()
    YESTERDAY = ListItem()
    TODAY = ListItem()
    BLOCK = ListItem()
    ABSENCES = ListItem()
    THANKS = ListItem()
