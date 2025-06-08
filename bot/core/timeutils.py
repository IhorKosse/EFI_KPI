import datetime
from core.common import TelegramUserCtx

from core.settings.timezone import get_timezone_shift


async def now_according_to_users_timezone(user: TelegramUserCtx) -> datetime.datetime:
    timezone_shift = await get_timezone_shift(user)
    utc_now = datetime.datetime.utcnow()

    # Calculate time in the specified UTC offset
    if timezone_shift is None:
        offset_time = utc_now
    else:
        offset_time = utc_now + datetime.timedelta(hours=timezone_shift)

    # Remove milliseconds and return the datetime object
    return offset_time.replace(microsecond=0)
