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

cinfo = f"📝`{prefix_userbot}online`"
ccomand = " включает и выключает вечный онлайн, который будет читать сообщения в чатах."

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

logging_enabled = False

async def toggle_eternal_online(app, message):
    global logging_enabled
    logging_enabled = not logging_enabled
    status = "включен" if logging_enabled else "выключен"
    await message.reply_text(f"**✅ Вечный онлайн {status}.**")
    if logging_enabled:
        while logging_enabled:
            try:
                msg = await app.send_message("me", "Я все еще здесь! 👍")
                await msg.delete()
                await asyncio.sleep(1000)
            except asyncio.CancelledError:
                break

async def mark_all_as_read(app):
    async for dialog in app.get_dialogs():
        await app.send_read_acknowledge(dialog.chat.id, clear_mentions=True)

async def online_handler(client, message):
    await toggle_eternal_online(client, message)

async def read_messages_handler(client, message):
    if logging_enabled:
        await mark_all_as_read(client)

@app.on_message(filters.create(is_owner) & filters.command("online", prefixes=prefix_userbot))
async def online(_, message):
    await online_handler(app, message)

@app.on_message(filters.create(lambda _, __, m: logging_enabled))
async def read_messages(_, message):
    await read_messages_handler(app, message)
