from pyrogram import Client, filters
import requests

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]

cinfo = f"💱`{prefix_userbot}exchange_rate`"
ccomand = " показывает курс обмена валют. Пример: `exchange_rate USD RUB`"

def register_module(app: Client):
    @app.on_message(filters.command("exchange_rate", prefixes=prefix_userbot))
    async def exchange_rate(_, message):
        try:
            base, target = message.text.split(" ")[1:3]
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base.upper()}")
            data = response.json()
            rate = data["rates"].get(target.upper())
            if rate:
                reply_text = f"**Курс {base.upper()} к {target.upper()}:** {rate}"
            else:
                reply_text = "**❌Неверная валюта.**"
        except Exception as e:
            reply_text = f"**❌Произошла ошибка: {e}**"
        await message.delete()
        await message.reply_text(reply_text)

print("Модуль exchange_rate загружен!")
