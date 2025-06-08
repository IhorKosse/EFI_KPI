import datetime
import random


def no_tasks_for_today() -> str:
    with open("responses/en_no_tasks_for_today.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def working_one_moment() -> str:
    with open("responses/en_one_moment_working.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def no_tasks() -> str:
    # TODO: Make bot more human-like, provide more than one response.
    return "No tasks ☺️\nWanna add something?"


def no_tasks_for_this_day() -> str:
    # TODO: Make bot more human-like, provide more than one response.
    return "There are no tasks for this day\\."


def no_tasks_in_inbox() -> str:
    # TODO: Make bot more human-like, provide more than one response.
    return "Empty inbox ☺️\nWanna add something?"


def start_command_text() -> str:
    return "Hello, I'm Efi, your chat-bot planner! 👋\n\nWe're informal here, communicate as you're comfortable. I'm your hero in the world of task management! 🚀\n\nPlan, create, close, update - everything is in your hands. To see how it works, read <a href='https://telegra.ph/EFI-EN-05-01'>Telegraph</a> - everything is clear there. 📖\n\nJust write to me what you need, and I'll do everything. Let's make your days effective and easy together! 💪🏼"


def timezone_prompt() -> str:
    return "Choose your time zone:"


def timezone_first() -> str:
    return "Please setup your timezone first, use /start"


def timezone_update_message(picked_timezone_shift: str) -> str:
    return f"Thank you, your time zone is now UTC {picked_timezone_shift}, you can change it later in the settings."


def tutorial_start_message(task_prompt: str) -> str:
    return f"It's very simple, let's try it right now\\. Add your first task, here are general examples of tasks: \n {task_prompt} \nOr you can try to write something of your own and see the result\\. For a detailed understanding of how create, update, delete and search tasks read [Telegraph](https://telegra.ph/EFI-EN-05-01) \\."


def task_start_prompt() -> str:
    return "\n *\\- Remind to watch the podcast in 20 min\\.\n \\- Remind to clean the gallery in an hour \\(will take an hour\\)\\.\n \\- Training from 14 to 16 today \\.*\n"


def task_completion_prompt() -> str:
    return "Postpone reading the Efi telegraph for another hour."


def task_completion_message(task_prompt: str) -> str:
    return f"Great, you've added your first task, now try to update it by writing: '{task_prompt}' 📖"


def task_update_prompt() -> str:
    return "I've already read the Efi telegraph."


def task_update_message(task_prompt: str) -> str:
    return f"Super, task updated. Read the telegraph and delete the telegraph task or just write: '{task_prompt}' 📖"


def task_close_message() -> str:
    return "Ta-dam, I deleted the task and you now know how easy it is to manage tasks with me. 💪 \n\nMany more cool features are waiting for you. So let's go, forward to efficiency with Efi! ✨👊"


def close_tutorial() -> str:
    return "End the tutorial."


def tutorial_complete_message() -> str:
    return "Tutorial completed, if you didn't complete the tutorial to the end, don't forget to close your test tasks). To learn more, see <a href='https://telegra.ph/EFI-EN-05-01'>Telegraph</a>"


def oops() -> str:
    return "Oops, something went wrong. Let's try again? It would be better to rephrase the task. Let us know if you'd like some help from us @efi_support"


def invalid_command() -> str:
    return "Invalid command occurred. Let us know if you'd like some help from us @efi_support"


def smth_wrong() -> str:
    return "Something went wrong on our side, we already know about that and working to fix. Let us know if you'd like some help from us @efi_support"


def non_text_message() -> str:
    return "Non text messages are not supported right now. Let us know if you'd like some help from us @efi_support."


def settings_menu_text() -> str:
    return "Settings, choose what you need to change"


def settings_timezone_update_message(picked_timezone_shift_hours: str) -> str:
    return f"Thank you, your time zone is now {picked_timezone_shift_hours} UTC."


def current_time(offset_time: datetime) -> str:
    return f"Current time: {offset_time.replace(microsecond=0)}"


def today() -> str:
    return "📅 Today"


def all_tasks() -> str:
    return "All tasks"

def auto_reminders() -> str:
    return "Auto reminders:"

def auto_reminders_on() -> str:
    return "On time"

def auto_reminders_off() -> str:
    return "Off"

def auto_reminders_15() -> str:
    return "15 min before"

def auto_reminders_30() -> str:
    return "30 min before"

def auto_reminders_60() -> str:
    return "60 min before"


def todays_tasks() -> str:
    return "Today's tasks"


def overdue_tasks() -> str:
    return "Overdue tasks"


def no_todays_tasks() -> str:
    return "No tasks for today"


def tomorrows_tasks() -> str:
    return "Tomorrow's tasks"


def no_tomorrows_tasks() -> str:
    return "No tasks for tomorrow"


def weeks_tasks() -> str:
    return "Week's tasks"


def no_weeks_tasks() -> str:
    return "No tasks for this week"


def workweeks_tasks() -> str:
    return "Workweek's tasks"


def no_workweeks_tasks() -> str:
    return "No tasks for this workweek"


def weekends_tasks() -> str:
    return "Weekend's tasks"


def no_weekends_tasks() -> str:
    return "No tasks for this weekend"


def two_weeks_tasks() -> str:
    return "Two weeks tasks"


def no_two_weeks_tasks() -> str:
    return "No tasks for the next two weeks"


def inbox_tasks() -> str:
    return "Inbox tasks"


def no_inbox_tasks() -> str:
    return "No tasks in the inbox"


def days() -> list[str]:
    return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def days_short() -> list[str]:
    return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def months() -> list[str]:
    return [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]


def months_short() -> list[str]:
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def total_tasks() -> str:
    return "Total tasks"


def load_more_tasks() -> str:
    return "Load more tasks"


def by() -> str:
    return "by "
