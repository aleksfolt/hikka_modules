from pyrogram import Client, filters
from datetime import datetime
import pytz

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]

cinfo = f"🕒`{prefix_userbot}time`"
ccomand = " показывает текущее время в указанном городе. Пример: `time Europe/Moscow`"

def register_module(app: Client):
    @app.on_message(filters.command("time", prefixes=prefix_userbot))
    async def time(_, message):
        try:
            city = message.text.split(" ", maxsplit=1)[1]
            timezone = pytz.timezone(city)
            current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            reply_text = f"**Текущее время в {city}:**\n{current_time}"
        except Exception as e:
            reply_text = f"**❌Произошла ошибка: {e}**"
        await message.delete()
        await message.reply_text(reply_text)

print("Модуль time загружен!")
