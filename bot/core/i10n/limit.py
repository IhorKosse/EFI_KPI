from core.i10n.common import gen_response
from core.i10n import limit__en as en
from core.i10n import limit__ua as ua
from core.i10n import limit__it as it


def raise_limit(minutes: int, seconds: int) -> str:
    return gen_response(en.raise_limit, ua.raise_limit, it.raise_limit, minutes, seconds)


def permission_to_write_again() -> str:
    return gen_response(en.permission_to_write_again, ua.permission_to_write_again, it.permission_to_write_again)
