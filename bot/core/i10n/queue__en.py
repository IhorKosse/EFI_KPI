def status_message(processing: int, queue: int) -> str:
    processing_word = "message" if processing == 1 else "messages"
    processing_part = "Processing" if processing < 2 else f"Processing: {processing} {processing_word}"

    if queue > 0:
        queue_word = "message" if queue == 1 else "messages"
        return f"{processing_part}. Queue: {queue} {queue_word}."
    else:
        return f"{processing_part}..."
