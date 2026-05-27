import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

from dotenv import load_dotenv
import yt_dlp

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "MusicBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(bot)

if not os.path.exists("downloads"):
    os.makedirs("downloads")

async def download_audio(query):

    loop = asyncio.get_event_loop()

    def run():

        ydl_opts = {
            "format": "bestaudio",
            "quiet": True,
            "outtmpl": "downloads/%(id)s.%(ext)s"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                f"ytsearch:{query}",
                download=True
            )["entries"][0]

            return ydl.prepare_filename(info)

    return await loop.run_in_executor(None, run)

@bot.on_message(filters.command("start"))
async def start_handler(_, message: Message):

    await message.reply_text(
        "Music Bot Started"
    )

@bot.on_message(filters.command("play"))
async def play_handler(_, message: Message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage: /play song"
        )

    query = " ".join(message.command[1:])

    msg = await message.reply_text(
        "Downloading..."
    )

    try:

        file_path = await download_audio(query)

        await call_py.join_group_call(
            message.chat.id,
            AudioPiped(file_path)
        )

        await msg.edit_text(
            "Streaming Started"
        )

    except Exception as e:

        await msg.edit_text(
            str(e)
        )

async def main():

    await bot.start()
    await call_py.start()

    print("Bot Started Successfully")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
