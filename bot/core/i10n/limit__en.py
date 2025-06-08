def raise_limit(minutes: int, seconds: int) -> str:
    parts = []
    if minutes > 0:
        minute_word = "minute" if minutes == 1 else "minutes"
        parts.append(f"{minutes} {minute_word}")
    if seconds > 0:
        second_word = "second" if seconds == 1 else "seconds"
        parts.append(f"{seconds} {second_word}")
    
    time_str = " and ".join(parts)
    return f"You have exceeded the character limit. Please wait {time_str}. We will notify you when the restriction ends 🤝. Let us know if you'd like some help from us @efi_support"

def permission_to_write_again() -> str:
    return "The character limit has been lifted. You can send messages now."