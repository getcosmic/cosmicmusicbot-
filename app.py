import os
import asyncio
from pyrogram import Client, filters
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

async def download_audio(query):

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

    loop = asyncio.get_event_loop()

    return await loop.run_in_executor(None, run)

@bot.on_message(filters.command("start"))
async def start(_, message):

    await message.reply_text(
        "Music Bot Started"
    )

@bot.on_message(filters.command("play"))
async def play(_, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage: /play song"
        )

    query = " ".join(message.command[1:])

    msg = await message.reply_text(
        "Downloading..."
    )

    path = await download_audio(query)

    await call_py.join_group_call(
        message.chat.id,
        AudioPiped(path)
    )

    await msg.edit_text(
        "Streaming Started"
    )

async def main():

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    await bot.start()
    await call_py.start()

    print("Bot Started")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
