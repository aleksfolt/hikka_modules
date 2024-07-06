# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the Copyleft license.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: Verify
# Author: YourName
# Commands:
# .chatcaptchaon
# .chatcaptchaoff
# ---------------------------------------------------------------------------------

import asyncio
import logging
from typing import List

import telethon
from telethon import types
from telethon.events import ChatAction
from telethon.tl.functions.channels import EditBannedRequest, EditAdminRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelAdminRights

from .. import loader, utils  # type: ignore

@loader.tds
class VerifyMod(loader.Module):
    "Verification for new chat members"
    
    strings = {
        "name": "Verify",
        "pls_verify": (
            '<a href="tg://user?id={}">Hello</a>, please verify yourself by clicking the button below within 20 minutes or you will be kicked!'
        ),
        "verify_status": "<b>[Verify]</b> {}",
        "verify_success": "✅ <a href='tg://user?id={}'>You have been verified!</a>",
        "verify_fail": "❌ <a href='tg://user?id={}'>You have failed to verify and have been kicked.",
    }
    
    class CUserModel(pydantic.BaseModel):
        chat: int
        user: int
        message: int

    async def client_ready(self, client, db):
        self.db = db
        self.log = logging.getLogger(__name__)
        self._db = "VerifyMod"
        self.locked_users: List[self.CUserModel] = []
    
    async def watcher(self, event):
        "Watcher"
        client: telethon.TelegramClient = event.client
        if isinstance(event, ChatAction.Event):
            if event.chat_id not in self.db.get(self._db, "chats", []):
                return
            if event.user_added or event.user_joined:
                for user in event.users:
                    if user.bot:
                        continue
                    self.locked_users.append(self.CUserModel(chat=event.chat_id, user=user.id, message=0))
                    await client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, send_messages=True)))
                    msg = await client.send_message(event.chat_id, self.strings["pls_verify"].format(user.id), buttons=[types.KeyboardButtonCallback("Verify", data=f"verify_{user.id}")])
                    self.locked_users[-1].message = msg.id
                
                await asyncio.sleep(1200)
                for locked_user in list(filter(lambda x: x.chat == event.chat_id and x.user in [user.id for user in event.users], self.locked_users)):
                    self.locked_users.remove(locked_user)
                    await client(EditBannedRequest(locked_user.chat, locked_user.user, ChatBannedRights(until_date=None, view_messages=True)))
                    await client.kick_participant(locked_user.chat, locked_user.user)
                    await client.send_message(locked_user.chat, self.strings["verify_fail"].format(locked_user.user))
        
        if isinstance(event, types.Message):
            for locked_user in list(filter(lambda x: x.chat == event.chat_id and x.user == event.sender_id, self.locked_users)):
                self.locked_users.remove(locked_user)
                await client(EditBannedRequest(locked_user.chat, locked_user.user, ChatBannedRights(until_date=None, send_messages=None)))
                await client.delete_messages(locked_user.chat, locked_user.message)
                await client.send_message(locked_user.chat, self.strings["verify_success"].format(locked_user.user))

    async def chatcaptchaoncmd(self, m: types.Message):
        "Turn on captcha in chat"
        l: list = self.db.get(self._db, "chats", [])
        if m.chat_id in l:
            return await utils.answer(m, self.strings("verify_status").format("already ON"))
        l.append(m.chat_id)
        self.db.set(self._db, "chats", l)
        await utils.answer(m, self.strings("verify_status").format("ON"))

    async def chatcaptchaoffcmd(self, m: types.Message):
        "Turn off captcha in chat"
        l: list = self.db.get(self._db, "chats", [])
        if m.chat_id not in l:
            return await utils.answer(m, self.strings("verify_status").format("already OFF"))
        l.remove(m.chat_id)
        self.db.set(self._db, "chats", l)
        await utils.answer(m, self.strings("verify_status").format("OFF"))
