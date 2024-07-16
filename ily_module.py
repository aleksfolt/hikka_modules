import random
from pyrogram import Client, filters
from asyncio import sleep

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])
    print(OWNER_ID)

cinfo = f"📝`{prefix_userbot}ily`"
ccomand = " famous TikTok animation with hearts"

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

class ILYMod:
    """Famous TikTok hearts animation implemented in Pyrogram"""

    strings = {"name": "LoveMagic"}

    def __init__(self, app: Client):
        self.app = app

    async def ilycmd(self, client, message):
        """This famous TikTok animation..."""
        if not message.outgoing:
            message = await message.reply("ily")

        arr = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "💖"]
        h = "🤍"
        first_block = ""
        for i in "".join(
            [
                h * 9,
                "\n",
                h * 2,
                arr[0] * 2,
                h,
                arr[0] * 2,
                h * 2,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h * 2,
                arr[0] * 5,
                h * 2,
                "\n",
                h * 3,
                arr[0] * 3,
                h * 3,
                "\n",
                h * 4,
                arr[0],
                h * 4,
            ]
        ).split("\n"):
            first_block += i + "\n"
            await message.edit(first_block)
            await sleep(0.1)
        for i in arr:
            await message.edit(
                "".join(
                    [
                        h * 9,
                        "\n",
                        h * 2,
                        i * 2,
                        h,
                        i * 2,
                        h * 2,
                        "\n",
                        h,
                        i * 7,
                        h,
                        "\n",
                        h,
                        i * 7,
                        h,
                        "\n",
                        h,
                        i * 7,
                        h,
                        "\n",
                        h * 2,
                        i * 5,
                        h * 2,
                        "\n",
                        h * 3,
                        i * 3,
                        h * 3,
                        "\n",
                        h * 4,
                        i,
                        h * 4,
                        "\n",
                        h * 9,
                    ]
                )
            )
            await sleep(0.2)
        for _ in range(8):
            rand = random.choices(arr, k=34)
            await message.edit(
                "".join(
                    [
                        h * 9,
                        "\n",
                        h * 2,
                        rand[0],
                        rand[1],
                        h,
                        rand[2],
                        rand[3],
                        h * 2,
                        "\n",
                        h,
                        rand[4],
                        rand[5],
                        rand[6],
                        rand[7],
                        rand[8],
                        rand[9],
                        rand[10],
                        h,
                        "\n",
                        h,
                        rand[11],
                        rand[12],
                        rand[13],
                        rand[14],
                        rand[15],
                        rand[16],
                        rand[17],
                        h,
                        "\n",
                        h,
                        rand[18],
                        rand[19],
                        rand[20],
                        rand[21],
                        rand[22],
                        rand[23],
                        rand[24],
                        h,
                        "\n",
                        h * 2,
                        rand[25],
                        rand[26],
                        rand[27],
                        rand[28],
                        rand[29],
                        h * 2,
                        "\n",
                        h * 3,
                        rand[30],
                        rand[31],
                        rand[32],
                        h * 3,
                        "\n",
                        h * 4,
                        rand[33],
                        h * 4,
                        "\n",
                        h * 9,
                    ]
                )
            )
            await sleep(0.2)
        fourth = "".join(
            [
                h * 9,
                "\n",
                h * 2,
                arr[0] * 2,
                h,
                arr[0] * 2,
                h * 2,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h,
                arr[0] * 7,
                h,
                "\n",
                h * 2,
                arr[0] * 5,
                h * 2,
                "\n",
                h * 3,
                arr[0] * 3,
                h * 3,
                "\n",
                h * 4,
                arr[0],
                h * 4,
                "\n",
                h * 9,
            ]
        )
        await message.edit(fourth)
        for _ in range(47):
            fourth = fourth.replace("🤍", "❤️", 1)
            await message.edit(fourth)
            await sleep(0.07)
        for i in range(8):
            await message.edit((arr[0] * (8 - i) + "\n") * (8 - i))
            await sleep(0.3)
        for i in ["I", "I ❤️", "I ❤️ U", "I ❤️ U!"]:
            await message.edit(f"<b>{i}</b>")
            await sleep(0.2)

def register_module(app: Client):
    ily_mod = ILYMod(app)

    @app.on_message(filters.create(is_owner) & filters.command("ily", prefixes=prefix_userbot))
    async def ily(client, message):
        await ily_mod.ilycmd(client, message)
