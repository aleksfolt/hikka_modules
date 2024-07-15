from pyrogram import Client, filters
import requests

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]

cinfo = f"🎬`{prefix_userbot}movie`"
ccomand = " показывает информацию о фильме. Пример: `movie Inception`"

def register_module(app: Client):
    @app.on_message(filters.command("movie", prefixes=prefix_userbot))
    async def movie(_, message):
        try:
            movie_name = message.text.split(" ", maxsplit=1)[1]
            response = requests.get(f"http://www.omdbapi.com/?t={movie_name}&apikey=YOUR_OMDB_API_KEY")
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

print("Модуль movie загружен!")
