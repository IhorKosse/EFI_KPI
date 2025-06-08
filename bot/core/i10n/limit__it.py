def raise_limit(minutes: int, seconds: int) -> str:
    parts = []
    if minutes > 0:
        minute_word = "minuto" if minutes == 1 else "minuti"
        parts.append(f"{minutes} {minute_word}")
    if seconds > 0:
        second_word = "secondo" if seconds == 1 else "secondi"
        parts.append(f"{seconds} {second_word}")

    time_str = " e ".join(parts)
    return f"Hai superato il limite di caratteri. Per favore, aspetta {time_str}. Ti avviseremo quando la restrizione terminerà 🤝. Facci sapere se hai bisogno di aiuto @efi_support"


def permission_to_write_again() -> str:
    return "Il limite di caratteri è stato rimosso. Ora puoi inviare messaggi."
