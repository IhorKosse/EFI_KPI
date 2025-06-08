def raise_limit(minutes: int, seconds: int) -> str:
    parts = []
    if minutes > 0:
        minute_word = "хвилину" if minutes == 1 else "хвилини" if 1 < minutes < 5 else "хвилин"
        parts.append(f"{minutes} {minute_word}")
    if seconds > 0:
        second_word = "секунду" if seconds == 1 else "секунди" if 1 < seconds < 5 else "секунд"
        parts.append(f"{seconds} {second_word}")
    
    time_str = " та ".join(parts)
    return f"Ви перевищили ліміт символів. Будь ласка, зачекайте {time_str}. Ми повідомимо вас коли закінчиться обмеження 🤝. Напишіть нам в підтримку, якщо у вас виникли проблеми @efi_support"

def permission_to_write_again() -> str:
    return "Обмеження за кількістю символів знято. Ви можете надсилати повідомлення."