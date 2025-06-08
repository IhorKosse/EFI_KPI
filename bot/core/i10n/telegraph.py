from core.i10n.common import gen_response
from core.i10n import telegraph_en as en
from core.i10n import telegraph_ua as ua
from core.i10n import telegraph_it as it


def telegraph() -> str:
    return gen_response(en.telegraph, ua.telegraph, it.telegraph)


def telegraph_link() -> str:
    return gen_response(en.telegraph_link, ua.telegraph_link, it.telegraph_link)
