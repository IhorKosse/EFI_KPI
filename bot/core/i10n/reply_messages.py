from core.i10n import reply_messages__ua as ua
from core.i10n import reply_messages__en as en
from core.i10n import reply_messages__it as it
from core.i10n.common import gen_response


def cant_find_related_task() -> str:
    return gen_response(en.cant_find_related_task, ua.cant_find_related_task, it.cant_find_related_task)
