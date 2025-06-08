from core.i10n import tasks_closing__ua as ua
from core.i10n import tasks_closing__en as en
from core.i10n import tasks_closing__it as it
from core.i10n.common import gen_response


def ok_task_marked_as_done() -> str:
    return gen_response(en.ok_task_marked_as_done, ua.ok_task_marked_as_done, it.ok_task_marked_as_done)


def ok_task_closed() -> str:
    return gen_response(en.ok_task_closed, ua.ok_task_closed, it.ok_task_closed)
