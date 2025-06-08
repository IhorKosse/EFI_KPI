def days(hours: int, days: int) -> str:
    day_word = "день" if days == 1 else "дні" if 1 < days < 5 else "днів"
    if hours != 0:
        hour_word = "година" if hours == 1 else "години" if 1 < hours < 5 else "годин"
        return f"{int(days)} {day_word} та {int(hours)} {hour_word} залишилось"
    else:
        return f"{int(days)} {day_word}"

def hours(hours: int) -> str:
    hour_word = "година" if hours == 1 else "години" if 1 < hours < 5 else "годин"
    return f"{int(hours)} {hour_word} залишилось"

def minutes(minutes: int) -> str:
    minute_word = "хвилина" if minutes == 1 else "хвилини" if 1 < minutes < 5 else "хвилин"
    return f"{int(minutes)} {minute_word} залишилось"

def right_now() -> str:
    return "Зараз"