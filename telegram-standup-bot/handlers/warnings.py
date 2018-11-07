from aiogram import types


async def only_private_groups(msg: types.Message):
    return await msg.reply(
        "This command can be used"
        " only in private groups",
        reply=False
    )


async def only_non_private_groups(msg: types.Message):
    return await msg.reply(
        "This command can be used"
        " only in public groups",
        reply=False
    )

