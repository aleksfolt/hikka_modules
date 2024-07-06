# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔓 Not licensed.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Captcha
# Author: D4n13l3k00
# Commands:
# .chatcaptchaon
# .chatcaptchaoff
# ---------------------------------------------------------------------------------

# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00

import asyncio
import io
import logging
from typing import List

import aiohttp
import pydantic
import telethon
from telethon import types
from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

from .. import loader, utils  # type: ignore


@loader.tds
class CaptchaMod(loader.Module):
    "Captcha for chats"

    strings = {
        "name": "Captcha",
        "pls_pass_captcha": (
            '<a href="tg://user?id={}">Hello</a>, please verify yourself by clicking the button below within 20 minutes or you will be kicked!'
        ),
        "captcha_status": "<b>[Captcha]</b> {}",
        "verify_success": "✅ <a href='tg://user?id={}'>You have been verified!</a>",
        "verify_fail": "❌ <a href='tg://user?id={}'>You have failed to verify and have been kicked.</a>",
    }

    class CUserModel(pydantic.BaseModel):
        chat: int
        user: int
        message: int

    async def client_ready(self, _, db):
        self.db = db
        self.log = logging.getLogger(__name__)
        self._db = "CaptchaMod"
        self.locked_users: List[self.CUserModel] = []

    async def watcher(self, m):
        "Watcher"
        client: telethon.TelegramClient = m.client
        if isinstance(m, ChatAction.Event):
            if m.chat_id not in self.db.get(self._db, "chats", []):
                return
            if m.user_added or m.user_joined:
                users = [i.id for i in m.users]
                for u in users:
                    _u = await client.get_entity(u)
                    if _u.bot:
                        continue
                    self.locked_users.append(self.CUserModel(chat=m.chat_id, user=u.id, message=0))
                    await client(EditBannedRequest(m.chat_id, u.id, ChatBannedRights(until_date=None, send_messages=True)))
                    msg = await client.send_message(m.chat_id, self.strings["pls_pass_captcha"].format(u.id), buttons=[types.KeyboardButtonCallback("Verify", data=f"verify_{u.id}")])
                    self.locked_users[-1].message = msg.id
                
                await asyncio.sleep(1200)
                for locked_user in list(filter(lambda x: x.chat == m.chat_id and x.user in users, self.locked_users)):
                    self.locked_users.remove(locked_user)
                    await client(EditBannedRequest(locked_user.chat, locked_user.user, ChatBannedRights(until_date=None, view_messages=True)))
                    await client.kick_participant(locked_user.chat, locked_user.user)
                    await client.send_message(locked_user.chat, self.strings["verify_fail"].format(locked_user.user))
        
        if isinstance(m, types.Message):
            for locked_user in list(filter(lambda x: x.chat == m.chat_id and x.user == m.sender_id, self.locked_users)):
                self.locked_users.remove(locked_user)
                await client(EditBannedRequest(locked_user.chat, locked_user.user, ChatBannedRights(until_date=None, send_messages=None)))
                await client.delete_messages(locked_user.chat, locked_user.message)
                await client.send_message(locked_user.chat, self.strings["verify_success"].format(locked_user.user))

    async def chatcaptchaoncmd(self, m: types.Message):
        "Turn on captcha in chat"
        l: list = self.db.get(self._db, "chats", [])
        if m.chat_id in l:
            return await utils.answer(m, self.strings["captcha_status"].format("already ON"))
        l.append(m.chat_id)
        self.db.set(self._db, "chats", l)
        await utils.answer(m, self.strings["captcha_status"].format("ON"))

    async def chatcaptchaoffcmd(self, m: types.Message):
        "Turn off captcha in chat"
        l: list = self.db.get(self._db, "chats", [])
        if m.chat_id not in l:
            return await utils.answer(m, self.strings["captcha_status"].format("already OFF"))
        l.remove(m.chat_id)
        self.db.set(self._db, "chats", l)
        await utils.answer(m, self.strings["captcha_status"].format("OFF"))

    @loader.inline_everyone
    async def on_inline_callback_query(self, call: types.CallbackQuery):
        "Handle inline button clicks"
        data = call.data.decode("utf-8")
        if data.startswith("verify_"):
            user_id = int(data.split("_")[1])
            for locked_user in list(filter(lambda x: x.chat == call.chat_id and x.user == user_id, self.locked_users)):
                self.locked_users.remove(locked_user)
                await call.client(EditBannedRequest(locked_user.chat, locked_user.user, ChatBannedRights(until_date=None, send_messages=None)))
                await call.delete()
                await call.client.send_message(locked_user.chat, self.strings["verify_success"].format(locked_user.user))
