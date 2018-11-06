from aiogram import types


async def start_bot(msg: types.Message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        "Add bot to a standup group",
        url=f"https://telegram.me/"
        f"standup_tbe_remak_bot?startgroup=true",
    )
    markup.add(button)
    await msg.reply(
        f"Hello, {msg.from_user.first_name}!\n"
        f"You need add me to your stand-up group.\n"
        f"I will be posting team updates there.\n"
        f"**Thanks!**\n\n"
        f"*Bot is in alfa version*, pls submit issues to ",
        reply_markup=markup,
        reply=False,
    )


async def help_bot(msg: types.Message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(
        "submit a ticket",
        url=r"https://github.com/ZhukovGreen"
        r"/telegram-standup-bot/issues",
    )
    markup.add(button)
    await msg.reply(
        "The support channel is "
        "https://t.me/joinchat/EiE7ykcEzD3-3DfvxzdSow",
        reply_markup=markup,
        reply=False,
    )
