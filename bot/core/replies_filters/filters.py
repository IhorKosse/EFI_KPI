from core.common import BotCtx, TelegramMessageCtx, TelegramUserCtx
from core.i10n.reply_messages import cant_find_related_task
from core.messages.history import edit_in_history, fetch
from core.replies_filters.actions import process_task_completing, process_task_reopening
from core.replies_filters.regexp_filters import apply_regexp_filters
from aiogram import enums

async def apply_message_reply_filters(ctx: BotCtx, ray: int, input: TelegramMessageCtx) -> (bool, str|None, str|None):
    related_message_id = input.message.reply_to_message.message_id

    user = TelegramUserCtx.from_message_context(input)


    response = await fetch(ray, chat_id=user._id, message_id=related_message_id)
    messages = response.get("results", [])
    if messages and messages[0].get("related_task_ids_json"):
        if len(messages)>0 and len(messages[0].get("related_task_ids_json"))>0:
            related_task_id = messages[0]["related_task_ids_json"][0]

    if not related_task_id:
        await input.message.reply(cant_find_related_task())
        return

    related_task_id = int(related_task_id)
    lowercased_message = input.message.text.lower()

    reply = await apply_regexp_filters(ctx, ray, user, lowercased_message, related_task_id)
    if reply:
        return True, reply, None
    else:
        content = messages[0]['content']

        related_task_id = messages[0]['related_task_ids_json'][0] if messages[0]['related_task_ids_json'] else None

        task_data = f" {content}  Task ID: {related_task_id}"

        return False, None, task_data


async def close_tasks_by_reaction(ray: int, message_id: int, chat_id: int, ctx: BotCtx, user: TelegramUserCtx, session:None) -> str | None:
    response = await fetch(ray, chat_id=chat_id, message_id=message_id)
    messages = response.get("results", [])
    message = messages[0]
    related_task_ids = message.get("related_task_ids_json", [])
    if not related_task_ids:
        return None

    # Assuming there's only one related task ID for simplicity
    task_id = related_task_ids[0]

    # Cross out the message text to indicate completion
    old_text = message.get("content", "")
    new_text = f"~{old_text}~"

    await ctx.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=new_text,
        parse_mode=enums.ParseMode.MARKDOWN_V2
    )
    await edit_in_history(
        ray=ray,
        chat_id=chat_id,
        message_id=message_id,
        new_text=new_text,
        type=message.get("type", ""),
        related_tasks_ids=related_task_ids,
        session=session
    )
    return await process_task_completing(ctx=None, ray=ray, user=user, target_task_id=task_id)

async def reopen_tasks_by_reaction(ray: int, message_id: int, chat_id: int, ctx: BotCtx, user: TelegramUserCtx, session:None) -> str | None:
    response = await fetch(ray, chat_id=chat_id, message_id=message_id)
    messages = response.get("results", [])
    message = messages[0]
    related_task_ids = message.get("related_task_ids_json", [])
    if not related_task_ids:
        return None

    # Assuming there's only one related task ID for simplicity
    task_id = related_task_ids[0]

    # Cross out the message text to indicate completion
    old_text = message.get("content", "")
    new_text = f"~{old_text}~"

    await ctx.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=new_text,
        parse_mode=enums.ParseMode.MARKDOWN_V2
    )
    await edit_in_history(
        ray=ray,
        chat_id=chat_id,
        message_id=message_id,
        new_text=new_text,
        type=message.get("type", ""),
        related_tasks_ids=related_task_ids,
        session=session
    )
    return await process_task_reopening(ctx=None, ray=ray, user=user, target_task_id=task_id)