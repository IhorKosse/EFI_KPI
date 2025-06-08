from io import BytesIO
from pydub import AudioSegment
from core.common import BotCtx


async def convert_voice_to_text(message, ctx: BotCtx):
    # Get information about the voice message file
    file_info = await ctx.bot.get_file(message.voice.file_id)

    # Download the file from the Telegram server
    voice_file = BytesIO()
    await ctx.bot.download_file(file_info.file_path, destination=voice_file)

    # Move the pointer to the beginning of the file
    voice_file.seek(0)

    # Convert the audio file to MP3 format using pydub
    audio = AudioSegment.from_file(voice_file, format="ogg")
    mp3_audio = BytesIO()
    audio.export(mp3_audio, format="mp3")
    mp3_audio.seek(0)

    # Check for successful conversion
    if mp3_audio.getbuffer().nbytes == 0:
        raise ValueError("Conversion of audio file to MP3 failed.")

    # Ensure the file is sent as bytes and the header is set correctly
    files = {"file": ("audio.mp3", mp3_audio, "audio/mpeg")}

    try:
        # Transcribe the voice message using OpenAI Whisper
        transcription = await ctx.ai.audio.transcriptions.create(
            model="whisper-1", file=files["file"], response_format="text"
        )
    finally:
        # Ensure resources are released
        voice_file.close()
        mp3_audio.close()

    return transcription
