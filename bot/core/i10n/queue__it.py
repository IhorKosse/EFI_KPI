def status_message(processing: int, queue: int) -> str:
    processing_word = "messaggio" if processing == 1 else "messaggi"
    processing_part = "Elaborazione" if processing < 2 else f"Elaborazione: {processing} {processing_word}"

    if queue > 0:
        queue_word = "messaggio" if queue == 1 else "messaggi"
        return f"{processing_part}. Coda: {queue} {queue_word}."
    else:
        return f"{processing_part}..."
