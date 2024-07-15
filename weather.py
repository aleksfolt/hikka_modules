from pyrogram import Client, filters
import requests
from datetime import datetime, timedelta

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]

cinfo = f"☀`{prefix_userbot}weather`"
ccomand = " показывает погоду в любом городе. Пример: `weather Москва`"


def get_api_key():
    try:
        with open("apis.bot", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("weather_key="):
                    return line.split("=", 1)[1].strip()
        return None
    except FileNotFoundError:
        return None


API_KEY = get_api_key()

weather_translation = {
    "ясно": ("ясное небо", "☀️"),
    "небольшая облачность": ("малооблачно", "🌤"),
    "облачно с прояснениями": ("облачно с прояснениями", "⛅"),
    "пасмурно": ("пасмурно", "☁️"),
    "небольшой дождь": ("небольшой дождь", "🌧"),
    "дождь": ("дождь", "🌧"),
    "гроза": ("гроза", "⛈"),
    "снег": ("снег", "❄️"),
    "туман": ("туман", "🌫"),
    "переменная облачность": ("переменная облачность", "🌤"),
}


def register_module(app: Client):
    @app.on_message(filters.command("weather_set_key", prefixes=prefix_userbot))
    async def set_key(_, message):
        global API_KEY
        new_key = message.text.split(" ", maxsplit=1)[1]
        with open("apis.bot", "a") as file:
            file.write(f"weather_key={new_key}\n")
        API_KEY = new_key
        await message.delete()
        await message.reply_text("**✅API ключ успешно установлен!**")

    @app.on_message(filters.command("weather", prefixes=prefix_userbot))
    async def weather(_, message):
        if not API_KEY:
            await message.reply_text("**❌API ключ не установлен. Установите его командой `.weather_set_key <key>`.**")
            return
        try:
            town = message.text.split(" ", maxsplit=1)[1]
            response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={town}&appid={API_KEY}&units=metric&lang=ru")
            data = response.json()
            if response.status_code == 200:
                town = data['name']
                temperature = data['main']['temp']
                weather_description = data['weather'][0]['description']
                timezone_offset = data['timezone']
                weather_rus, emoji = weather_translation.get(weather_description, (weather_description, "❓"))
                if emoji == "❓":
                    weather_rus = weather_description
                time_weather = (datetime.utcnow() + timedelta(seconds=timezone_offset)).strftime('%H:%M')
                reply_text = (f"**🏙Город:** {town}\n"
                              f"**🌡Температура:** {temperature}°C\n"
                              f"**{emoji}Погода:** {weather_rus}\n"
                              f"**⌛Время: {time_weather}**")
            else:
                reply_text = "**❌Произошла ошибка при получении данных о погоде.**"
        except IndexError:
            reply_text = "**❌Пожалуйста, укажите город. Пример: `weather Москва`**"
        except Exception as e:
            reply_text = f"**❌Произошла ошибка: {e}**"
        await message.delete()
        await message.reply_text(reply_text)


print("Модуль weather загружен!")
