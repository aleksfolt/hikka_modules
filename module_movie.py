from pyrogram import Client, filters
import requests

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]

cinfo = f"🎬`{prefix_userbot}movie`"
ccomand = " показывает информацию о фильме. Пример: `movie Inception`"

def get_api_key(service_name):
    try:
        with open("apis.bot", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith(f"{service_name}_key="):
                    return line.split("=", 1)[1].strip()
        return None
    except FileNotFoundError:
        return None

OMDB_API_KEY = get_api_key("omdb")

def register_module(app: Client):
    @app.on_message(filters.command("movie", prefixes=prefix_userbot))
    async def movie(_, message):
        if not OMDB_API_KEY:
            await message.reply_text("**❌API ключ не установлен. Установите его командой `.omdb_set_key <key>`.**\n\nПолучить api ключ можно на сайте: https://omdbapi.com/apikey.aspx")
            return
        try:
            movie_name = message.text.split(" ", maxsplit=1)[1]
            response = requests.get(f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}")
            data = response.json()
            if data["Response"] == "True":
                title = data["Title"]
                year = data["Year"]
                genre = data["Genre"]
                director = data["Director"]
                plot = data["Plot"]
                reply_text = (f"**🎬 Название:** {title}\n"
                              f"**📅 Год:** {year}\n"
                              f"**🎭 Жанр:** {genre}\n"
                              f"**🎬 Режиссер:** {director}\n"
                              f"**📖 Сюжет:** {plot}")
            else:
                reply_text = "**❌Фильм не найден.**"
        except Exception as e:
            reply_text = f"**❌Произошла ошибка: {e}**"
        await message.delete()
        await message.reply_text(reply_text)

    @app.on_message(filters.command("omdb_set_key", prefixes=prefix_userbot))
    async def set_key(_, message):
        global OMDB_API_KEY
        new_key = message.text.split(" ", maxsplit=1)[1]
        with open("apis.bot", "a") as file:
            file.write(f"omdb_key={new_key}\n")
        OMDB_API_KEY = new_key
        await message.delete()
        await message.reply_text("**✅API ключ успешно установлен!**")

print("Модуль movie загружен!")
