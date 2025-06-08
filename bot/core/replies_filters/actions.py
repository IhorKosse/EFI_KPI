from core import log
from core.api import tasks
from core.common import BotCtx, TelegramMessageCtx
from core.i10n.reply_messages import cant_find_related_task
from core.i10n.tasks_closing import ok_task_closed, ok_task_marked_as_done


async def process_task_completing(ctx: BotCtx, ray: int, user: TelegramMessageCtx, target_task_id: int) -> str | None:
    try:
        await tasks.close_one(user, target_task_id, completed=True)
        return ok_task_marked_as_done()

    except Exception as e:
        if "No matching records found" in str(e):
            return cant_find_related_task()

        else:
            log.error(ray, f"failed to mark task {target_task_id} as done")
            raise e


async def process_task_deletion(ctx: BotCtx, ray: int, user: TelegramMessageCtx, target_task_id: int) -> str | None:
    try:
        await tasks.close_one(user, target_task_id, completed=False)
        return ok_task_closed()

    except Exception as e:
        if "No matching records found" in str(e):
            return cant_find_related_task()

        else:
            log.error(ray, f"failed to close task {target_task_id}")
            raise e

async def process_task_reopening (ctx: BotCtx, ray: int, user: TelegramMessageCtx, target_task_id: int) -> str | None:
    try:
        await tasks.reopen_one(user, target_task_id)
        return ok_task_marked_as_done()

    except Exception as e:
        if "No matching records found" in str(e):
            return cant_find_related_task()

        else:
            log.error(ray, f"failed to mark task {target_task_id} as reopen")
            raise e