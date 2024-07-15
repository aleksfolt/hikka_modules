from pyrogram import Client, filters
import speedtest

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]

cinfo = f"⚡`{prefix_userbot}speedtest`"
ccomand = " показывает скорость интернета. Пример: `speedtest`"


def register_module(app: Client):
    @app.on_message(filters.command("speedtest", prefixes=prefix_userbot))
    async def speedtest_command(_, message):
        await message.reply_text("**⌛Начинаю тест скорости...**")
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        results = st.results.dict()
        
        download_speed = results["download"] / 1_000_000  # Convert to Mbps
        upload_speed = results["upload"] / 1_000_000  # Convert to Mbps
        ping = results["ping"]
        server = results["server"]["sponsor"]

        reply_text = (f"**🏎️ Speedtest Results:**\n"
                      f"**🔻 Download Speed:** {download_speed:.2f} Mbps\n"
                      f"**🔺 Upload Speed:** {upload_speed:.2f} Mbps\n"
                      f"**📶 Ping:** {ping} ms\n"
                      f"**🏢 Server:** {server}")

        await message.delete()
        await message.reply_text(reply_text)


print("Модуль speedtest загружен!")
