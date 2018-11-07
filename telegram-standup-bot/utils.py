import asyncio
import logging


logger = logging.getLogger(__file__)


async def cancel_task(task_id: int):
    task_reg = {
        id(task): task for task in asyncio.all_tasks()
    }
    try:
        task_reg[task_id].cancel()
    except KeyError:
        logger.warning(
            f"Trying to cancel the non existing task"
        )
        pass
