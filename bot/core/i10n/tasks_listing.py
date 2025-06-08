import datetime
from core.i10n.common import gen_response
from core.i10n import tasks_listing__ua as ua
from core.i10n import tasks_listing__en as en
from core.i10n import tasks_listing__it as it


def working_one_moment() -> str:
    return gen_response(en.working_one_moment, ua.working_one_moment, it.working_one_moment)


def no_tasks_for_today() -> str:
    return gen_response(en.no_tasks_for_today, ua.no_tasks_for_today, it.no_tasks_for_today)


def no_tasks() -> str:
    return gen_response(en.no_tasks, ua.no_tasks, it.no_tasks)


def no_tasks_for_this_day() -> str:
    return gen_response(en.no_tasks_for_this_day, ua.no_tasks_for_this_day, it.no_tasks_for_this_day)


def no_tasks_in_inbox() -> str:
    return gen_response(en.no_tasks_in_inbox, ua.no_tasks_in_inbox, it.no_tasks_in_inbox)


def start_command_text() -> str:
    return gen_response(en.start_command_text, ua.start_command_text, it.start_command_text)


def timezone_prompt() -> str:
    return gen_response(en.timezone_prompt, ua.timezone_prompt, it.timezone_prompt)


def timezone_first() -> str:
    return gen_response(en.timezone_first, ua.timezone_first, it.timezone_first)


def timezone_update_message(picked_timezone_shift: str) -> str:
    return gen_response(
        en.timezone_update_message, ua.timezone_update_message, it.timezone_update_message, picked_timezone_shift
    )


def tutorial_start_message(task_prompt: str) -> str:
    return gen_response(en.tutorial_start_message, ua.tutorial_start_message, it.tutorial_start_message, task_prompt)


def task_start_prompt() -> str:
    return gen_response(en.task_start_prompt, ua.task_start_prompt, it.task_start_prompt)


def task_completion_prompt() -> str:
    return gen_response(en.task_completion_prompt, ua.task_completion_prompt, it.task_completion_prompt)


def task_completion_message(task_prompt: str) -> str:
    return gen_response(en.task_completion_message, ua.task_completion_message, it.task_completion_message, task_prompt)


def task_update_prompt() -> str:
    return gen_response(en.task_update_prompt, ua.task_update_prompt, it.task_update_prompt)


def task_update_message(task_prompt: str) -> str:
    return gen_response(en.task_update_message, ua.task_update_message, it.task_update_message, task_prompt)


def task_close_message() -> str:
    return gen_response(en.task_close_message, ua.task_close_message, it.task_close_message)


def close_tutorial() -> str:
    return gen_response(en.close_tutorial, ua.close_tutorial, it.close_tutorial)


def tutorial_complete_message() -> str:
    return gen_response(en.tutorial_complete_message, ua.tutorial_complete_message, it.tutorial_complete_message)


def oops() -> str:
    return gen_response(en.oops, ua.oops, it.oops)


def invalid_command() -> str:
    return gen_response(en.invalid_command, ua.invalid_command, it.invalid_command)


def smth_wrong() -> str:
    return gen_response(en.smth_wrong, ua.smth_wrong, it.smth_wrong)


def non_text_message() -> str:
    return gen_response(en.non_text_message, ua.non_text_message, it.non_text_message)


def settings_menu_text() -> str:
    return gen_response(en.settings_menu_text, ua.settings_menu_text, it.settings_menu_text)


def settings_timezone_update_message(picked_timezone_shift_hours: str) -> str:
    return gen_response(
        en.settings_timezone_update_message,
        ua.settings_timezone_update_message,
        it.settings_timezone_update_message,
        picked_timezone_shift_hours,
    )


def auto_reminders() -> str:
    return gen_response(en.auto_reminders, ua.auto_reminders, it.auto_reminders)


