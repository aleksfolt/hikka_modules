from pyrogram import Client, filters

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])
    print(OWNER_ID)

logging_enabled = False

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

def log_message(message):
    print(f"Chat ID: {message.chat.id}, User ID: {message.from_user.id}, Message: {message.text}")

def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("online", prefixes=prefix_userbot))
    async def toggle_logging(_, message):
        global logging_enabled
        logging_enabled = not logging_enabled
        status = "включен" if logging_enabled else "выключен"
        await message.reply_text(f"**✅ Логирование сообщений {status}.**")

    @app.on_message(filters.create(lambda _, __, m: logging_enabled))
    async def read_messages(_, message):
        log_message(message)
