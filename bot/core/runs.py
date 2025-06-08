import asyncio


async def get_update_or_wait(
    ai, thread_id: str, run_id: str, timeout_seconds: float = 2
):
    run_status = await ai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    if run_status.status in ["in_progress", "queued"]:
        while True:
            await asyncio.sleep(timeout_seconds)
            run_status = await ai.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id
            )
            if run_status.status not in ["in_progress", "queued"]:
                break

    return run_status