def auto_reminders_on() -> str:
    return gen_response(en.auto_reminders_on, ua.auto_reminders_on, it.auto_reminders_on)


def auto_reminders_off() -> str:
    return gen_response(en.auto_reminders_off, ua.auto_reminders_off, it.auto_reminders_off)


def auto_reminders_15() -> str:
    return gen_response(en.auto_reminders_15, ua.auto_reminders_15, it.auto_reminders_15)


def auto_reminders_30() -> str:
    return gen_response(en.auto_reminders_30, ua.auto_reminders_30, it.auto_reminders_30)


def auto_reminders_60() -> str:
    return gen_response(en.auto_reminders_60, ua.auto_reminders_60, it.auto_reminders_60)


def current_time(offset_time: datetime) -> str:
    return gen_response(en.current_time, ua.current_time, it.current_time, offset_time)


def all_tasks() -> str:
    return gen_response(en.all_tasks, ua.all_tasks, it.all_tasks)


def todays_tasks() -> str:
    return gen_response(en.todays_tasks, ua.todays_tasks, it.todays_tasks)


def overdue_tasks() -> str:
    return gen_response(en.overdue_tasks, ua.overdue_tasks, it.overdue_tasks)


def no_todays_tasks() -> str:
    return gen_response(en.no_todays_tasks, ua.no_todays_tasks, it.no_todays_tasks)


def tomorrows_tasks() -> str:
    return gen_response(en.tomorrows_tasks, ua.tomorrows_tasks, it.tomorrows_tasks)


def no_tomorrows_tasks() -> str:
    return gen_response(en.no_tomorrows_tasks, ua.no_tomorrows_tasks, it.no_tomorrows_tasks)


def weeks_tasks() -> str:
    return gen_response(en.weeks_tasks, ua.weeks_tasks, it.weeks_tasks)


def no_weeks_tasks() -> str:
    return gen_response(en.no_weeks_tasks, ua.no_weeks_tasks, it.no_weeks_tasks)


def workweeks_tasks() -> str:
    return gen_response(en.workweeks_tasks, ua.workweeks_tasks, it.workweeks_tasks)


def no_workweeks_tasks() -> str:
    return gen_response(en.no_workweeks_tasks, ua.no_workweeks_tasks, it.no_workweeks_tasks)


def weekends_tasks() -> str:
    return gen_response(en.weekends_tasks, ua.weekends_tasks, it.weekends_tasks)


def no_weekends_tasks() -> str:
    return gen_response(en.no_weekends_tasks, ua.no_weekends_tasks, it.no_weekends_tasks)


def two_weeks_tasks() -> str:
    return gen_response(en.two_weeks_tasks, ua.two_weeks_tasks, it.two_weeks_tasks)


def no_two_weeks_tasks() -> str:
    return gen_response(en.no_two_weeks_tasks, ua.no_two_weeks_tasks, it.no_two_weeks_tasks)


def inbox_tasks() -> str:
    return gen_response(en.inbox_tasks, ua.inbox_tasks, it.inbox_tasks)


def no_inbox_tasks() -> str:
    return gen_response(en.no_inbox_tasks, ua.no_inbox_tasks, it.no_inbox_tasks)


def days() -> list[str]:
    return gen_response(en.days, ua.days, it.days)


def days_short() -> list[str]:
    return gen_response(en.days_short, ua.days_short, it.days_short)


def months() -> list[str]:
    return gen_response(en.months, ua.months, it.months)


def months_short() -> list[str]:
    return gen_response(en.months_short, ua.months_short, it.months_short)


def total_tasks() -> str:
    return gen_response(en.total_tasks, ua.total_tasks, it.total_tasks)


def today() -> str:
    return gen_response(en.today, ua.today, it.today)


def load_more_tasks() -> str:
    return gen_response(en.load_more_tasks, ua.load_more_tasks, it.load_more_tasks)


def by() -> str:
    return gen_response(en.by, ua.by, it.by)
