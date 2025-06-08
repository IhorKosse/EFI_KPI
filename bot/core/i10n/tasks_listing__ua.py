import datetime
import random


def no_tasks_for_today() -> str:
    with open("responses/ua_no_tasks_for_today.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def working_one_moment() -> str:
    with open("responses/ua_one_moment_working.txt", "r") as f:
        lines = f.readlines()
    return random.choice(lines).strip()


def no_tasks() -> str:
    # TODO: Make bot more human-like, provide more than one response.
    return "Задач немає ☺️\nДодамо щось?"


def no_tasks_for_this_day() -> str:
    # TODO: Make bot more human-like, provide more than one response.
    return "Немає завдань на цей день\\."


def no_tasks_in_inbox() -> str:
    return "Немає завдань в інбоксі ☺️\nДодамо щось?"


def start_command_text() -> str:
    return "Привіт, Я - Ефі, твій чат-бот планер! 👋\n\nТут ми не формалізуємось, спілкуйся так, як тобі зручно. Я твій герой у світі керування задачами! 🚀\n\nПлануй, створюй, закривай, оновлюй - усе в твоїх руках. Щоб побачити, як це працює, читай <a href='https://telegra.ph/EFI-UA-05-01'>Телеграф</a> - там все як на долоні. 📖\n\nПросто пиши мені, що потрібно, і я все зроблю.  Давай разом зробимо твої дні ефективними та легкими! 💪🏼"


def timezone_prompt() -> str:
    return "Виберіть свій часовий пояс:"


def timezone_first() -> str:
    return "Спочатку налаштуйте свій часовий пояс, використовуйте /start"


def timezone_update_message(picked_timezone_shift: str) -> str:
    return f"Дякую, ваш часовий пояс зараз UTC {picked_timezone_shift}, ви зможете його змінити потім в налаштуваннях."


def tutorial_start_message(task_prompt: str) -> str:
    return f"Все дуже просто, давай спробуємо прямо зараз\\. Додай свою першу задачу, ось загальні приклади задач: \n {task_prompt} \nАбо ж ти можеш спробувати написати щось своє і подивитись на результат\\. Для детального розуміння, як створювати, оновлювати, видаляти і шукати задачі прочитай [Телеграф](https://telegra.ph/EFI-UA-05-01) \\."


def task_start_prompt() -> str:
    return "\n *\\- Нагадай глянути подкаст через 20 хв\\.\n \\- Нагадай почистити галерею через годину \\(займе годину часу\\)\\.\n \\- Тренування з 14 по 16 сьогодні\\.*\n"


def task_completion_prompt() -> str:
    return "Перенеси читання телеграфу Efi ще на годину."


def task_completion_message(task_prompt: str) -> str:
    return f"Чудово, ти додав свою першу задачу, тепер спробуй оновити її, написавши: '{task_prompt}' 📖"


def task_update_prompt() -> str:
    return "Я вже прочитав телеграф Efi."


def task_update_message(task_prompt: str) -> str:
    return f"Супер, задача оновлена. Прочитай телеграф та видали задачу про телеграф або ж просто напиши:  '{task_prompt}' 📖"


def task_close_message() -> str:
    return "Та-дам, я видалив задачу а ти тепер знаєш, як легко зі мною управляти задачами. 💪 \n\nЩе багато класних фішок чекає на тебе. Так що давай, вперед до ефективності з Ефі! ✨👊"


def close_tutorial() -> str:
    return "Завершити туторіал ."


def tutorial_complete_message() -> str:
    return "Туторіал завершено, якщо ви не пройшли туторіал до кінця, не забудьте закрити свої тестові задачі). Щоб дізнатись більше, дивіться <a href='https://telegra.ph/EFI-UA-05-01'>Телеграф</a>"


def oops() -> str:
    return "Упс, щось пішло не так. Спробуймо ще разочок? Буде краще перефразувати задачу. Напиши нам в підтримку, якщо у тебе виникли проблеми @efi_support"


def invalid_command() -> str:
    return "Виникла недійсна команда. Напиши нам в підтримку, якщо у тебе виникли проблеми @efi_support"


def smth_wrong() -> str:
    return "Щось пішло не так з нашої сторони, ми вже знаємо про це і працюємо над виправленням. Напиши нам в підтримку, якщо у тебе виникли проблеми @efi_support"


def non_text_message() -> str:
    return "Повідомлення, що не є текстом, зараз не підтримуються. Напиши нам в підтримку, якщо у тебе виникли проблеми @efi_support"


def settings_menu_text() -> str:
    return "Налаштування, виберіть, що вам потрібно змінити"


def settings_timezone_update_message(picked_timezone_shift_hours: str) -> str:
    return f"Дякую, ваш часовий пояс зараз {picked_timezone_shift_hours} UTC."


def current_time(offset_time: datetime) -> str:
    return f"Поточний час: {offset_time.replace(microsecond=0)}"


def today() -> str:
    return "📅 Сьогодні"


def auto_reminders() -> str:
    return "Авто нагадування:"

def auto_reminders_on() -> str:
    return "В час початку"

def auto_reminders_off() -> str:
    return "Вимкнені"

def auto_reminders_15() -> str:
    return "15 хв до початку"

def auto_reminders_30() -> str:
    return "30 хв до початку"

def auto_reminders_60() -> str:
    return "60 хв до початку"


def all_tasks() -> str:
    return "Всі задачі"


def todays_tasks() -> str:
    return "Задачі на сьогодні"


def overdue_tasks() -> str:
    return "Прострочені задачі"


def no_todays_tasks() -> str:
    return "Немає задач на сьогодні"


def tomorrows_tasks() -> str:
    return "Задачі на завтра"


def no_tomorrows_tasks() -> str:
    return "Немає задач на завтра"


def weeks_tasks() -> str:
    return "Задачі на тиждень"


def no_weeks_tasks() -> str:
    return "Немає задач на цей тиждень"


def workweeks_tasks() -> str:
    return "Задачі на робочий тиждень"


def no_workweeks_tasks() -> str:
    return "Немає задач на цей робочий тиждень"


def weekends_tasks() -> str:
    return "Задачі на вихідні"


def no_weekends_tasks() -> str:
    return "Немає задач на ці вихідні"


def two_weeks_tasks() -> str:
    return "Задачі на два тижні"


def no_two_weeks_tasks() -> str:
    return "Немає задач на наступні два тижні"


def inbox_tasks() -> str:
    return "Задачі в інбоксі"


def no_inbox_tasks() -> str:
    return "Немає задач в інбоксі"


def days() -> list[str]:
    return ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]


def days_short() -> list[str]:
    return ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]


def months() -> list[str]:
    return [
        "Січень",
        "Лютий",
        "Березень",
        "Квітень",
        "Травень",
        "Червень",
        "Липень",
        "Серпень",
        "Вересень",
        "Жовтень",
        "Листопад",
        "Грудень",
    ]


def months_short() -> list[str]:
    return ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]


def total_tasks() -> str:
    return "Всього задач"


def load_more_tasks() -> str:
    return "Більше задач"


def by() -> str:
    return "до "


def free_trial_activated() -> str:
    return "🎉 Твій безкоштовний період користування активовано! Enjoy! 😉\n\nБільше про нього можна знайти за цим посиланням, або ж в налаштуваннях ⚙️"
