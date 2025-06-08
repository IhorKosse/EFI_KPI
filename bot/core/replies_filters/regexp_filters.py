import settings
from core.common import BotCtx, TelegramUserCtx
from core.i10n.common import EN, UA
from core.replies_filters import regexp_tasks_complete_common as mark_as_done_common
from core.replies_filters import regexp_tasks_complete_en as mark_as_done_en
from core.replies_filters import regexp_tasks_complete_ua as mark_as_done_ua
from core.replies_filters import regexp_tasks_delete_en as delete_en
from core.replies_filters import regexp_tasks_delete_ua as delete_ua
from core.replies_filters.actions import process_task_completing, process_task_deletion


async def apply_regexp_filters(
    ctx: BotCtx, ray: int, user: TelegramUserCtx, message_lowercased: str, target_task_id: int
) -> str | None:
    task_must_be_marked_as_completed = (
        (
            settings.LOCALIZATION == UA
            and (
                # WARN: Notice priority of calls.
                mark_as_done_ua.match(ray, message_lowercased)
                or mark_as_done_common.match(ray, message_lowercased)
                or mark_as_done_en.match(ray, message_lowercased)
            )
        )
        or (
            settings.LOCALIZATION == EN
            and (
                # WARN: Notice priority of calls.
                mark_as_done_en.match(ray, message_lowercased)
                or mark_as_done_common.match(ray, message_lowercased)
                or mark_as_done_ua.match(ray, message_lowercased)
            )
        )
        or (message_lowercased in ["👍", "👌", "🆗", "✅", "☑️"])
    )

    if task_must_be_marked_as_completed:
        return await process_task_completing(ctx, ray, user, target_task_id)

    task_must_be_deleted = (
        (
            settings.LOCALIZATION == UA
            and (
                # WARN: Notice priority of calls.
                delete_ua.match(ray, message_lowercased)
                # or delete_common.match(ray, message_lowercased)
                or delete_en.match(ray, message_lowercased)
            )
        )
        or (
            settings.LOCALIZATION == EN
            and (
                # WARN: Notice priority of calls.
                delete_en.match(ray, message_lowercased)
                # or delete_common.match(ray, message_lowercased)
                or delete_ua.match(ray, message_lowercased)
            )
        )
        or (message_lowercased in ["👍", "👌", "🆗", "✅", "☑️"])
    )

    if task_must_be_deleted:
        return await process_task_deletion(ctx, ray, user, target_task_id)

    # Means that no filter has been applied,
    # and no action is done.
    return None
