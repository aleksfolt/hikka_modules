from pyrogram import Client, filters
import asyncio

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])
    print(OWNER_ID)

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("spam", prefixes=prefix_userbot))
    async def spam(_, message):
        try:
            parts = message.text.split(" ", maxsplit=3)
            count = int(parts[1])
            text = parts[2]
            delay = float(parts[3])

            for _ in range(count):
                await message.reply_text(text)
                await asyncio.sleep(delay)

        except IndexError:
            await message.reply_text("**❌ Неправильный формат команды. Пример: `.spam 10 привет 0.1`**")
        except ValueError:
            await message.reply_text("**❌ Убедитесь, что количество сообщений и задержка указаны правильно.**")
        except Exception as e:
            await message.reply_text(f"**❌ Произошла ошибка: {e}**")
