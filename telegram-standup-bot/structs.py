from aiogram.utils.helper import (
    Helper,
    HelperMode,
    ListItem,
)


class BotStates(Helper):
    mode = HelperMode.snake_case

    STANDBY = ListItem()
    FEEL = ListItem()
    YESTERDAY = ListItem()
    TODAY = ListItem()
    BLOCK = ListItem()
    ABSENCES = ListItem()
