# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Captcha
# Author: AleksFolt
# Commands:
# .swcaptcha
# ---------------------------------------------------------------------------------

# meta developer: @aleksfolt

import logging
from typing import List

from telethon import TelegramClient, events, Button, types
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from .. import loader, utils  # type: ignore

logger = logging.getLogger(__name__)

@loader.tds
class CaptchaMod(loader.Module):
    """Captcha for chats"""

    strings = {
        "name": "Captcha",
        "pls_pass_captcha": (
            '<a href="tg://user?id={}">Хэй</a>, пройди капчу! Нажми на кнопку ниже чтобы разблокироваться!'
        ),
        "captcha_status": "<b>[Captcha]</b> {}",
        "verification_success": "✅ <b>Вы успешно прошли проверку!</b>",
    }

    class CUserModel:
        def __init__(self, chat, user, message):
            self.chat = chat
            self.user = user
            self.message = message

    async def client_ready(self, _, db):
        self.db = db
        self.log = logging.getLogger(__name__)
        self._db = "CaptchaMod"
        self.locked_users: List[self.CUserModel] = []

    async def watcher(self, m):
        "Watcher"
        client: TelegramClient = m.client
        if isinstance(m, events.ChatAction.Event):
            if m.chat_id not in self.db.get(self._db, "chats", []):
                return
            if m.user_added or m.user_joined:
                users = [i.id for i in m.users]
                for u in users:
                    _u = await client.get_entity(u)
                    if _u.bot:
                        continue
                    await client.edit_permissions(m.chat_id, u, send_messages=False)
                    m = await client.send_message(
                        m.chat_id,
                        self.strings("pls_pass_captcha").format(u),
                        buttons=[
                            Button.inline("Пройти проверку", data=f"verify_{u}")
                        ],
                    )
                    self.locked_users.append(self.CUserModel(m.chat_id, u, m.id))
                await asyncio.sleep(60)
                l: List[self.CUserModel] = list(
                    filter(lambda x: x.chat == m.chat_id and x.user in users, self.locked_users)
                )
                if l:
                    for u in l:
                        self.locked_users.remove(u)
                        await client.delete_messages(u.chat, ids=u.message)
                        await client(
                            EditBannedRequest(
                                u.chat,
                                u.user,
                                ChatBannedRights(until_date=None, view_messages=True),
                            )
                        )
            elif m.user_kicked or m.user_left:
                users = [i.id for i in m.users]
                for u in users:
                    l: List[self.CUserModel] = list(
                        filter(lambda x: x.chat == m.chat_id and x.user == u, self.locked_users)
                    )
                    if l:
                        ntt = l[0]
                        self.locked_users.remove(ntt)
                        return

        if isinstance(m, events.CallbackQuery.Event):
            client: TelegramClient = m.client
            if m.data.startswith(b"verify_"):
                user_id = int(m.data.split(b"_")[1])
                if m.query.user_id == user_id:
                    await client.edit_permissions(m.query.chat_id, user_id, send_messages=True)
                    await m.answer(self.strings["verification_success"], show_alert=True)
                    self.locked_users = [user for user in self.locked_users if user.user != user_id]
                    await client.delete_messages(m.query.chat_id, ids=m.query.msg_id)

    async def swcaptchacmd(self, m: types.Message):
        "Turn on/off captcha in chat"
        l: list = self.db.get(self._db, "chats", [])
        if m.chat_id in l:
            l.remove(m.chat_id)
            self.db.set(self._db, "chats", l)
            return await utils.answer(m, self.strings("captcha_status").format("OFF"))
        l.append(m.chat_id)
        self.db.set(self._db, "chats", l)
        await utils.answer(m, self.strings("captcha_status").format("ON"))
