def status_message(processing: int, queue: int) -> str:
    processing_word = (
        "повідомлення" if processing == 1 else "повідомлень" if processing > 4 else ""
    )
    queue_word = (
        "повідомлення" if queue == 1 else "повідомлень" if queue > 4 else ""
    )

    processing_part = f"Обробляється: {processing} {processing_word}" if processing >= 2 else "Обробляю"
    queue_part = f"В черзі: {queue} {queue_word}"

    if queue > 0:
        return f"{processing_part}. {queue_part}."
    else:
        return f"{processing_part}..."