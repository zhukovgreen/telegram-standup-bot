from ..app import dp


def convert_to_str_report(user_data: dict) -> str:
    return "\n\n".join(
        [
            f"*{ch}*\n{descr}"
            for ch, descr in user_data.items()
        ]
    )


async def get_target_chat(user_id: int) -> int:
    for chat_id, chat_data in dp.storage.data.items():
        if (
            int(chat_id) != user_id
            and str(user_id) in chat_data
        ):
            return int(chat_id)
    return user_id
