from core.i10n import tasks_listing as i10n
from core.common import BotCtx, TelegramMessageCtx
from core.tutorial.tutorial import send_timezone


from aiogram.enums import ParseMode


async def handle_start_command(ray: int, ctx: BotCtx, input: TelegramMessageCtx):
    text = i10n.start_command_text()
    await input.message.answer(text, parse_mode=ParseMode.HTML)
    await send_timezone(input.message)
