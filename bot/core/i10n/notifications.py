from core.i10n.common import gen_response
from core.i10n import notifications__en as en
from core.i10n import notifications__ua as ua
from core.i10n import notifications__it as it


def days(hours: int, days: int) -> str:
    return gen_response(en.days, ua.days, it.days, hours, days)


def hours(hours: int) -> str:
    return gen_response(en.hours, ua.hours, it.hours, hours)


def minutes(minutes: int) -> str:
    return gen_response(en.minutes, ua.minutes, it.minutes, minutes)


def right_now() -> str:
    return gen_response(en.right_now, ua.right_now, it.right_now)
