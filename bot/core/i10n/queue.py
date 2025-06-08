from core.i10n.common import gen_response
from core.i10n import queue__en as en
from core.i10n import queue__ua as ua
from core.i10n import queue__it as it


def status_message(processing: int, queue: int) -> str:
    return gen_response(en.status_message, ua.status_message, it.status_message, processing, queue)
